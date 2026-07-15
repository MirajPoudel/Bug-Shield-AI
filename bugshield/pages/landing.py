"""Landing page — matches the dark-navy hero design from the screenshots."""
import streamlit as st


def render(go):
    # ── Navbar ───────────────────────────────────────────────────────
    st.markdown("""
    <div class="bs-navbar">
      <div class="bs-logo">
        <span class="bs-logo-icon">⬡</span>
        <span class="bs-logo-text">BugShield-AI</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    col_sign, = [st.columns([1])[0]]  # right-align hack
    # Actually place Sign In button in a column layout
    nav_l, nav_r = st.columns([8, 1])
    with nav_r:
        if st.button("Sign In", key="nav_signin"):
            go("signin")

    # Fix: re-draw navbar without duplicate (use columns approach instead)
    # Remove the above markdown navbar and use columns properly:
    st.markdown('<div style="height:0"></div>', unsafe_allow_html=True)

    # ── Hero Section ──────────────────────────────────────────────────
    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown("""
        <div style="padding: 48px 0 40px 0;">
          <div class="bs-badge">
            <span class="bs-badge-dot"></span>
            AI-Powered Code Analysis
          </div>
          <div class="bs-hero-title">
            Smart Code<br><span>Reviewer</span>
          </div>
          <div class="bs-hero-sub">
            Catch bugs before they catch you. Get instant AI-powered code reviews
            with actionable scores and improvement suggestions.
          </div>
        </div>
        """, unsafe_allow_html=True)

        btn_l, btn_r = st.columns([1, 1])
        with btn_l:
            if st.button("🚀 Get Started →", key="hero_start"):
                go("signin")
        with btn_r:
            if st.button("Learn More", key="hero_learn"):
                st.session_state._show_features = True
                st.rerun()

    with right:
        st.markdown("""
        <div style="padding: 48px 0 40px 0; display:flex; justify-content:center;">
          <div class="bs-terminal">
            <div class="bs-terminal-header">
              <span class="bs-terminal-dot" style="background:#ff5f57"></span>
              <span class="bs-terminal-dot" style="background:#febc2e"></span>
              <span class="bs-terminal-dot" style="background:#28c840"></span>
              <span class="bs-terminal-title">bugshield — terminal</span>
            </div>
            <div class="bs-terminal-body">
              <div class="bs-term-cmd">$ bugshield review MyComponent.py</div>
              <div class="bs-term-info">Analyzing code for potential bugs and improvements...</div>
              <div class="bs-term-info">Running 4 AI agents...</div>
              <div style="height:8px"></div>
              <div class="bs-term-ok">✓ No critical bugs found.</div>
              <div class="bs-term-warn">⚠ 2 suggestions for code optimization.</div>
              <div class="bs-term-ok">✓ 1 style issue detected.</div>
              <div style="height:8px"></div>
              <div class="bs-term-info">Generating review report...</div>
              <div class="bs-term-score">🔥 Review complete! Score: 87/100 ▊</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Divider ───────────────────────────────────────────────────────
    st.markdown('<div class="bs-divider" style="margin: 0 0 40px 0;"></div>', unsafe_allow_html=True)

    # ── Features Grid ─────────────────────────────────────────────────
    st.markdown("""
    <div style="text-align:center; margin-bottom: 36px;">
      <div style="font-size:13px; color:#64748b; text-transform:uppercase; letter-spacing:2px; margin-bottom:12px;">FEATURES</div>
      <div style="font-size:36px; font-weight:800; color:#fff;">Everything you need to write<br><span style="background:linear-gradient(90deg,#3b82f6,#8b5cf6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">better code</span></div>
    </div>
    """, unsafe_allow_html=True)

    f1, f2, f3, f4 = st.columns(4)
    features = [
        ("🐛", "Bug Detection", "Identifies bugs, security vulnerabilities, and edge cases with detailed explanations and fix suggestions."),
        ("💡", "Code Improvements", "Suggests refactoring opportunities, better patterns, and performance optimizations."),
        ("📖", "Auto Documentation", "Generates clean, professional documentation for your functions, classes, and modules."),
        ("📊", "Quality Metrics", "Scores readability, maintainability, and best-practices adherence with actionable insights."),
    ]
    for col, (icon, title, desc) in zip([f1, f2, f3, f4], features):
        with col:
            st.markdown(f"""
            <div class="bs-section" style="text-align:center; height: 200px;">
              <div style="font-size:36px; margin-bottom:14px;">{icon}</div>
              <div style="font-size:16px; font-weight:700; color:#e2e8f0; margin-bottom:10px;">{title}</div>
              <div style="font-size:13px; color:#64748b; line-height:1.6;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── Supported inputs ─────────────────────────────────────────────
    st.markdown('<div class="bs-divider" style="margin: 40px 0;"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center; margin-bottom: 36px;">
      <div style="font-size:36px; font-weight:800; color:#fff; margin-bottom:12px;">Three ways to analyze code</div>
      <div style="font-size:16px; color:#64748b;">Paste code directly, upload a file, or point to a GitHub repository</div>
    </div>
    """, unsafe_allow_html=True)

    i1, i2, i3 = st.columns(3)
    inputs = [
        ("✏️", "Paste Code", "Paste any snippet directly in the editor. Supports 15+ languages with auto-detection."),
        ("📁", "Upload File", "Upload .py, .js, .ts, .java, .go and many more file formats for instant analysis."),
        ("🐙", "GitHub Repo", "Paste a GitHub URL (file or repo) to analyze your entire codebase remotely."),
    ]
    for col, (icon, title, desc) in zip([i1, i2, i3], inputs):
        with col:
            st.markdown(f"""
            <div style="background:#0d1829;border:1px solid #1a2744;border-radius:12px;padding:28px;text-align:center;">
              <div style="font-size:42px; margin-bottom:16px;">{icon}</div>
              <div style="font-size:18px; font-weight:700; color:#e2e8f0; margin-bottom:10px;">{title}</div>
              <div style="font-size:14px; color:#64748b; line-height:1.7;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── Models info ───────────────────────────────────────────────────
    st.markdown('<div class="bs-divider" style="margin: 40px 0;"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center; margin-bottom:36px;">
      <div style="font-size:36px; font-weight:800; color:#fff; margin-bottom:12px;">Powered by State-of-the-Art Models</div>
    </div>
    """, unsafe_allow_html=True)

    m1, m2 = st.columns(2)
    models = [
        ("🤖", "Qwen2.5-Coder", "Alibaba's code-specialized model. Excellent at understanding complex codebases, bug detection, and generating idiomatic code."),
        ("🧠", "DeepSeek-Coder", "DeepSeek's powerful coding model. Outstanding at multi-language support, code explanation, and documentation generation."),
    ]
    for col, (icon, name, desc) in zip([m1, m2], models):
        with col:
            st.markdown(f"""
            <div style="background:#0d1829;border:1px solid #1a2744;border-radius:12px;padding:28px;display:flex;gap:20px;align-items:flex-start;">
              <div style="font-size:42px;">{icon}</div>
              <div>
                <div style="font-size:20px;font-weight:700;color:#e2e8f0;margin-bottom:8px;">{name}</div>
                <div style="font-size:14px;color:#64748b;line-height:1.7;">{desc}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    # ── CTA ───────────────────────────────────────────────────────────
    st.markdown('<div class="bs-divider" style="margin: 40px 0;"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center; padding: 40px 0 60px;">
      <div style="font-size:40px; font-weight:800; color:#fff; margin-bottom:14px;">Ready to write better code?</div>
      <div style="font-size:16px; color:#64748b; margin-bottom:32px;">Join developers using BugShield-AI to catch bugs before they ship.</div>
    </div>
    """, unsafe_allow_html=True)

    _, cta_col, _ = st.columns([2, 1, 2])
    with cta_col:
        if st.button("🚀 Start for Free →", key="cta_btn"):
            go("signup")

    st.markdown("""
    <div style="text-align:center; margin-top:20px;">
      <span style="font-size:14px; color:#64748b;">Already have an account? </span>
      <a href="#" onclick="return false;" style="color:#60a5fa; font-size:14px; text-decoration:none;">Sign in</a>
    </div>
    """, unsafe_allow_html=True)
