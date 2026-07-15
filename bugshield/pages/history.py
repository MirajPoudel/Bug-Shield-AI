"""History page — stats + list of past reviews matching screenshot 166."""
import streamlit as st
import sys, os
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from auth import get_reviews, get_user_stats
from styles import score_color, score_rating, language_color


def _relative_time(iso: str) -> str:
    try:
        dt = datetime.fromisoformat(iso)
        diff = datetime.now() - dt
        secs = int(diff.total_seconds())
        if secs < 60:
            return "Just now"
        elif secs < 3600:
            return f"{secs // 60}m ago"
        elif secs < 86400:
            return f"{secs // 3600}hr ago"
        else:
            return f"{secs // 86400}d ago"
    except Exception:
        return "—"


def render(go):
    from pages.review import _navbar
    _navbar(go)

    username = st.session_state.username
    reviews = get_reviews(username)
    stats = get_user_stats(username)

    # ── Page title ────────────────────────────────────────────────────
    st.markdown("""
    <div style="text-align:center;padding:24px 0 20px;">
      <div class="bs-page-header-badge">🕐 Review History</div>
      <div class="bs-page-title">Your <span>History</span></div>
      <div style="font-size:15px;color:#64748b;">All your past code reviews in one place</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Stats row ─────────────────────────────────────────────────────
    s1, s2, s3 = st.columns(3)
    stat_defs = [
        (stats["total"], "Total Reviews", "#e2e8f0"),
        (stats["avg_score"], "Avg Score", "#10b981"),
        (stats["best_score"], "Best Score", "#60a5fa"),
    ]
    for col, (num, label, color) in zip([s1, s2, s3], stat_defs):
        with col:
            st.markdown(f"""
            <div style="background:#0d1829;border:1px solid #1a2744;border-radius:12px;
                 padding:24px;text-align:center;">
              <div style="font-size:40px;font-weight:800;color:{color};line-height:1;margin-bottom:6px;">{num}</div>
              <div style="font-size:13px;color:#64748b;text-transform:uppercase;letter-spacing:0.5px;">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div style="height:24px"></div>', unsafe_allow_html=True)

    if not reviews:
        # Empty state
        st.markdown("""
        <div style="text-align:center;padding:64px 24px;background:#0d1829;border:1px solid #1a2744;border-radius:16px;">
          <div style="font-size:56px;margin-bottom:20px;">🛡️</div>
          <div style="font-size:22px;font-weight:700;color:#e2e8f0;margin-bottom:10px;">No reviews yet</div>
          <div style="font-size:15px;color:#64748b;margin-bottom:28px;">
            Run your first code review to see results here.
          </div>
        </div>
        """, unsafe_allow_html=True)
        _, cta, _ = st.columns([2, 1, 2])
        with cta:
            if st.button("🔍 Start First Review", use_container_width=True, type="primary"):
                go("review")
        return

    # ── Search / filter ───────────────────────────────────────────────
    fl, fr = st.columns([3, 1])
    with fl:
        search = st.text_input("🔍 Search reviews", placeholder="Search by language, score, or code...", label_visibility="collapsed", key="hist_search")
    with fr:
        filter_lang = st.selectbox("Language", ["All"] + sorted(set(r.get("language", "—") for r in reviews)),
                                   label_visibility="collapsed", key="hist_filter")

    # Apply filters
    filtered = reviews
    if search:
        q = search.lower()
        filtered = [r for r in filtered if
                    q in r.get("language", "").lower() or
                    q in r.get("code_preview", "").lower() or
                    q in str(r.get("score", ""))]
    if filter_lang != "All":
        filtered = [r for r in filtered if r.get("language") == filter_lang]

    st.markdown(f'<div style="font-size:13px;color:#64748b;margin:12px 0;">{len(filtered)} review{"s" if len(filtered)!=1 else ""}</div>', unsafe_allow_html=True)

    # ── Review list ───────────────────────────────────────────────────
    for idx, rev in enumerate(filtered):
        score = rev.get("score", 0)
        lang = rev.get("language", "unknown")
        rating_label, rating_color = score_rating(score)
        sc = score_color(score)
        lc = language_color(lang)
        ts = _relative_time(rev.get("timestamp", ""))
        preview = rev.get("code_preview", "")[:80]

        col_card, col_btn = st.columns([6, 1])
        with col_card:
            st.markdown(f"""
            <div class="bs-review-card">
              <div class="bs-review-score-badge" style="background:{sc}18;color:{sc};">{score}</div>
              <div class="bs-review-info">
                <div class="bs-review-tags">
                  <span class="bs-tag" style="background:{lc}20;color:{lc};">{lang}</span>
                  <span class="bs-tag" style="background:{rating_color}18;color:{rating_color};">{rating_label}</span>
                </div>
                <div class="bs-review-code-preview">{preview}…</div>
              </div>
              <div class="bs-review-meta">🕐 {ts}</div>
            </div>
            """, unsafe_allow_html=True)

        with col_btn:
            if st.button("View →", key=f"view_rev_{idx}"):
                # Reconstruct result for viewing
                st.session_state.review_result = {
                    "code": rev.get("code_preview", "") + "\n# [Full code not stored in history]",
                    "language": lang,
                    "model": rev.get("model", ""),
                    "score": score,
                    "summary": (rev.get("analysis") or {}).get("summary", ""),
                    "analysis": rev.get("analysis") or {},
                    "bugs": rev.get("bugs") or [],
                    "improvements": rev.get("improvements") or [],
                    "docs": rev.get("docs") or "",
                    "error": None,
                }
                go("results")

    # ── Pagination hint ───────────────────────────────────────────────
    if len(filtered) > 10:
        st.markdown(f'<div style="text-align:center;font-size:13px;color:#475569;margin-top:16px;">Showing all {len(filtered)} reviews</div>', unsafe_allow_html=True)

    # ── Bottom action ─────────────────────────────────────────────────
    st.markdown('<div class="bs-divider"></div>', unsafe_allow_html=True)
    _, cta_col, _ = st.columns([3, 1, 3])
    with cta_col:
        if st.button("🔍 New Review", use_container_width=True, type="primary", key="new_review_btn"):
            go("review")
