"""Review page — code input with Paste / File / GitHub tabs + agent pipeline."""
import streamlit as st
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from auth import save_review

LANGUAGES = [
    "auto-detect", "python", "javascript", "typescript", "java",
    "go", "rust", "cpp", "c", "csharp", "ruby", "php", "swift",
    "kotlin", "scala", "html", "css", "bash", "sql",
]

MODELS = {
    "Qwen2.5-Coder 1.5B ⚡ (Fast — auto-installed)": "qwen2.5-coder:1.5b",
    "Qwen2.5-Coder 7B (Better quality)": "qwen2.5-coder:7b",
    "DeepSeek-Coder 1.3B ⚡ (Fast)": "deepseek-coder:1.3b",
    "DeepSeek-Coder 6.7B": "deepseek-coder:6.7b",
    "CodeLlama 7B": "codellama",
    "Llama3 (General)": "llama3",
}


def render(go):
    _navbar(go)

    # Page header
    st.markdown("""
    <div class="bs-page-header">
      <div class="bs-page-header-badge">⚙️ Code Review Results</div>
      <div class="bs-page-title">Review <span>Analysis</span></div>
      <div style="font-size:16px;color:#64748b;">Paste code, upload a file, or paste a GitHub URL</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Sidebar: model & language ────────────────────────────────────
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        model_label = st.selectbox(
            "AI Model",
            list(MODELS.keys()),
            key="model_select"
        )
        selected_model = MODELS[model_label]
        st.session_state.selected_model = selected_model

        st.markdown("---")
        st.markdown("### 📖 Models Info")
        st.markdown("""
        <div style="font-size:13px;color:#64748b;line-height:1.7;">
        Make sure <strong style="color:#60a5fa;">Ollama</strong> is running locally:
        <br><br>
        <code style="background:#0a1628;padding:4px 8px;border-radius:4px;font-size:12px;">ollama serve</code>
        <br><br>
        Pull a model:<br>
        <code style="background:#0a1628;padding:4px 8px;border-radius:4px;font-size:12px;">ollama pull qwen2.5-coder</code>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 🤖 Agent Pipeline")
        steps = [
            ("🔍", "Code Analyzer", "Structure & quality"),
            ("🐛", "Bug Detector", "Bugs & security"),
            ("💡", "Improvement Agent", "Refactoring tips"),
            ("📖", "Doc Generator", "Auto documentation"),
        ]
        for icon, name, desc in steps:
            st.markdown(f"""
            <div class="bs-agent-step">
              <span class="bs-step-icon">{icon}</span>
              <div>
                <div class="bs-step-name">{name}</div>
                <div class="bs-step-desc">{desc}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    # ── Input tabs ────────────────────────────────────────────────────
    tab_paste, tab_file, tab_github = st.tabs(["✏️  Paste Code", "📁  Upload File", "🐙  GitHub URL"])

    code_to_review = None
    detected_lang = "python"

    with tab_paste:
        lang_col, _ = st.columns([1, 3])
        with lang_col:
            lang = st.selectbox("Language", LANGUAGES, key="paste_lang")

        code_input = st.text_area(
            "Paste your code here",
            height=320,
            placeholder="# Paste your code here...\ndef example():\n    pass",
            key="code_paste",
            label_visibility="collapsed"
        )

        if code_input.strip():
            if lang == "auto-detect":
                from utils.github_fetcher import detect_language_from_code
                detected_lang = detect_language_from_code(code_input)
            else:
                detected_lang = lang
            code_to_review = code_input.strip()

    with tab_file:
        uploaded = st.file_uploader(
            "Upload a code file",
            type=["py", "js", "ts", "jsx", "tsx", "java", "go", "rs", "cpp",
                  "c", "cs", "rb", "php", "swift", "kt", "scala", "html", "css",
                  "sh", "sql", "txt", "r", "m"],
            key="file_upload",
            label_visibility="collapsed"
        )

        if uploaded:
            file_content = uploaded.read().decode("utf-8", errors="replace")
            from utils.github_fetcher import detect_language_from_code, _detect_language
            detected_lang = _detect_language(uploaded.name)
            if detected_lang == "text":
                detected_lang = detect_language_from_code(file_content)

            st.markdown(f"""
            <div class="bs-alert bs-alert-success">
              ✅ Loaded <strong>{uploaded.name}</strong> · {len(file_content)} chars · Language: <strong>{detected_lang}</strong>
            </div>
            """, unsafe_allow_html=True)
            st.code(file_content[:1000] + ("..." if len(file_content) > 1000 else ""), language=detected_lang)
            code_to_review = file_content

    with tab_github:
        gh_url = st.text_input(
            "GitHub URL",
            placeholder="https://github.com/owner/repo  or  https://github.com/owner/repo/blob/main/file.py",
            key="github_url",
            label_visibility="collapsed"
        )

        if gh_url.strip():
            st.markdown("""
            <div class="bs-alert bs-alert-info">
              💡 You can link to a single file or a full repository. For repos, the top 5 most relevant files will be analyzed.
            </div>
            """, unsafe_allow_html=True)

        if gh_url.strip() and st.button("🔍 Fetch from GitHub", key="fetch_gh"):
            with st.spinner("Fetching from GitHub..."):
                try:
                    from utils.github_fetcher import fetch_github_file, fetch_github_repo_files
                    if "/blob/" in gh_url or "raw.githubusercontent" in gh_url:
                        code, lang_gh, fname = fetch_github_file(gh_url.strip())
                        st.session_state.gh_code = code
                        st.session_state.gh_lang = lang_gh
                        st.session_state.gh_label = fname
                        st.session_state.gh_multi = False
                    else:
                        files = fetch_github_repo_files(gh_url.strip())
                        st.session_state.gh_files = files
                        st.session_state.gh_multi = True
                except Exception as e:
                    st.markdown(f'<div class="bs-alert bs-alert-error">⚠️ {e}</div>', unsafe_allow_html=True)

        if st.session_state.get("gh_multi") and "gh_files" in st.session_state:
            files = st.session_state.gh_files
            st.markdown(f"""<div class="bs-alert bs-alert-success">✅ Fetched {len(files)} files from repository</div>""", unsafe_allow_html=True)
            file_names = [f["filename"] for f in files]
            chosen = st.selectbox("Select file to review", file_names, key="gh_file_choice")
            chosen_file = next(f for f in files if f["filename"] == chosen)
            detected_lang = chosen_file["language"]
            code_to_review = chosen_file["code"]
            st.code(code_to_review[:800] + "...", language=detected_lang)

        elif not st.session_state.get("gh_multi") and "gh_code" in st.session_state:
            detected_lang = st.session_state.gh_lang
            code_to_review = st.session_state.gh_code
            st.markdown(f"""<div class="bs-alert bs-alert-success">✅ Loaded: <strong>{st.session_state.gh_label}</strong> · {detected_lang}</div>""", unsafe_allow_html=True)
            st.code(code_to_review[:800] + "...", language=detected_lang)

    # ── Review Button ─────────────────────────────────────────────────
    st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
    _, btn_col, _ = st.columns([1, 2, 1])
    with btn_col:
        do_review = st.button("🔍 Start AI Review →", key="start_review",
                              use_container_width=True, type="primary",
                              disabled=not bool(code_to_review))

    if do_review and code_to_review:
        _run_review(go, code_to_review, detected_lang, selected_model)


def _run_review(go, code: str, language: str, model: str):
    """Run the multi-agent pipeline with progress display."""
    st.markdown('<div class="bs-divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center; margin-bottom:24px;">
      <div style="font-size:20px;font-weight:700;color:#fff;">🤖 Running AI Agents...</div>
      <div style="font-size:14px;color:#64748b;margin-top:6px;">4 specialized agents analyzing your code</div>
    </div>
    """, unsafe_allow_html=True)

    steps = [
        ("🔍", "Code Analyzer", "Evaluating structure, quality & readability..."),
        ("🐛", "Bug Detector", "Scanning for bugs, security issues & performance problems..."),
        ("💡", "Improvement Agent", "Generating refactoring suggestions & better patterns..."),
        ("📖", "Documentation Generator", "Writing professional documentation..."),
    ]

    progress_bar = st.progress(0, text="Initializing agents...")
    status_placeholder = st.empty()

    for i, (icon, name, desc) in enumerate(steps):
        progress_bar.progress((i) / len(steps), text=f"Running {name}...")
        status_placeholder.markdown(f"""
        <div class="bs-agent-step active">
          <span class="bs-step-icon">{icon}</span>
          <div>
            <div class="bs-step-name">{name}</div>
            <div class="bs-step-desc">{desc}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(0.1)

    # Check Ollama availability
    try:
        import requests as req_lib
        resp = req_lib.get("http://localhost:11434/api/tags", timeout=3)
        ollama_ok = resp.status_code == 200
    except Exception:
        ollama_ok = False

    if not ollama_ok:
        progress_bar.progress(100, text="Using demo mode (Ollama not detected)")
        status_placeholder.markdown("""
        <div class="bs-alert bs-alert-warning">
          ⚠️ <strong>Ollama not detected</strong> at localhost:11434. Running in demo mode with simulated results.
          To use real AI: install Ollama, run <code>ollama serve</code>, then pull a model.
        </div>
        """, unsafe_allow_html=True)
        # Use mock
        from agents.graph import _mock_analysis, _mock_bugs, _mock_improvements, _mock_docs
        import re
        result = {
            "code": code,
            "language": language,
            "model": model,
            "analysis": _mock_analysis(),
            "bugs": _mock_bugs(),
            "improvements": _mock_improvements(),
            "docs": _mock_docs(language),
            "score": 85,
            "summary": "The code is well-structured and follows clean coding principles. There are some areas for improvement in readability, performance, and security.",
            "error": "demo_mode",
        }
    else:
        try:
            from agents.graph import run_review
            result = run_review(code=code, language=language, model=model)
            progress_bar.progress(100, text="Analysis complete!")
            status_placeholder.empty()
        except Exception as e:
            progress_bar.progress(100, text="Completed with errors")
            from agents.graph import _mock_analysis, _mock_bugs, _mock_improvements, _mock_docs
            result = {
                "code": code, "language": language, "model": model,
                "analysis": _mock_analysis(), "bugs": _mock_bugs(),
                "improvements": _mock_improvements(), "docs": _mock_docs(language),
                "score": 85, "summary": "Analysis completed.", "error": str(e),
            }

    # Save to history
    from auth import save_review
    save_review(st.session_state.username, {
        "language": language,
        "model": model,
        "score": result.get("score", 0) or (result.get("analysis") or {}).get("score", 0),
        "code_preview": code[:120],
        "analysis": result.get("analysis"),
        "bugs": result.get("bugs"),
        "improvements": result.get("improvements"),
        "docs": result.get("docs"),
        "summary": result.get("summary"),
    })

    st.session_state.review_result = result
    go("results")


def _navbar(go):
    u = st.session_state.username
    initial = u[0].upper() if u else "U"

    col_logo, col_spacer, col_nav = st.columns([2, 4, 3])
    with col_logo:
        st.markdown("""
        <div class="bs-logo" style="padding:14px 0;">
          <span class="bs-logo-icon">⬡</span>
          <span class="bs-logo-text">BugShield-AI</span>
        </div>
        """, unsafe_allow_html=True)

    with col_nav:
        n1, n2, n3, n4 = st.columns(4)
        with n1:
            st.markdown(f"""
            <div style="padding:10px 0;text-align:center;">
              <div style="width:34px;height:34px;border-radius:50%;background:linear-gradient(135deg,#3b82f6,#8b5cf6);
                   display:inline-flex;align-items:center;justify-content:center;font-weight:700;color:#fff;">{initial}</div>
              <div style="font-size:12px;color:#64748b;margin-top:2px;">{u}</div>
            </div>
            """, unsafe_allow_html=True)
        with n2:
            if st.button("⌨️ Review", key="nav_review"):
                go("review")
        with n3:
            if st.button("🕐 History", key="nav_history"):
                go("history")
        with n4:
            if st.button("⏏️ Logout", key="nav_logout"):
                st.session_state.logged_in = False
                st.session_state.username = ""
                st.session_state.review_result = None
                go("landing")

    st.markdown('<div class="bs-divider" style="margin:0 0 8px 0;"></div>', unsafe_allow_html=True)
