"""BugShield-AI — Main Streamlit Application Entry Point"""
import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

st.set_page_config(
    page_title="BugShield-AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

from styles import inject_css
inject_css()

# ── Session state defaults ──────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "page" not in st.session_state:
    st.session_state.page = "landing"
if "review_result" not in st.session_state:
    st.session_state.review_result = None
if "selected_model" not in st.session_state:
    st.session_state.selected_model = "qwen2.5-coder"
if "auth_tab" not in st.session_state:
    st.session_state.auth_tab = "signin"

# ── Router ──────────────────────────────────────────────────────────
def go(page: str):
    st.session_state.page = page
    st.rerun()

page = st.session_state.page

if page == "landing":
    from pages.landing import render
    render(go)

elif page == "signin":
    from pages.login import render
    render(go, tab="signin")

elif page == "signup":
    from pages.login import render
    render(go, tab="signup")

elif page == "review":
    if not st.session_state.logged_in:
        go("signin")
    else:
        from pages.review import render
        render(go)

elif page == "history":
    if not st.session_state.logged_in:
        go("signin")
    else:
        from pages.history import render
        render(go)

elif page == "results":
    if not st.session_state.logged_in:
        go("signin")
    else:
        from pages.results import render
        render(go)

else:
    go("landing")
