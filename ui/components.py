"""Reusable UI components for UnderstandIQ."""

import streamlit as st
from typing import Dict, List, Callable


def card(content: str, class_name: str = "uicard") -> None:
    """Render a card with content."""
    st.markdown(f'<div class="{class_name}">{content}</div>', unsafe_allow_html=True)


def render_metric_card(label: str, value: str, suffix: str = "", color: str = "primary") -> None:
    """Render a metric card."""
    color_map = {
        "primary": "var(--accent-primary)",
        "success": "var(--accent-success)",
        "warning": "var(--accent-warning)",
        "danger": "var(--accent-danger)"
    }
    color_value = color_map.get(color, color_map["primary"])

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value" style="color: {color_value}">{value}{suffix}</div>
    </div>
    """, unsafe_allow_html=True)


def render_verdict_card(score: float, level_name: str, description: str) -> None:
    """Render the main verdict card."""
    st.markdown(f"""
    <div class="verdict-card">
        <div class="verdict-title">{int(score)}</div>
        <div style="font-size: 24px; font-weight: 600; margin-bottom: 8px;">{level_name}</div>
        <div class="verdict-description">{description}</div>
    </div>
    """, unsafe_allow_html=True)


def render_insight_card(text: str) -> None:
    """Render an insight card."""
    st.markdown(f'<div class="insight-card">{text}</div>', unsafe_allow_html=True)


def render_recommendation_card(text: str) -> None:
    """Render a recommendation card."""
    st.markdown(f'<div class="recommendation-card">{text}</div>', unsafe_allow_html=True)


def render_question_card(question: Dict, question_num: int, total: int) -> None:
    """Render a question card."""
    st.markdown(f"""
    <div class="question-card">
        <div class="question-number">Question {question_num} of {total}</div>
        <div class="question-text">{question['question_text']}</div>
    </div>
    """, unsafe_allow_html=True)


def render_confidence_slider(on_change: Callable = None) -> int:
    """Render the confidence slider and return selected value (1-5)."""
    st.markdown('<div class="confidence-section">', unsafe_allow_html=True)
    st.markdown('<div class="confidence-label">How confident are you in your answer?</div>', unsafe_allow_html=True)

    options = ["1 — Just guessing", "2 — Somewhat unsure", "3 — Neutral", "4 — Fairly confident", "5 — Completely certain"]
    selected = st.select_slider(
        "Confidence Level",
        options=options,
        value="3 — Neutral",
        key="confidence_slider",
        help="Rate how confident you are in your answer before seeing results"
    )

    confidence_value = options.index(selected) + 1
    st.markdown(f'<div class="confidence-value">Selected: {confidence_value}/5</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    return confidence_value


def render_option_button(label: str, key: str, selected: bool = False) -> bool:
    """Render an option button and return if selected."""
    selected_class = "selected" if selected else ""
    return st.button(label, key=key, use_container_width=True)


def render_breakdown_row(q: Dict, index: int) -> None:
    """Render a single row in the question breakdown."""
    question_text = q.get('question_text', '')[:60] + '...' if len(q.get('question_text', '')) > 60 else q.get('question_text', '')
    topic = q.get('topic_tag', 'N/A')
    is_correct = q.get('is_correct', False)
    confidence = q.get('confidence_rating', 3)
    status = q.get('calibration_status', 'Unknown')

    status_color = {
        "Well-calibrated": "var(--accent-success)",
        "Overconfident": "var(--accent-danger)",
        "Underconfident": "var(--accent-warning)"
    }.get(status, "var(--text-secondary)")

    result_icon = "✓" if is_correct else "✗"

    st.markdown(f"""
    <div class="breakdown-row">
        <div class="breakdown-question">{question_text}</div>
        <div class="breakdown-topic">{topic}</div>
        <div class="breakdown-result" style="color: {'var(--accent-success)' if is_correct else 'var(--accent-danger)'}">{result_icon}</div>
        <div class="breakdown-confidence">{confidence}/5</div>
        <div class="breakdown-status" style="color: {status_color}">{status}</div>
    </div>
    """, unsafe_allow_html=True)


def render_progress_bar(current: int, total: int) -> None:
    """Render a progress bar."""
    progress = current / total
    st.progress(progress)


def render_document_info(filename: str, word_count: int, reading_time: int) -> None:
    """Render document information."""
    st.markdown(f"""
    <div class="uicard uicard-success">
        <strong>{filename}</strong><br>
        {word_count:,} words · ~{reading_time} min read
    </div>
    """, unsafe_allow_html=True)


def render_error(message: str) -> None:
    """Render an error message."""
    st.markdown(f"""
    <div class="uicard uicard-danger">
        <strong>Error:</strong> {message}
    </div>
    """, unsafe_allow_html=True)


def render_success(message: str) -> None:
    """Render a success message."""
    st.markdown(f"""
    <div class="uicard uicard-success">
        {message}
    </div>
    """, unsafe_allow_html=True)