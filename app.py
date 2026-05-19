"""
UnderstandIQ — Metacognitive Assessment Engine
Author: Muhammad Rayan Shahid | ByteBrilliance AI
Research: HCMS — DOI: 10.5281/zenodo.18269740
"""

import os
import io
import json
import streamlit as st
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

from core.document_parser import extract_text_from_file, extract_text_from_textarea
from core.question_generator import generate_questions
from core.scoring_engine import (
    calculate_accuracy_score,
    calculate_calibration_score,
    calculate_understandiq_score,
    get_level_name,
    get_calibration_status,
)
from core.insight_generator import generate_insights, generate_recommendations
from ui.styles import get_theme_css
from ui.components import (
    render_header,
    render_verdict_card,
    render_metric_cards,
    render_progress_bar,
    render_breakdown_table,
    render_insights,
    render_recommendations,
    render_info,
    render_success_msg,
    render_error,
    render_section,
)

# ─── Page Config ──────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="UnderstandIQ",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed",
)
st.markdown(get_theme_css(), unsafe_allow_html=True)

# ─── Session State Init ────────────────────────────────────────────────────────

def init():
    defaults = {
        "stage": "upload",          # upload | quiz | results
        "questions": [],
        "current_q": 0,
        "answers": [],              # finalized answers list
        "pending_answer": None,     # answer selected for current question (not yet committed)
        "document_text": "",
        "filename": "",
        "word_count": 0,
        "reading_time": 0,
        "num_questions": 8,
        "depth": "mixed",
        "results": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init()

# ─── Helpers ──────────────────────────────────────────────────────────────────

def reset():
    keys_to_clear = [
        "questions", "current_q", "answers", "pending_answer",
        "document_text", "filename", "word_count", "reading_time",
        "results", "stage"
    ]
    for k in keys_to_clear:
        if k in st.session_state:
            del st.session_state[k]
    st.rerun()


def go_to_stage(stage: str):
    st.session_state.stage = stage
    st.rerun()

# ─── Stage 1: Upload ──────────────────────────────────────────────────────────

def show_upload():
    render_header()

    render_info(
        "Upload any PDF, DOCX, or text — lecture notes, research papers, articles, study guides. "
        "UnderstandIQ will test not just whether you answer correctly, but whether your confidence matches reality."
    )

    col1, col2 = st.columns([1, 1])
    with col1:
        uploaded_file = st.file_uploader(
            "Upload document",
            type=["pdf", "txt", "docx"],
            label_visibility="collapsed",
        )
    with col2:
        raw_text = st.text_area(
            "Or paste text",
            height=120,
            placeholder="Paste notes, article, or study material here…",
            label_visibility="collapsed",
        )

    text, filename, word_count, reading_time = "", "", 0, 0

    if uploaded_file:
        text, filename, word_count, reading_time = extract_text_from_file(uploaded_file)
    elif raw_text.strip():
        text, filename, word_count, reading_time = extract_text_from_textarea(raw_text)

    if text:
        render_success_msg(f"{filename} · {word_count:,} words · ~{reading_time} min read")
        st.session_state.document_text = text
        st.session_state.filename = filename
        st.session_state.word_count = word_count
        st.session_state.reading_time = reading_time

        render_section("Configure Assessment")
        col1, col2 = st.columns(2)
        with col1:
            num_q = st.selectbox(
                "Number of questions",
                [5, 8, 10],
                index=1,
                help="More questions = more precise calibration data."
            )
        with col2:
            depth = st.selectbox(
                "Question depth",
                ["mixed", "surface", "conceptual", "applied"],
                format_func=lambda x: {
                    "mixed": "Mixed (Recommended)",
                    "surface": "Surface — Recall",
                    "conceptual": "Conceptual — Understanding",
                    "applied": "Applied — Transfer",
                }[x],
                index=0,
            )
        st.session_state.num_questions = num_q
        st.session_state.depth = depth

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Generate Assessment →", use_container_width=True):
            if len(text.split()) < 50:
                render_error("Please provide at least 50 words of content for a meaningful assessment.")
            else:
                with st.spinner("Analyzing your document and generating questions…"):
                    try:
                        questions = generate_questions(
                            st.session_state.document_text,
                            st.session_state.num_questions,
                            st.session_state.depth,
                        )
                        if not questions:
                            render_error("Could not generate questions. Please check your API key or try different content.")
                        else:
                            st.session_state.questions = questions
                            st.session_state.current_q = 0
                            st.session_state.answers = []
                            st.session_state.pending_answer = None
                            st.session_state.stage = "quiz"
                            st.rerun()
                    except Exception as e:
                        render_error(f"Error generating questions: {str(e)}")
    else:
        if uploaded_file or raw_text.strip():
            render_error("Could not extract text from this file. Try a different format or paste text directly.")

# ─── Stage 2: Quiz ────────────────────────────────────────────────────────────
#
# ROOT BUG FIX EXPLANATION:
# The original code used st.button() for options inside a loop. st.button() returns
# True only on the rerun immediately triggered by the click, but Streamlit reruns the
# entire script — so by the time "Next Question" is processed, the option button state
# is gone and selected_option is always None → all answers marked wrong.
#
# FIX: Use st.radio() for option selection, which stores state across reruns properly.
# We also use st.session_state.pending_answer to hold the selected option until
# the user clicks "Next", then we commit it. This is the correct Streamlit pattern.

def show_quiz():
    questions = st.session_state.questions
    if not questions:
        go_to_stage("upload")
        return

    current = st.session_state.current_q
    total = len(questions)
    q = questions[current]

    render_progress_bar(current + 1, total)

    # Question display
    st.markdown(f"""
    <div class="question-card">
        <div class="question-number">Question {current + 1} of {total} · {q.get('difficulty', 'surface').title()} · {q.get('topic_tag', '')}</div>
        <div class="question-text">{q['question_text']}</div>
    </div>
    """, unsafe_allow_html=True)

    options = q.get("options", [])

    # ── Answer selection via st.radio (state persists across reruns) ──────────
    # Key includes current_q to reset when moving to next question
    radio_key = f"radio_q{current}"

    if options:
        selected = st.radio(
            "Select your answer:",
            options,
            key=radio_key,
            index=None,          # No default selection — user must actively choose
            label_visibility="collapsed",
        )
    else:
        selected = st.text_input(
            "Your answer:",
            key=f"text_q{current}",
            placeholder="Type your answer here…",
        )
        selected = selected.strip() if selected else None

    # ── Confidence slider ─────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="confidence-label">Rate your confidence before seeing the result</div>', unsafe_allow_html=True)

    confidence_labels = [
        "1 — Just guessing",
        "2 — Somewhat unsure",
        "3 — Neutral",
        "4 — Fairly confident",
        "5 — Completely certain",
    ]
    conf_selection = st.select_slider(
        "Confidence",
        options=confidence_labels,
        value="3 — Neutral",
        key=f"conf_q{current}",
        label_visibility="collapsed",
    )
    confidence_value = confidence_labels.index(conf_selection) + 1  # 1-5

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Navigation ────────────────────────────────────────────────────────────
    col1, col2 = st.columns([1, 2])

    with col1:
        if current > 0:
            if st.button("← Back", use_container_width=True):
                # Remove last committed answer to allow re-answering previous question
                if st.session_state.answers:
                    st.session_state.answers.pop()
                st.session_state.current_q -= 1
                st.rerun()

    with col2:
        is_last = current == total - 1
        btn_label = "Finish & See Results →" if is_last else "Next Question →"
        can_proceed = selected is not None and selected != ""

        if st.button(btn_label, disabled=not can_proceed, use_container_width=True):
            # ── Correctness check ─────────────────────────────────────────────
            correct_answer = q.get("correct_answer", "")
            is_correct = _check_correct(selected, correct_answer)

            answer_record = {
                "question_text": q.get("question_text", ""),
                "selected_answer": selected,
                "correct_answer": correct_answer,
                "confidence_rating": confidence_value,
                "topic_tag": q.get("topic_tag", "General"),
                "difficulty": q.get("difficulty", "surface"),
                "is_correct": is_correct,
                "calibration_status": get_calibration_status({
                    "confidence_rating": confidence_value,
                    "is_correct": is_correct,
                }),
            }
            st.session_state.answers.append(answer_record)

            if is_last:
                _calculate_results()
            else:
                st.session_state.current_q += 1
                st.rerun()

    if not can_proceed:
        st.markdown(
            '<div style="text-align:center; font-size:12px; color: var(--text-muted); margin-top:0.5rem;">Select an answer to continue</div>',
            unsafe_allow_html=True
        )


def _check_correct(selected: str, correct: str) -> bool:
    """
    Robust correctness check.
    Handles: exact match, case differences, option letter prefix variations.
    """
    if not selected or not correct:
        return False

    s = selected.strip().lower()
    c = correct.strip().lower()

    # Exact match
    if s == c:
        return True

    # Strip option prefix (A., B., etc.) and compare text
    def strip_prefix(text):
        if len(text) >= 3 and text[1] in ".)" and text[0].isalpha():
            return text[2:].strip()
        return text

    return strip_prefix(s) == strip_prefix(c)


def _calculate_results():
    answers = st.session_state.answers
    accuracy = calculate_accuracy_score(answers)
    calibration = calculate_calibration_score(answers)
    uiq = calculate_understandiq_score(accuracy, calibration)
    level_name, level_desc = get_level_name(uiq)
    insights = generate_insights(answers, accuracy, calibration, uiq)
    recs = generate_recommendations(answers, accuracy, calibration, insights)

    st.session_state.results = {
        "accuracy": accuracy,
        "calibration": calibration,
        "understandiq_score": uiq,
        "level_name": level_name,
        "level_description": level_desc,
        "insights": insights,
        "recommendations": recs,
        "answers": answers,
        "filename": st.session_state.filename,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    st.session_state.stage = "results"
    st.rerun()

# ─── Stage 3: Results ─────────────────────────────────────────────────────────

def show_results():
    results = st.session_state.results
    if not results:
        go_to_stage("upload")
        return

    # Header
    st.markdown("""
    <div style="text-align:center; margin-bottom: 2rem;">
        <div style="font-family: DM Mono, monospace; font-size:11px; text-transform:uppercase;
             letter-spacing:0.1em; color: var(--text-muted); margin-bottom:0.5rem;">Assessment Complete</div>
        <div style="font-size:28px; font-weight:700; color:var(--text);">Your Cognitive Profile</div>
    </div>
    """, unsafe_allow_html=True)

    # Verdict
    render_verdict_card(
        results["understandiq_score"],
        results["level_name"],
        results["level_description"],
    )

    # Metrics
    render_metric_cards(
        results["accuracy"],
        results["calibration"],
        results["understandiq_score"],
    )

    # Calibration chart
    render_section("Calibration Gap Analysis")
    _render_chart(results["answers"])

    st.markdown("<br>", unsafe_allow_html=True)

    # Breakdown
    render_breakdown_table(results["answers"])

    st.markdown("<br>", unsafe_allow_html=True)

    # Insights
    render_insights(results["insights"])

    st.markdown("<br>", unsafe_allow_html=True)

    # Recommendations
    render_recommendations(results["recommendations"])

    st.markdown("---")

    # PDF download
    render_section("Export")
    pdf_bytes = _generate_pdf(results)
    st.download_button(
        label="⬇ Download PDF Report",
        data=pdf_bytes,
        file_name=f"UnderstandIQ_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
        mime="application/pdf",
        use_container_width=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Start New Assessment", use_container_width=True):
        reset()


def _render_chart(answers: list):
    import plotly.graph_objects as go

    q_nums = list(range(1, len(answers) + 1))
    confidences = [((a["confidence_rating"] - 1) / 4) * 100 for a in answers]
    correctness = [100 if a["is_correct"] else 0 for a in answers]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=[x - 0.2 for x in q_nums],
        y=confidences,
        name="Confidence",
        marker_color="#7c6fff",
        width=0.35,
        hovertemplate="Q%{x:.0f}<br>Confidence: %{y:.0f}%<extra></extra>",
    ))

    fig.add_trace(go.Bar(
        x=[x + 0.2 for x in q_nums],
        y=correctness,
        name="Correctness",
        marker_color=["#00d4aa" if c else "#ff6b6b" for c in correctness],
        width=0.35,
        hovertemplate="Q%{x:.0f}<br>Correct: %{y:.0f}%<extra></extra>",
    ))

    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor="#111118",
        paper_bgcolor="#111118",
        font=dict(family="Outfit, sans-serif", color="#8888aa", size=12),
        xaxis=dict(
            title="Question",
            tickmode="linear",
            tick0=1,
            dtick=1,
            gridcolor="#1e1e30",
            zeroline=False,
        ),
        yaxis=dict(
            title="Score (%)",
            range=[0, 108],
            gridcolor="#1e1e30",
            zeroline=False,
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        margin=dict(t=50, b=40, l=50, r=20),
        height=300,
        bargap=0.15,
    )

    # Add gap annotation
    for i, (conf, corr) in enumerate(zip(confidences, correctness)):
        gap = abs(conf - corr)
        if gap >= 50:
            fig.add_annotation(
                x=i + 1,
                y=max(conf, corr) + 6,
                text=f"⚠ {gap:.0f}pt gap",
                showarrow=False,
                font=dict(size=9, color="#ffb347"),
            )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def _generate_pdf(results: dict) -> bytes:
    """Generate PDF report as bytes (works on Streamlit Cloud — no disk write)."""
    from fpdf import FPDF

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Title
    pdf.set_font("Arial", "B", 22)
    pdf.set_text_color(124, 111, 255)
    pdf.cell(0, 14, "UnderstandIQ Report", ln=True, align="C")

    pdf.set_font("Arial", "", 9)
    pdf.set_text_color(136, 136, 170)
    pdf.cell(0, 6, f"Document: {results['filename']}", ln=True, align="C")
    pdf.cell(0, 6, f"Generated: {results['timestamp']}", ln=True, align="C")
    pdf.ln(8)

    # Score block
    pdf.set_fill_color(20, 20, 30)
    pdf.set_draw_color(124, 111, 255)
    pdf.rect(15, pdf.get_y(), 180, 32, style="FD")
    pdf.set_font("Arial", "B", 28)
    pdf.set_text_color(124, 111, 255)
    pdf.cell(0, 18, str(int(results["understandiq_score"])), ln=True, align="C")
    pdf.set_font("Arial", "B", 13)
    pdf.set_text_color(232, 232, 240)
    pdf.cell(0, 8, results["level_name"], ln=True, align="C")
    pdf.ln(6)

    # Metrics
    pdf.set_font("Arial", "B", 11)
    pdf.set_text_color(200, 200, 220)
    pdf.cell(60, 8, f"Accuracy: {results['accuracy']:.0f}%", ln=False)
    pdf.cell(60, 8, f"Calibration: {results['calibration']:.0f}%", ln=False)
    pdf.cell(60, 8, f"UnderstandIQ: {results['understandiq_score']:.0f}", ln=True)
    pdf.ln(6)

    # Divider
    pdf.set_draw_color(40, 40, 60)
    pdf.line(15, pdf.get_y(), 195, pdf.get_y())
    pdf.ln(4)

    # Question breakdown
    pdf.set_font("Arial", "B", 12)
    pdf.set_text_color(180, 180, 220)
    pdf.cell(0, 8, "Question Breakdown", ln=True)
    pdf.ln(2)

    pdf.set_font("Arial", "", 8)
    for i, a in enumerate(results["answers"], 1):
        status = "CORRECT" if a["is_correct"] else "WRONG"
        calib = a.get("calibration_status", "")
        q = a["question_text"][:60] + ("…" if len(a["question_text"]) > 60 else "")
        pdf.set_text_color(0, 212, 170) if a["is_correct"] else pdf.set_text_color(255, 107, 107)
        pdf.cell(12, 6, f"Q{i}", ln=False)
        pdf.set_text_color(200, 200, 220)
        pdf.cell(110, 6, q, ln=False)
        pdf.cell(20, 6, status, ln=False)
        pdf.cell(18, 6, f"Conf:{a['confidence_rating']}/5", ln=False)
        pdf.cell(0, 6, calib[:14], ln=True)

    pdf.ln(6)
    pdf.line(15, pdf.get_y(), 195, pdf.get_y())
    pdf.ln(4)

    # Insights
    pdf.set_font("Arial", "B", 12)
    pdf.set_text_color(180, 180, 220)
    pdf.cell(0, 8, "Insights", ln=True)
    pdf.ln(2)
    pdf.set_font("Arial", "", 9)
    pdf.set_text_color(160, 160, 190)
    for ins in results["insights"]:
        pdf.multi_cell(0, 5, f"• {ins}")
        pdf.ln(2)

    pdf.ln(4)

    # Recommendations
    pdf.set_font("Arial", "B", 12)
    pdf.set_text_color(180, 180, 220)
    pdf.cell(0, 8, "Recommended Actions", ln=True)
    pdf.ln(2)
    pdf.set_font("Arial", "", 9)
    pdf.set_text_color(160, 160, 190)
    for rec in results["recommendations"]:
        pdf.multi_cell(0, 5, f"→ {rec}")
        pdf.ln(2)

    pdf.ln(8)

    # Footer
    pdf.set_font("Arial", "I", 8)
    pdf.set_text_color(80, 80, 110)
    pdf.cell(0, 6, "Built on HCMS Research · DOI: 10.5281/zenodo.18269740 · Muhammad Rayan Shahid", align="C")

    # Return as bytes (no disk write — works on Streamlit Cloud)
    return bytes(pdf.output())


# ─── Router ───────────────────────────────────────────────────────────────────

def main():
    stage = st.session_state.get("stage", "upload")
    if stage == "upload":
        show_upload()
    elif stage == "quiz":
        show_quiz()
    elif stage == "results":
        show_results()


if __name__ == "__main__":
    main()
