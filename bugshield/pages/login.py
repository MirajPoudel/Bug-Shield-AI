"""Login and Signup page — matches the dark auth card design from screenshots."""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from auth import login, signup


def render(go, tab: str = "signin"):
    # Sync tab state
    if "auth_tab" not in st.session_state:
        st.session_state.auth_tab = tab

    st.markdown("""
    <div style="min-height: 100vh; display:flex; flex-direction:column; align-items:center; justify-content:center; padding: 40px 0;
         background: radial-gradient(ellipse at 50% 0%, rgba(37,99,235,0.10) 0%, transparent 65%);">
    """, unsafe_allow_html=True)

    # Logo
    st.markdown("""
    <div style="text-align:center; margin-bottom:24px;">
      <div style="font-size:52px; background:linear-gradient(135deg,#f97316,#3b82f6);
           -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
           font-weight:900; line-height:1;">⬡</div>
      <div style="font-size:26px; font-weight:800; color:#fff; margin-top:4px;">BugShield-AI</div>
      <div style="font-size:15px; color:#64748b; margin-top:6px;">Welcome back</div>
      <div style="font-size:14px; color:#475569; margin-top:2px;">Sign in to your account to continue</div>
    </div>
    """, unsafe_allow_html=True)

    # Center the form
    _, center, _ = st.columns([1, 1.4, 1])
    with center:
        st.markdown('<div class="bs-auth-card">', unsafe_allow_html=True)

        # Tab toggle
        tab_col1, tab_col2 = st.columns(2)
        with tab_col1:
            signin_active = st.session_state.auth_tab == "signin"
            btn_style = "primary" if signin_active else "secondary"
            if st.button("Sign In", key="tab_signin",
                         type="primary" if signin_active else "secondary",
                         use_container_width=True):
                st.session_state.auth_tab = "signin"
                st.rerun()
        with tab_col2:
            signup_active = st.session_state.auth_tab == "signup"
            if st.button("Sign Up", key="tab_signup",
                         type="primary" if signup_active else "secondary",
                         use_container_width=True):
                st.session_state.auth_tab = "signup"
                st.rerun()

        st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)

        if st.session_state.auth_tab == "signin":
            _render_signin(go)
        else:
            _render_signup(go)

        # Divider with OR
        st.markdown("""
        <div style="display:flex;align-items:center;gap:12px;margin:20px 0;">
          <div style="flex:1;height:1px;background:#1a2744;"></div>
          <div style="font-size:12px;color:#475569;text-transform:uppercase;letter-spacing:1px;">OR CONTINUE WITH</div>
          <div style="flex:1;height:1px;background:#1a2744;"></div>
        </div>
        """, unsafe_allow_html=True)

        oa, ob = st.columns(2)
        with oa:
            st.markdown("""<div style="background:#0a1628;border:1px solid #1e3a5f;border-radius:8px;
              padding:10px;text-align:center;font-size:14px;color:#94a3b8;cursor:pointer;">
              🔵 Google</div>""", unsafe_allow_html=True)
        with ob:
            st.markdown("""<div style="background:#0a1628;border:1px solid #1e3a5f;border-radius:8px;
              padding:10px;text-align:center;font-size:14px;color:#94a3b8;cursor:pointer;">
              ⚫ GitHub</div>""", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # Footer link
    if st.session_state.auth_tab == "signin":
        st.markdown("""
        <div style="text-align:center; margin-top:20px; font-size:14px; color:#64748b;">
          Don't have an account?
        </div>
        """, unsafe_allow_html=True)
        _, lnk, _ = st.columns([2, 1, 2])
        with lnk:
            if st.button("Sign up →", key="goto_signup", use_container_width=True):
                st.session_state.auth_tab = "signup"
                st.rerun()
    else:
        st.markdown("""
        <div style="text-align:center; margin-top:20px; font-size:14px; color:#64748b;">
          Already have an account?
        </div>
        """, unsafe_allow_html=True)
        _, lnk, _ = st.columns([2, 1, 2])
        with lnk:
            if st.button("Sign in →", key="goto_signin", use_container_width=True):
                st.session_state.auth_tab = "signin"
                st.rerun()

    # Back to landing
    _, back_col, _ = st.columns([2, 1, 2])
    with back_col:
        if st.button("← Back to home", key="back_home", use_container_width=True):
            go("landing")


def _render_signin(go):
    st.markdown('<div style="font-size:18px;font-weight:700;color:#fff;margin-bottom:4px;">Sign in</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:13px;color:#64748b;margin-bottom:20px;">Enter your credentials to access your account</div>', unsafe_allow_html=True)

    email = st.text_input("Email or Username", placeholder="you@example.com", key="signin_email")
    password = st.text_input("Password", type="password", placeholder="••••••••", key="signin_password")

    c1, c2 = st.columns([1, 1])
    with c1:
        remember = st.checkbox("Remember me", key="signin_remember")
    with c2:
        st.markdown('<div style="text-align:right;padding-top:4px;"><span style="font-size:13px;color:#60a5fa;">Forgot password?</span></div>', unsafe_allow_html=True)

    st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)

    if "signin_error" in st.session_state and st.session_state.signin_error:
        st.markdown(f'<div class="bs-alert bs-alert-error">⚠️ {st.session_state.signin_error}</div>', unsafe_allow_html=True)

    if st.button("Sign in", key="do_signin", use_container_width=True, type="primary"):
        if not email or not password:
            st.session_state.signin_error = "Please fill in all fields."
        else:
            success, result = login(email.strip(), password)
            if success:
                st.session_state.logged_in = True
                st.session_state.username = result
                st.session_state.signin_error = ""
                go("review")
            else:
                st.session_state.signin_error = result
        st.rerun()

    # Demo credentials hint
    st.markdown("""
    <div style="background:rgba(59,130,246,0.06);border:1px solid rgba(59,130,246,0.15);border-radius:8px;
         padding:12px 16px;margin-top:16px;font-size:13px;color:#93c5fd;">
      💡 <strong>Demo account:</strong> email <code>demo@bugshield.ai</code> / password <code>demo123</code>
    </div>
    """, unsafe_allow_html=True)


def _render_signup(go):
    st.markdown('<div style="font-size:18px;font-weight:700;color:#fff;margin-bottom:4px;">Create account</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:13px;color:#64748b;margin-bottom:20px;">Join BugShield-AI and start reviewing code</div>', unsafe_allow_html=True)

    username = st.text_input("Username", placeholder="yourname", key="signup_username")
    email = st.text_input("Email", placeholder="you@example.com", key="signup_email")
    password = st.text_input("Password", type="password", placeholder="Min. 6 characters", key="signup_password")
    confirm = st.text_input("Confirm Password", type="password", placeholder="Repeat password", key="signup_confirm")

    st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)

    if "signup_error" in st.session_state and st.session_state.signup_error:
        st.markdown(f'<div class="bs-alert bs-alert-error">⚠️ {st.session_state.signup_error}</div>', unsafe_allow_html=True)
    if "signup_success" in st.session_state and st.session_state.signup_success:
        st.markdown(f'<div class="bs-alert bs-alert-success">✅ {st.session_state.signup_success}</div>', unsafe_allow_html=True)

    if st.button("Create Account", key="do_signup", use_container_width=True, type="primary"):
        st.session_state.signup_error = ""
        st.session_state.signup_success = ""
        if not username or not email or not password or not confirm:
            st.session_state.signup_error = "Please fill in all fields."
        elif password != confirm:
            st.session_state.signup_error = "Passwords do not match."
        else:
            success, msg = signup(username.strip(), email.strip(), password)
            if success:
                st.session_state.signup_success = msg
                st.session_state.auth_tab = "signin"
            else:
                st.session_state.signup_error = msg
        st.rerun()
