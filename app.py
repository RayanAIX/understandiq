"""UnderstandIQ - Metacognitive Assessment Engine"""

import os
import json
import streamlit as st
from datetime import datetime
from fpdf import FPDF

from dotenv import load_dotenv
load_dotenv()

from core.document_parser import extract_text_from_file, extract_text_from_textarea
from core.question_generator import generate_questions
from core.scoring_engine import (
    calculate_accuracy_score,
    calculate_calibration_score,
    calculate_understandiq_score,
    get_level_name,
    get_calibration_status
)
from core.insight_generator import generate_insights, generate_recommendations
from ui.styles import get_theme_css
from ui.components import (
    render_verdict_card,
    render_metric_card,
    render_insight_card,
    render_recommendation_card,
    render_breakdown_row,
    render_error,
    render_success,
    render_progress_bar
)

st.set_page_config(
    page_title="UnderstandIQ",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown(get_theme_css(), unsafe_allow_html=True)


def init_session_state():
    """Initialize all session state variables."""
    defaults = {
        'stage': 'upload',
        'questions': [],
        'current_q': 0,
        'answers': [],
        'document_text': '',
        'filename': '',
        'word_count': 0,
        'reading_time': 0,
        'num_questions': 8,
        'depth': 'mixed',
        'results': None
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_quiz():
    """Reset quiz state for new attempt."""
    st.session_state.questions = []
    st.session_state.current_q = 0
    st.session_state.answers = []
    st.session_state.results = None
    st.session_state.stage = 'upload'


def show_upload_stage():
    """Stage 1: Upload and configure."""
    st.markdown("""
    <div style="text-align: center; margin-bottom: 40px;">
        <h1 style="font-size: 42px; margin-bottom: 8px;">UnderstandIQ</h1>
        <p style="color: var(--text-secondary); font-size: 18px;">
            Discover the gap between what you think you know — and what you actually know.
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="upload-container">', unsafe_allow_html=True)

        col1, col2 = st.columns([1, 1])

        with col1:
            uploaded_file = st.file_uploader(
                "Upload your learning material",
                type=['pdf', 'txt', 'docx'],
                help="Upload PDF, DOCX, or text file"
            )

        with col2:
            raw_text = st.text_area(
                "Or paste text directly",
                height=100,
                placeholder="Paste your notes, article, or study material here..."
            )

        if uploaded_file or raw_text:
            text = ""
            filename = ""

            if uploaded_file:
                text, filename, word_count, reading_time = extract_text_from_file(uploaded_file)
            else:
                text, filename, word_count, reading_time = extract_text_from_textarea(raw_text)

            if text:
                st.session_state.document_text = text
                st.session_state.filename = filename
                st.session_state.word_count = word_count
                st.session_state.reading_time = reading_time

                st.markdown(f"""
                <div class="uicard uicard-success">
                    <strong>{filename}</strong><br>
                    {word_count:,} words · ~{reading_time} min read
                </div>
                """, unsafe_allow_html=True)

                st.markdown("### Configure Assessment")

                col1, col2 = st.columns(2)

                with col1:
                    num_q = st.selectbox(
                        "Number of Questions",
                        [5, 8, 10],
                        index=1,
                        help="More questions provide better assessment"
                    )
                    st.session_state.num_questions = num_q

                with col2:
                    depth = st.selectbox(
                        "Question Depth",
                        ["mixed", "surface", "conceptual", "applied"],
                        index=0,
                        help="Surface: recall, Conceptual: understanding, Applied: transfer"
                    )
                    st.session_state.depth = depth

                st.markdown("---")

                if st.button("Generate Assessment", use_container_width=True):
                    generate_assessment()


def generate_assessment():
    """Generate questions using Gemini API."""
    with st.spinner("Analyzing your document and generating questions..."):
        try:
            questions = generate_questions(
                st.session_state.document_text,
                st.session_state.num_questions,
                st.session_state.depth
            )

            if not questions:
                render_error("No questions generated. Please try again.")
                return

            st.session_state.questions = questions
            st.session_state.current_q = 0
            st.session_state.answers = []
            st.session_state.stage = 'quiz'
            st.rerun()

        except Exception as e:
            render_error(f"Failed to generate questions: {str(e)}")


def show_quiz_stage():
    """Stage 2: Quiz flow."""
    if not st.session_state.questions:
        st.session_state.stage = 'upload'
        st.rerun()
        return

    questions = st.session_state.questions
    current = st.session_state.current_q

    render_progress_bar(current + 1, len(questions))

    q = questions[current]

    st.markdown(f"""
    <div class="question-card">
        <div class="question-number">Question {current + 1} of {len(questions)}</div>
        <div class="question-text">{q['question_text']}</div>
    </div>
    """, unsafe_allow_html=True)

    selected_option = None
    options = q.get('options', [])

    if options:
        for i, opt in enumerate(options):
            label = f"**{chr(65 + i)}.** {opt[3:] if opt.startswith(('A.', 'B.', 'C.', 'D.')) else opt}"
            if st.button(label, key=f"option_{i}", use_container_width=True):
                selected_option = opt
    else:
        st.info("This is a conceptual question. Select your answer below.")
        answer_input = st.text_input("Your answer:", key=f"text_answer_{current}")
        if answer_input:
            selected_option = answer_input

    st.markdown('<div class="confidence-section">', unsafe_allow_html=True)
    st.markdown('<div class="confidence-label">How confident are you in your answer?</div>', unsafe_allow_html=True)

    confidence_options = [
        "1 — Just guessing",
        "2 — Somewhat unsure",
        "3 — Neutral",
        "4 — Fairly confident",
        "5 — Completely certain"
    ]
    selected_conf = st.select_slider(
        "Confidence Level",
        options=confidence_options,
        value="3 — Neutral",
        key=f"confidence_{current}"
    )
    confidence_value = confidence_options.index(selected_conf) + 1

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    col1, col2 = st.columns([1, 1])

    with col1:
        if current > 0 and st.button("← Previous", use_container_width=True):
            st.session_state.current_q -= 1
            st.rerun()

    with col2:
        can_proceed = selected_option is not None
        next_label = "Finish Assessment" if current == len(questions) - 1 else "Next Question →"

        if st.button(next_label, disabled=not can_proceed, use_container_width=True):
            is_correct = selected_option == q.get('correct_answer', '')

            answer_record = {
                'question_text': q.get('question_text', ''),
                'selected_answer': selected_option,
                'correct_answer': q.get('correct_answer', ''),
                'confidence_rating': confidence_value,
                'topic_tag': q.get('topic_tag', 'Unknown'),
                'difficulty': q.get('difficulty', 'surface'),
                'is_correct': is_correct,
                'calibration_status': get_calibration_status({
                    'confidence_rating': confidence_value,
                    'is_correct': is_correct
                })
            }

            st.session_state.answers.append(answer_record)

            if current < len(questions) - 1:
                st.session_state.current_q += 1
                st.rerun()
            else:
                calculate_results()


def calculate_results():
    """Calculate all results and move to results stage."""
    answers = st.session_state.answers
    questions = st.session_state.questions

    accuracy = calculate_accuracy_score(answers)
    calibration = calculate_calibration_score(answers)
    understandiq_score = calculate_understandiq_score(accuracy, calibration)

    level_name, level_description = get_level_name(understandiq_score)

    insights = generate_insights(answers, accuracy, calibration, understandiq_score)
    recommendations = generate_recommendations(answers, accuracy, calibration, insights)

    st.session_state.results = {
        'accuracy': accuracy,
        'calibration': calibration,
        'understandiq_score': understandiq_score,
        'level_name': level_name,
        'level_description': level_description,
        'insights': insights,
        'recommendations': recommendations,
        'answers': answers,
        'filename': st.session_state.filename,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    st.session_state.stage = 'results'
    st.rerun()


def show_results_stage():
    """Stage 4: Results dashboard."""
    results = st.session_state.results

    if not results:
        st.session_state.stage = 'upload'
        st.rerun()
        return

    st.markdown("### Your Assessment Results")

    render_verdict_card(
        results['understandiq_score'],
        results['level_name'],
        results['level_description']
    )

    st.markdown("### Key Metrics")

    col1, col2, col3 = st.columns(3)

    with col1:
        render_metric_card("Accuracy", f"{results['accuracy']:.0f}%", color="success")

    with col2:
        render_metric_card("Calibration", f"{results['calibration']:.0f}%", color="warning")

    with col3:
        render_metric_card("UnderstandIQ", f"{results['understandiq_score']:.0f}", color="primary")

    st.markdown("---")
    st.markdown("### Calibration Gap Analysis")

    import plotly.graph_objects as go
    import numpy as np

    answers = results['answers']
    question_nums = list(range(1, len(answers) + 1))

    confidences = [a['confidence_rating'] * 20 for a in answers]
    correctness = [100 if a['is_correct'] else 0 for a in answers]

    colors_conf = ['#6C63FF' if c > 0 else '#3a3a4a' for c in confidences]
    colors_corr = ['#00D4AA' if c == 100 else '#FF6B6B' for c in correctness]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=[x - 0.2 for x in question_nums],
        y=confidences,
        name='Confidence',
        marker_color='#6C63FF',
        width=0.35
    ))

    fig.add_trace(go.Bar(
        x=[x + 0.2 for x in question_nums],
        y=correctness,
        name='Correctness',
        marker_color=['#00D4AA' if c else '#FF6B6B' for c in correctness],
        width=0.35
    ))

    fig.update_layout(
        template='plotly_dark',
        plot_bgcolor='#111118',
        paper_bgcolor='#111118',
        xaxis=dict(
            title='Question Number',
            tickmode='linear',
            tick0=1,
            dtick=1,
            gridcolor='#1E1E2E'
        ),
        yaxis=dict(
            title='Score (%)',
            range=[0, 100],
            gridcolor='#1E1E2E'
        ),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='center',
            x=0.5
        ),
        margin=dict(t=60, b=40, l=60, r=40),
        height=350
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.markdown("### Question Breakdown")

    for i, answer in enumerate(answers):
        render_breakdown_row(answer, i)

    st.markdown("---")
    st.markdown("### Learning Insights")

    for insight in results['insights']:
        render_insight_card(insight)

    st.markdown("---")
    st.markdown("### Recommended Actions")

    for rec in results['recommendations']:
        render_recommendation_card(rec)

    st.markdown("---")

    if st.button("Download PDF Report", use_container_width=True):
        pdf = generate_pdf_report(results)
        pdf_path = os.path.join(os.getcwd(), 'understandiq_report.pdf')
        pdf.output(pdf_path)

        with open(pdf_path, 'rb') as f:
            st.download_button(
                label="Download Report",
                data=f,
                file_name='UnderstandIQ_Report.pdf',
                mime='application/pdf',
                use_container_width=True
            )

    st.markdown("---")

    if st.button("Start New Assessment", use_container_width=True):
        reset_quiz()


def generate_pdf_report(results: dict) -> FPDF:
    """Generate PDF report."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font('Arial', 'B', 24)
    pdf.set_text_color(108, 99, 255)
    pdf.cell(0, 20, 'UnderstandIQ Report', 0, 1, 'C')
    pdf.ln(5)

    pdf.set_font('Arial', '', 10)
    pdf.set_text_color(136, 136, 170)
    pdf.cell(0, 10, f"Document: {results['filename']}", 0, 1)
    pdf.cell(0, 10, f"Date: {results['timestamp']}", 0, 1)
    pdf.ln(10)

    pdf.set_font('Arial', 'B', 16)
    pdf.set_text_color(232, 232, 240)
    pdf.cell(0, 12, f"UnderstandIQ Score: {results['understandiq_score']:.0f}", 0, 1)
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f"Level: {results['level_name']}", 0, 1)
    pdf.cell(0, 10, f"Description: {results['level_description']}", 0, 1)
    pdf.ln(10)

    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 12, "Metrics", 0, 1)
    pdf.set_font('Arial', '', 11)
    pdf.set_text_color(232, 232, 240)
    pdf.cell(0, 8, f"Accuracy Score: {results['accuracy']:.1f}%", 0, 1)
    pdf.cell(0, 8, f"Calibration Score: {results['calibration']:.1f}%", 0, 1)
    pdf.ln(10)

    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 12, "Question Breakdown", 0, 1)
    pdf.set_font('Arial', '', 9)

    for i, answer in enumerate(results['answers'], 1):
        q_text = answer['question_text'][:50] + '...' if len(answer['question_text']) > 50 else answer['question_text']
        status = "✓" if answer['is_correct'] else "✗"
        pdf.cell(0, 7, f"Q{i}: {q_text} | {answer['topic_tag']} | {status} | Conf: {answer['confidence_rating']}/5", 0, 1)

    pdf.ln(10)

    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 12, "Insights", 0, 1)
    pdf.set_font('Arial', '', 10)
    for insight in results['insights']:
        pdf.multi_cell(0, 7, f"• {insight}")
        pdf.ln(3)

    pdf.ln(10)

    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 12, "Recommendations", 0, 1)
    pdf.set_font('Arial', '', 10)
    for rec in results['recommendations']:
        pdf.multi_cell(0, 7, f"• {rec}")
        pdf.ln(3)

    return pdf


def main():
    """Main application entry point."""
    init_session_state()

    if st.session_state.stage == 'upload':
        show_upload_stage()
    elif st.session_state.stage == 'quiz':
        show_quiz_stage()
    elif st.session_state.stage == 'results':
        show_results_stage()


if __name__ == "__main__":
    main()