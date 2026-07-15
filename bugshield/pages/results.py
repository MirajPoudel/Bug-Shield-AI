"""Results page — score circle, bugs, improvements, docs, metrics."""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from styles import score_color, score_rating, severity_color, language_color, score_circle_svg


def render(go):
    from pages.review import _navbar
    _navbar(go)

    result = st.session_state.get("review_result")
    if not result:
        st.markdown('<div class="bs-alert bs-alert-warning">⚠️ No review results found. Please run a review first.</div>', unsafe_allow_html=True)
        if st.button("Go to Review"):
            go("review")
        return

    analysis = result.get("analysis") or {}
    bugs = result.get("bugs") or []
    improvements = result.get("improvements") or []
    docs = result.get("docs") or ""
    language = result.get("language", "code")
    model = result.get("model", "")
    score = result.get("score") or analysis.get("score", 0) or 75
    summary = result.get("summary") or analysis.get("summary", "")
    is_demo = result.get("error") == "demo_mode"

    if is_demo:
        st.markdown("""
        <div class="bs-alert bs-alert-warning">
          ⚠️ <strong>Demo mode:</strong> Ollama is not running. Results are simulated for preview.
          Start Ollama with <code>ollama serve</code> for real AI analysis.
        </div>
        """, unsafe_allow_html=True)

    # ── Header badge ─────────────────────────────────────────────────
    st.markdown("""
    <div style="text-align:center; padding: 24px 0 16px;">
      <div class="bs-page-header-badge">⌨️ Code Review Results</div>
      <div class="bs-page-title">Review <span>Analysis</span></div>
    </div>
    """, unsafe_allow_html=True)

    # ── Score + Summary ───────────────────────────────────────────────
    score_col, info_col = st.columns([1, 2], gap="large")

    with score_col:
        rating_label, rating_color = score_rating(score)
        color = score_color(score)
        circle_svg = score_circle_svg(score, size=160)
        st.markdown(f"""
        <div style="background:#0d1829;border:1px solid #1a2744;border-radius:16px;padding:32px;text-align:center;">
          <div style="position:relative;width:160px;height:160px;margin:0 auto 16px;">
            {circle_svg}
            <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);text-align:center;">
              <div style="font-size:42px;font-weight:800;color:{color};line-height:1;">{score}</div>
              <div style="font-size:13px;color:#64748b;">out of 100</div>
            </div>
          </div>
          <div style="display:inline-flex;align-items:center;gap:8px;padding:6px 18px;
               background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.25);
               border-radius:20px;font-size:15px;font-weight:600;color:{rating_color};">
            ✓ {rating_label}
          </div>
          <div style="margin-top:16px;font-size:13px;color:#64748b;">
            Language: <strong style="color:#60a5fa;">{language}</strong><br>
            Model: <strong style="color:#a78bfa;">{model}</strong>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with info_col:
        # Summary
        st.markdown(f"""
        <div style="background:#0d1829;border:1px solid #1a2744;border-radius:16px;padding:24px;margin-bottom:14px;">
          <div style="font-size:16px;font-weight:700;color:#fff;margin-bottom:12px;">📋 Summary</div>
          <div style="font-size:15px;color:#cbd5e1;line-height:1.8;">{summary or "Code analysis complete."}</div>
        </div>
        """, unsafe_allow_html=True)

        # Quality Metrics
        readability = analysis.get("readability", 70)
        maintainability = analysis.get("maintainability", 85)
        best_practices = analysis.get("best_practices", 90)
        metrics = [
            ("Readability", readability),
            ("Maintainability", maintainability),
            ("Best Practices", best_practices),
        ]
        st.markdown('<div style="font-size:16px;font-weight:700;color:#fff;margin-bottom:12px;">📊 Code Quality Metrics</div>', unsafe_allow_html=True)
        m_cols = st.columns(3)
        for col, (label, val) in zip(m_cols, metrics):
            c = score_color(val)
            with col:
                st.markdown(f"""
                <div style="background:#0a1628;border:1px solid #1a2744;border-radius:10px;padding:16px;text-align:center;">
                  <div style="font-size:30px;font-weight:800;color:{c};line-height:1;">{val}</div>
                  <div style="font-size:12px;color:#64748b;margin-top:6px;text-transform:uppercase;letter-spacing:0.5px;">{label}</div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown('<div class="bs-divider"></div>', unsafe_allow_html=True)

    # ── Tabs: Bugs / Strengths / Improvements / Docs / Code ──────────
    tab_bugs, tab_strengths, tab_improve, tab_docs, tab_code = st.tabs([
        f"🐛 Bugs ({len(bugs)})",
        f"✅ Strengths ({len(analysis.get('strengths', []))})",
        f"💡 Improvements ({len(improvements)})",
        "📖 Documentation",
        "💻 Source Code",
    ])

    with tab_bugs:
        if not bugs:
            st.markdown("""
            <div style="text-align:center;padding:48px;color:#10b981;">
              <div style="font-size:48px;margin-bottom:16px;">✅</div>
              <div style="font-size:20px;font-weight:700;">No bugs found!</div>
              <div style="font-size:14px;color:#64748b;margin-top:8px;">Your code passed all bug detection checks.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Group by type
            perf_bugs = [b for b in bugs if b.get("type") == "performance"]
            sec_bugs = [b for b in bugs if b.get("type") == "security"]
            other_bugs = [b for b in bugs if b.get("type") not in ("performance", "security")]

            for group_label, group_icon, group in [
                ("Critical & Logic Bugs", "⚠️", other_bugs),
                ("Security Issues", "🔒", sec_bugs),
                ("Performance Issues", "⚡", perf_bugs),
            ]:
                if not group:
                    continue
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;font-size:18px;font-weight:700;color:#fff;margin:20px 0 12px;">
                  <span>{group_icon}</span> {group_label} ({len(group)})
                </div>
                """, unsafe_allow_html=True)
                for bug in group:
                    sev = bug.get("severity", "medium")
                    sev_color = severity_color(sev)
                    st.markdown(f"""
                    <div class="bs-bug-card" style="border-left:3px solid {sev_color};">
                      <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
                        <span style="background:{sev_color}22;color:{sev_color};padding:2px 10px;border-radius:5px;
                             font-size:12px;font-weight:600;text-transform:uppercase;">{sev}</span>
                        <div class="bs-bug-title">{bug.get('title','Issue')}</div>
                      </div>
                      <div class="bs-bug-desc">{bug.get('description','')}</div>
                      {'<div style="font-size:13px;color:#64748b;margin-bottom:8px;">📍 '+bug.get('line_hint','')+'</div>' if bug.get('line_hint') else ''}
                      <div class="bs-bug-solution">💡 <strong>Solution:</strong> {bug.get('solution','')}</div>
                    </div>
                    """, unsafe_allow_html=True)

    with tab_strengths:
        strengths = analysis.get("strengths", [])
        if not strengths:
            st.markdown('<div class="bs-alert bs-alert-info">No strengths data available.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="font-size:16px;font-weight:700;color:#fff;margin-bottom:16px;">What your code does well:</div>', unsafe_allow_html=True)
            for s in strengths:
                st.markdown(f"""
                <div class="bs-strength-item">
                  <span style="color:#10b981;font-size:18px;">✓</span>
                  <span>{s}</span>
                </div>
                """, unsafe_allow_html=True)

    with tab_improve:
        if not improvements:
            st.markdown('<div class="bs-alert bs-alert-info">No improvement suggestions available.</div>', unsafe_allow_html=True)
        else:
            for i, imp in enumerate(improvements, 1):
                cat = imp.get("category", "improvement")
                cat_colors = {
                    "performance": "#f97316", "readability": "#3b82f6",
                    "maintainability": "#8b5cf6", "security": "#ef4444",
                    "best_practice": "#10b981",
                }
                cat_color = cat_colors.get(cat, "#60a5fa")

                with st.expander(f"#{i} · {imp.get('title', 'Improvement')}", expanded=i <= 2):
                    st.markdown(f"""
                    <span style="background:{cat_color}22;color:{cat_color};padding:3px 10px;
                         border-radius:5px;font-size:12px;font-weight:600;text-transform:uppercase;
                         margin-bottom:12px;display:inline-block;">{cat}</span>
                    <div style="font-size:14px;color:#94a3b8;line-height:1.7;margin-bottom:16px;">{imp.get('description','')}</div>
                    """, unsafe_allow_html=True)

                    if imp.get("code_before") or imp.get("code_after"):
                        b_col, a_col = st.columns(2)
                        with b_col:
                            st.markdown('<div style="font-size:13px;color:#ef4444;font-weight:600;margin-bottom:6px;">Before:</div>', unsafe_allow_html=True)
                            if imp.get("code_before"):
                                st.code(imp["code_before"], language=result.get("language", "text"))
                        with a_col:
                            st.markdown('<div style="font-size:13px;color:#10b981;font-weight:600;margin-bottom:6px;">After:</div>', unsafe_allow_html=True)
                            if imp.get("code_after"):
                                st.code(imp["code_after"], language=result.get("language", "text"))

    with tab_docs:
        if not docs:
            st.markdown('<div class="bs-alert bs-alert-info">Documentation not available.</div>', unsafe_allow_html=True)
        else:
            st.markdown(docs)

    with tab_code:
        code = result.get("code", "")
        st.markdown(f'<div style="font-size:13px;color:#64748b;margin-bottom:8px;">{language} · {len(code)} characters · {len(code.splitlines())} lines</div>', unsafe_allow_html=True)
        st.code(code, language=language)

    # ── Action buttons ────────────────────────────────────────────────
    st.markdown('<div class="bs-divider"></div>', unsafe_allow_html=True)
    a1, a2, a3 = st.columns(3)
    with a1:
        if st.button("🔄 Review Another", key="review_another", use_container_width=True):
            go("review")
    with a2:
        if st.button("🕐 View History", key="goto_hist", use_container_width=True):
            go("history")
    with a3:
        # Download report as text
        report = _build_report(result)
        st.download_button(
            "📥 Download Report",
            data=report,
            file_name="bugshield_review.md",
            mime="text/markdown",
            use_container_width=True,
        )


def _build_report(result: dict) -> str:
    analysis = result.get("analysis") or {}
    bugs = result.get("bugs") or []
    improvements = result.get("improvements") or []
    docs = result.get("docs") or ""
    score = result.get("score", 0)
    lang = result.get("language", "")

    lines = [
        f"# BugShield-AI Code Review Report",
        f"",
        f"**Language:** {lang}  |  **Model:** {result.get('model', '')}  |  **Score:** {score}/100",
        f"",
        f"## Summary",
        result.get("summary", ""),
        f"",
        f"## Quality Metrics",
        f"- Readability: {analysis.get('readability', 'N/A')}",
        f"- Maintainability: {analysis.get('maintainability', 'N/A')}",
        f"- Best Practices: {analysis.get('best_practices', 'N/A')}",
        f"",
        f"## Bugs Found ({len(bugs)})",
    ]
    for bug in bugs:
        lines += [
            f"### [{bug.get('severity','').upper()}] {bug.get('title','')}",
            bug.get("description", ""),
            f"**Solution:** {bug.get('solution', '')}",
            "",
        ]
    lines += [f"## Improvement Suggestions ({len(improvements)})"]
    for imp in improvements:
        lines += [
            f"### {imp.get('title','')} ({imp.get('category','')})",
            imp.get("description", ""),
            "",
        ]
    if docs:
        lines += ["## Documentation", docs]
    return "\n".join(lines)
