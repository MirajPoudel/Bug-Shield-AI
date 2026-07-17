"""Custom CSS styles for BugShield-AI matching the dark navy theme."""

MAIN_CSS = """
<style>
/* ===== GLOBAL RESET & BASE ===== */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background-color: #050d1a !important;
    color: #e2e8f0 !important;
    font-family: 'Inter', sans-serif !important;
}

[data-testid="stSidebar"] {
    background-color: #080f20 !important;
    border-right: 1px solid #1a2744 !important;
}

[data-testid="stHeader"] {
    display: none !important;
    height: 0 !important;
    min-height: 0 !important;
    padding: 0 !important;
    visibility: hidden !important;
}

/* ── Strip every bit of top padding Streamlit inserts after hiding the header.
   We use the most-specific selector chain possible so it beats Emotion styles. ── */
html body div[data-testid="stAppViewContainer"]
    section[data-testid="stMain"]
    div[data-testid="stMainBlockContainer"] {
    padding-top: 0 !important;
}
html body div[data-testid="stAppViewContainer"]
    section[data-testid="stMain"] > div {
    padding-top: 0 !important;
}
/* Catch-all for older selector shapes */
[data-testid="stMainBlockContainer"],
[data-testid="stAppViewBlockContainer"],
section[data-testid="stMain"],
.block-container,
div.block-container,
.main .block-container {
    padding-top: 0 !important;
    margin-top: 0 !important;
}

/* Hide Streamlit default elements */
#MainMenu, footer, .stDeployButton { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }

/* ===== HEADER / NAVBAR ===== */
.bs-navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px 24px;
    background: rgba(8, 15, 32, 0.95);
    border-bottom: 1px solid #1a2744;
    position: sticky;
    top: 0;
    z-index: 100;
    margin-bottom: 0;
}

.bs-logo {
    display: flex;
    align-items: center;
    gap: 10px;
    text-decoration: none;
}

.bs-logo-icon {
    font-size: 28px;
    background: linear-gradient(135deg, #f97316, #3b82f6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 900;
}

.bs-logo-text {
    font-size: 20px;
    font-weight: 700;
    color: #fff;
    letter-spacing: -0.3px;
}

.bs-nav-links {
    display: flex;
    align-items: center;
    gap: 8px;
}

.bs-nav-btn {
    padding: 8px 16px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    border: none;
    transition: all 0.2s;
}

.bs-nav-btn-ghost {
    background: transparent;
    color: #94a3b8;
    border: 1px solid #1e3a5f;
}

.bs-nav-btn-ghost:hover { background: #1a2744; color: #fff; }

.bs-nav-btn-danger {
    background: rgba(239, 68, 68, 0.15);
    color: #ef4444;
    border: 1px solid rgba(239, 68, 68, 0.3);
}

.bs-user-badge {
    display: flex;
    align-items: center;
    gap: 10px;
}

.bs-avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: linear-gradient(135deg, #3b82f6, #8b5cf6);
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 16px;
    color: #fff;
}

/* ===== LANDING PAGE ===== */
.bs-hero {
    min-height: 85vh;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 60px 48px;
    gap: 60px;
}

.bs-hero-left { flex: 1; }

.bs-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 6px 14px;
    background: rgba(59, 130, 246, 0.1);
    border: 1px solid rgba(59, 130, 246, 0.3);
    border-radius: 20px;
    font-size: 13px;
    color: #60a5fa;
    margin-bottom: 24px;
}

.bs-badge-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #22c55e;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.6; transform: scale(0.8); }
}

.bs-hero-title {
    font-size: 56px;
    font-weight: 800;
    line-height: 1.1;
    color: #fff;
    margin-bottom: 20px;
}

.bs-hero-title span {
    background: linear-gradient(90deg, #3b82f6, #8b5cf6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.bs-hero-sub {
    font-size: 17px;
    color: #94a3b8;
    line-height: 1.7;
    max-width: 440px;
    margin-bottom: 36px;
}

.bs-hero-btns {
    display: flex;
    gap: 16px;
    flex-wrap: wrap;
}

.bs-btn-primary {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 13px 28px;
    background: linear-gradient(135deg, #2563eb, #7c3aed);
    color: #fff;
    border-radius: 10px;
    font-size: 16px;
    font-weight: 600;
    text-decoration: none;
    border: none;
    cursor: pointer;
    transition: all 0.2s;
    box-shadow: 0 4px 20px rgba(37, 99, 235, 0.4);
}

.bs-btn-primary:hover { transform: translateY(-2px); box-shadow: 0 6px 28px rgba(37, 99, 235, 0.5); }

.bs-btn-secondary {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 13px 28px;
    background: transparent;
    color: #e2e8f0;
    border: 1px solid #1e3a5f;
    border-radius: 10px;
    font-size: 16px;
    font-weight: 500;
    text-decoration: none;
    cursor: pointer;
    transition: all 0.2s;
}

.bs-btn-secondary:hover { background: #1a2744; border-color: #3b82f6; }

/* Terminal mockup */
.bs-terminal {
    background: #0d1117;
    border: 1px solid #21262d;
    border-radius: 12px;
    overflow: hidden;
    width: 440px;
    min-width: 320px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.5);
}

.bs-terminal-header {
    background: #161b22;
    padding: 12px 16px;
    display: flex;
    align-items: center;
    gap: 8px;
    border-bottom: 1px solid #21262d;
}

.bs-terminal-dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
}

.bs-terminal-title {
    font-size: 13px;
    color: #8b949e;
    margin-left: 8px;
    font-family: 'JetBrains Mono', monospace;
}

.bs-terminal-body {
    padding: 20px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    line-height: 1.8;
}

.bs-term-cmd { color: #e6edf3; }
.bs-term-info { color: #8b949e; }
.bs-term-ok { color: #3fb950; }
.bs-term-warn { color: #d29922; }
.bs-term-accent { color: #79c0ff; }
.bs-term-score { color: #ff7b72; }

/* ===== AUTH / LOGIN ===== */
.bs-auth-page {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 40px 20px;
    background: radial-gradient(ellipse at 50% 0%, rgba(37,99,235,0.12) 0%, transparent 70%);
}

.bs-auth-logo {
    text-align: center;
    margin-bottom: 24px;
}

.bs-auth-logo-icon {
    font-size: 42px;
    display: block;
    margin-bottom: 8px;
}

.bs-auth-logo-name {
    font-size: 28px;
    font-weight: 800;
    color: #fff;
}

.bs-auth-tagline { font-size: 15px; color: #94a3b8; margin-bottom: 8px; }

.bs-auth-card {
    background: #0d1829;
    border: 1px solid #1a2744;
    border-radius: 16px;
    padding: 36px;
    width: 100%;
    max-width: 460px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.4);
}

.bs-auth-title { font-size: 22px; font-weight: 700; color: #fff; margin-bottom: 4px; }
.bs-auth-subtitle { font-size: 14px; color: #64748b; margin-bottom: 28px; }

/* ===== INPUT FIELDS ===== */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: #0a1628 !important;
    border: 1px solid #1e3a5f !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
    font-family: 'Inter', sans-serif !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 2px rgba(59,130,246,0.2) !important;
}

.stSelectbox > div > div {
    background: #0a1628 !important;
    border: 1px solid #1e3a5f !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
}

/* Labels */
.stTextInput label, .stTextArea label, .stSelectbox label, .stRadio label {
    color: #94a3b8 !important;
    font-size: 13px !important;
    font-weight: 500 !important;
}

/* ===== BUTTONS ===== */
.stButton > button {
    background: linear-gradient(135deg, #2563eb, #7c3aed) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    padding: 12px 28px !important;
    transition: all 0.2s !important;
    width: 100% !important;
}

.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 24px rgba(37,99,235,0.4) !important;
}

/* Secondary buttons */
.btn-secondary > button {
    background: transparent !important;
    border: 1px solid #1e3a5f !important;
    color: #94a3b8 !important;
}

.btn-danger > button {
    background: rgba(239,68,68,0.1) !important;
    border: 1px solid rgba(239,68,68,0.3) !important;
    color: #ef4444 !important;
}

/* ===== SCORE CIRCLE ===== */
.bs-score-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 32px;
}

.bs-score-circle-container {
    position: relative;
    width: 160px;
    height: 160px;
    margin-bottom: 20px;
}

.bs-score-circle-container svg {
    transform: rotate(-90deg);
}

.bs-score-text {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
}

.bs-score-num {
    font-size: 42px;
    font-weight: 800;
    line-height: 1;
}

.bs-score-label {
    font-size: 13px;
    color: #64748b;
}

.bs-rating-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 14px;
    font-weight: 600;
    margin-top: 12px;
}

/* ===== STATS CARDS ===== */
.bs-stats-row {
    display: flex;
    gap: 1px;
    background: #1a2744;
    border-radius: 12px;
    overflow: hidden;
    margin-bottom: 24px;
}

.bs-stat {
    flex: 1;
    background: #0d1829;
    padding: 24px;
    text-align: center;
}

.bs-stat-num {
    font-size: 36px;
    font-weight: 800;
    line-height: 1;
    margin-bottom: 6px;
}

.bs-stat-label {
    font-size: 13px;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* ===== REVIEW CARDS (History) ===== */
.bs-review-card {
    background: #0d1829;
    border: 1px solid #1a2744;
    border-radius: 12px;
    padding: 18px 22px;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 18px;
    cursor: pointer;
    transition: all 0.2s;
}

.bs-review-card:hover {
    border-color: #2563eb;
    background: #101f3a;
}

.bs-review-score-badge {
    min-width: 52px;
    height: 52px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    font-weight: 800;
}

.bs-review-info { flex: 1; min-width: 0; }

.bs-review-tags {
    display: flex;
    gap: 8px;
    margin-bottom: 6px;
}

.bs-tag {
    padding: 3px 10px;
    border-radius: 5px;
    font-size: 12px;
    font-weight: 600;
    font-family: 'JetBrains Mono', monospace;
}

.bs-review-code-preview {
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    color: #64748b;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.bs-review-meta {
    font-size: 12px;
    color: #475569;
    text-align: right;
    white-space: nowrap;
}

/* ===== ANALYSIS SECTIONS ===== */
.bs-section {
    background: #0d1829;
    border: 1px solid #1a2744;
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 16px;
}

.bs-section-title {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 18px;
    font-weight: 700;
    color: #fff;
    margin-bottom: 18px;
}

.bs-bug-card {
    background: #0a1628;
    border: 1px solid #1a2744;
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 10px;
}

.bs-bug-title { font-weight: 600; color: #e2e8f0; margin-bottom: 6px; }
.bs-bug-desc { font-size: 14px; color: #64748b; margin-bottom: 8px; line-height: 1.6; }
.bs-bug-solution { font-size: 13px; color: #60a5fa; }

.bs-strength-item {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    padding: 12px 16px;
    background: rgba(16,185,129,0.05);
    border: 1px solid rgba(16,185,129,0.15);
    border-radius: 8px;
    margin-bottom: 8px;
    font-size: 14px;
    color: #d1fae5;
}

.bs-metrics-row {
    display: flex;
    gap: 12px;
}

.bs-metric-card {
    flex: 1;
    background: #0a1628;
    border: 1px solid #1a2744;
    border-radius: 10px;
    padding: 20px;
    text-align: center;
}

.bs-metric-num {
    font-size: 32px;
    font-weight: 800;
    line-height: 1;
    margin-bottom: 6px;
}

.bs-metric-label {
    font-size: 12px;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* ===== IMPROVEMENT CARDS ===== */
.bs-improve-card {
    background: #0a1628;
    border: 1px solid #1a2744;
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 10px;
}

.bs-improve-title { font-weight: 600; color: #e2e8f0; margin-bottom: 4px; }
.bs-improve-desc { font-size: 14px; color: #64748b; line-height: 1.6; }

/* ===== CODE BLOCKS ===== */
.bs-code-block {
    background: #0a0f1a;
    border: 1px solid #1a2744;
    border-radius: 8px;
    padding: 16px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    color: #e2e8f0;
    overflow-x: auto;
    white-space: pre-wrap;
    margin: 8px 0;
}

/* ===== TABS ===== */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid #1a2744 !important;
    gap: 4px;
}

.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #64748b !important;
    border-radius: 8px 8px 0 0 !important;
    font-weight: 500 !important;
    padding: 10px 20px !important;
}

.stTabs [aria-selected="true"] {
    background: rgba(37,99,235,0.1) !important;
    color: #60a5fa !important;
    border-bottom: 2px solid #3b82f6 !important;
}

/* ===== ALERTS / INFO ===== */
.bs-alert {
    padding: 14px 18px;
    border-radius: 10px;
    font-size: 14px;
    margin-bottom: 16px;
    display: flex;
    align-items: flex-start;
    gap: 10px;
}

.bs-alert-info { background: rgba(59,130,246,0.08); border: 1px solid rgba(59,130,246,0.2); color: #93c5fd; }
.bs-alert-warning { background: rgba(245,158,11,0.08); border: 1px solid rgba(245,158,11,0.2); color: #fcd34d; }
.bs-alert-error { background: rgba(239,68,68,0.08); border: 1px solid rgba(239,68,68,0.2); color: #fca5a5; }
.bs-alert-success { background: rgba(16,185,129,0.08); border: 1px solid rgba(16,185,129,0.2); color: #6ee7b7; }

/* ===== DIVIDERS ===== */
.bs-divider {
    height: 1px;
    background: #1a2744;
    margin: 24px 0;
}

/* ===== FILE UPLOAD ===== */
[data-testid="stFileUploader"] {
    background: #0d1829 !important;
    border: 2px dashed #1e3a5f !important;
    border-radius: 12px !important;
}

/* ===== PROGRESS / SPINNER ===== */
.stProgress > div > div {
    background: linear-gradient(90deg, #2563eb, #7c3aed) !important;
    border-radius: 4px !important;
}

/* ===== SCROLLBAR ===== */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #050d1a; }
::-webkit-scrollbar-thumb { background: #1e3a5f; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #2563eb; }

/* ===== REVIEW PAGE HEADER ===== */
.bs-page-header {
    text-align: center;
    padding: 32px 24px 24px;
}

.bs-page-header-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 6px 14px;
    background: rgba(59,130,246,0.1);
    border: 1px solid rgba(59,130,246,0.3);
    border-radius: 20px;
    font-size: 13px;
    color: #60a5fa;
    margin-bottom: 16px;
}

.bs-page-title {
    font-size: 42px;
    font-weight: 800;
    color: #fff;
    margin-bottom: 12px;
}

.bs-page-title span {
    background: linear-gradient(90deg, #3b82f6, #8b5cf6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* ===== SIDEBAR STYLING ===== */
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stRadio label {
    color: #94a3b8 !important;
}

[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
    color: #e2e8f0 !important;
}

/* ===== CHECKBOX ===== */
.stCheckbox label { color: #94a3b8 !important; font-size: 14px !important; }

/* ===== Spinner overlay ===== */
.bs-agent-step {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 16px;
    background: #0d1829;
    border: 1px solid #1a2744;
    border-radius: 8px;
    margin-bottom: 8px;
    font-size: 14px;
}

.bs-agent-step.done { border-color: rgba(16,185,129,0.3); }
.bs-agent-step.active { border-color: rgba(59,130,246,0.4); background: rgba(37,99,235,0.05); }

.bs-step-icon { font-size: 18px; min-width: 24px; }
.bs-step-name { font-weight: 500; color: #e2e8f0; }
.bs-step-desc { font-size: 13px; color: #64748b; margin-top: 2px; }

</style>
"""

def inject_css():
    import streamlit as st
    st.markdown(MAIN_CSS, unsafe_allow_html=True)


def score_color(score: int) -> str:
    if score >= 80:
        return "#10b981"
    elif score >= 60:
        return "#f59e0b"
    else:
        return "#ef4444"


def score_rating(score: int) -> tuple[str, str]:
    """Returns (label, color)"""
    if score >= 90:
        return "Excellent", "#10b981"
    elif score >= 75:
        return "Good", "#10b981"
    elif score >= 60:
        return "Fair", "#f59e0b"
    else:
        return "Poor", "#ef4444"


def severity_color(severity: str) -> str:
    return {
        "critical": "#ef4444",
        "high": "#f97316",
        "medium": "#f59e0b",
        "low": "#64748b"
    }.get(severity.lower(), "#64748b")


def language_color(lang: str) -> str:
    return {
        "python": "#3b82f6",
        "javascript": "#f59e0b",
        "typescript": "#60a5fa",
        "java": "#ef4444",
        "go": "#06b6d4",
        "rust": "#f97316",
        "cpp": "#8b5cf6",
        "c": "#6366f1",
    }.get(lang.lower(), "#64748b")


def score_circle_svg(score: int, size: int = 160) -> str:
    color = score_color(score)
    radius = (size - 16) // 2
    circ = 2 * 3.14159 * radius
    dash = (score / 100) * circ
    return f"""
<svg width="{size}" height="{size}" style="transform:rotate(-90deg)">
  <circle cx="{size//2}" cy="{size//2}" r="{radius}" fill="none" stroke="#1a2744" stroke-width="10"/>
  <circle cx="{size//2}" cy="{size//2}" r="{radius}" fill="none" stroke="{color}" stroke-width="10"
    stroke-dasharray="{dash:.1f} {circ:.1f}"
    stroke-linecap="round"/>
</svg>"""
