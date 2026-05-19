"""UnderstandIQ UI Components"""

import streamlit as st


def render_header():
    st.markdown("""
    <div class="app-header">
        <div class="app-title">Understand<span>IQ</span></div>
        <div class="app-tagline">Discover the gap between what you think you know — and what you actually know.</div>
        <div class="app-badge">Built on HCMS Research · DOI: 10.5281/zenodo.18269740</div>
    </div>
    """, unsafe_allow_html=True)


def render_verdict_card(score: float, level: str, description: str):
    st.markdown(f"""
    <div class="verdict-block">
        <div class="verdict-score">{score:.0f}</div>
        <div class="verdict-level">{level}</div>
        <div class="verdict-desc">{description}</div>
    </div>
    """, unsafe_allow_html=True)


def render_metric_cards(accuracy: float, calibration: float, uiq: float):
    acc_color = "success" if accuracy >= 70 else ("warning" if accuracy >= 50 else "danger")
    cal_color = "success" if calibration >= 70 else ("warning" if calibration >= 50 else "danger")
    uiq_color = "accent"

    st.markdown(f"""
    <div class="metric-row">
        <div class="metric-card">
            <div class="metric-value metric-{acc_color}">{accuracy:.0f}%</div>
            <div class="metric-label">Accuracy</div>
        </div>
        <div class="metric-card">
            <div class="metric-value metric-{cal_color}">{calibration:.0f}%</div>
            <div class="metric-label">Calibration</div>
        </div>
        <div class="metric-card">
            <div class="metric-value metric-{uiq_color}">{uiq:.0f}</div>
            <div class="metric-label">UnderstandIQ Score</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_progress_bar(current: int, total: int):
    pct = (current / total) * 100
    st.markdown(f"""
    <div class="progress-label">{current} of {total}</div>
    <div class="progress-wrap">
        <div class="progress-fill" style="width: {pct}%"></div>
    </div>
    """, unsafe_allow_html=True)


def render_breakdown_table(answers: list):
    st.markdown('<div class="section-header">Question Breakdown</div>', unsafe_allow_html=True)
    for i, a in enumerate(answers):
        correct = a.get("is_correct", False)
        calib = a.get("calibration_status", "Well-calibrated")
        q_text = a.get("question_text", "")
        if len(q_text) > 65:
            q_text = q_text[:65] + "…"

        calib_class = {
            "Overconfident": "calib-over",
            "Underconfident": "calib-under",
            "Well-calibrated": "calib-good"
        }.get(calib, "calib-good")

        row_class = "breakdown-correct" if correct else "breakdown-wrong"
        icon = "✓" if correct else "✗"
        conf = a.get("confidence_rating", 3)
        tag = a.get("topic_tag", "General")

        st.markdown(f"""
        <div class="breakdown-row {row_class}">
            <div class="breakdown-status">{icon}</div>
            <div class="breakdown-question">{q_text}</div>
            <div class="breakdown-tag">{tag}</div>
            <div class="breakdown-calibration {calib_class}">{calib} · {conf}/5</div>
        </div>
        """, unsafe_allow_html=True)


def render_insights(insights: list):
    st.markdown('<div class="section-header">Learning Insights</div>', unsafe_allow_html=True)
    for insight in insights:
        st.markdown(f'<div class="insight-card">💡 {insight}</div>', unsafe_allow_html=True)


def render_recommendations(recs: list):
    st.markdown('<div class="section-header">Recommended Actions</div>', unsafe_allow_html=True)
    for rec in recs:
        st.markdown(f'<div class="rec-card">→ {rec}</div>', unsafe_allow_html=True)


def render_info(msg: str):
    st.markdown(f'<div class="info-box">{msg}</div>', unsafe_allow_html=True)


def render_success_msg(msg: str):
    st.markdown(f'<div class="success-box">✓ {msg}</div>', unsafe_allow_html=True)


def render_error(msg: str):
    st.markdown(f'<div class="error-box">⚠ {msg}</div>', unsafe_allow_html=True)


def render_section(title: str):
    st.markdown(f'<div class="section-header">{title}</div>', unsafe_allow_html=True)
