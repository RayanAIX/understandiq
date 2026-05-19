<div align="center">

# UnderstandIQ

**Stop measuring what students get right.**  
**Start measuring whether they truly understand.**

[![Live Demo](https://img.shields.io/badge/Live_Demo-understandiq.streamlit.app-7c6fff?style=for-the-badge)](https://understandiq.streamlit.app)
[![Research](https://img.shields.io/badge/Research-DOI_10.5281/zenodo.18269740-00d4aa?style=for-the-badge)](https://doi.org/10.5281/zenodo.18269740)
[![Python](https://img.shields.io/badge/Python-3.9+-ffb347?style=for-the-badge&logo=python&logoColor=white)](https://python.org)

</div>

---

## The Problem with Traditional Assessment

Every quiz, exam, and AI tutoring tool answers one question:

> *"Did you get it right?"*

But that question is broken. A student can guess correctly. A student can recall a definition without understanding it. A student can score 80% on a test and fail when the same concept appears in a different form.

**UnderstandIQ asks a different question:**

> *"Do you know whether you got it right?"*

That second question — the metacognitive one — reveals something the first one never can: the **Illusion of Understanding**. The gap between how confident you feel and how well you actually know something is the strongest predictor of future learning failure.

---

## What UnderstandIQ Does

Upload any learning material — a research paper, lecture notes, a textbook chapter, an article. UnderstandIQ generates assessment questions at surface, conceptual, and applied depth levels.

For each question, you answer **and** rate your confidence *before* seeing the result.

The system then reveals:

- **Accuracy Score** — What percentage you got right
- **Calibration Score** — How well your confidence matched your actual performance  
- **UnderstandIQ Score** — The composite metric: you need both to score high

The result isn't a grade. It's a **cognitive fingerprint** — a precise map of where your understanding is solid, where it's brittle, and where confidence is masking a gap.

---

## The Science Behind It

UnderstandIQ operationalizes three validated cognitive science constructs:

**Confidence Calibration** — Brier scores and calibration curves have long been used in forecasting and clinical psychology. UnderstandIQ adapts them to measure learner self-assessment accuracy.

**Illusion of Understanding** — Documented extensively in Dunning-Kruger research and Bjork's work on desirable difficulties. High confidence + wrong answer = the most dangerous cognitive state in learning.

**Cognitive Stability** — From the HCMS framework: consistency of reasoning across repeated and varied exposures to the same concept.

> **Research Foundation:** Built on the Human Cognition Measurement System (HCMS)  
> Preprint: [DOI: 10.5281/zenodo.18269740](https://doi.org/10.5281/zenodo.18269740)  
> *Muhammad Rayan Shahid — Independent AI Researcher, ByteBrilliance AI*

---

## Features

| Feature | Description |
|--------|-------------|
| 📄 Document Upload | PDF, DOCX, or raw text paste |
| 🧠 AI Question Generation | Surface, conceptual, and applied depth via Groq LLaMA |
| 📊 Confidence Capture | Per-question rating before results are shown |
| 🎯 Calibration Analysis | Gap chart visualizing confidence vs. correctness per question |
| 💡 Insight Engine | Rule-based cognitive pattern detection |
| 📋 PDF Report | Full downloadable assessment report |
| ⬇ Zero Setup | Deployed and live — no installation needed |

---

## UnderstandIQ Score Levels

| Score | Level | What It Means |
|-------|-------|---------------|
| 85–100 | **Calibrated Mastery** | High accuracy + well-calibrated confidence |
| 70–84 | **Solid Understanding** | Good accuracy, minor calibration gaps |
| 55–69 | **Surface Knowledge** | Moderate accuracy but overconfidence detected |
| 40–54 | **Knowledge Illusion** | Significant gap between confidence and performance |
| 0–39 | **Foundational Gap** | Low accuracy with overconfidence — highest-risk state |

---

## Quick Start (Local)

```bash
git clone https://github.com/RayanAIX/understandiq
cd understandiq
pip install -r requirements.txt
cp .env.example .env
# Add your Groq API key to .env
streamlit run app.py
```

Get a free Groq API key at [console.groq.com](https://console.groq.com) — generous free tier, extremely fast inference.

---

## Project Structure

```
understandiq/
├── app.py                      # Main Streamlit application
├── core/
│   ├── document_parser.py      # PDF, DOCX, text extraction
│   ├── question_generator.py   # Groq API question generation + JSON validation
│   ├── scoring_engine.py       # Calibration math and UnderstandIQ scoring
│   └── insight_generator.py    # Rule-based cognitive pattern insights
├── ui/
│   ├── styles.py               # Dark research-lab CSS theme
│   └── components.py           # Reusable UI components
├── requirements.txt
└── .env.example
```

---

## Use Cases

**EdTech Platforms** — Add calibration scoring to any existing quiz system to surface metacognitive data.

**Independent Learners** — Audit your own understanding before exams or presentations.

**Tutors and Educators** — Identify students who are overconfident in weak areas before it becomes a problem.

**Cognitive Science Research** — Collect confidence-accuracy data at scale for metacognition studies.

**AI Assessment Systems** — Use as a reference implementation for calibration-aware evaluation.

---

## Technical Stack

- **Frontend:** Streamlit (Python)
- **AI:** Groq API (LLaMA 3.3 70B) for question generation
- **Document Parsing:** pdfplumber, python-docx
- **Visualization:** Plotly (dark theme)
- **PDF Export:** fpdf2 (in-memory, no disk write)
- **Deployment:** Streamlit Community Cloud

---

## The Scoring Math

```python
# Convert confidence (1-5 scale) to percentage
conf_pct = ((confidence - 1) / 4) * 100

# Calibration gap per question
gap = abs(conf_pct - (100 if correct else 0))

# Calibration score
calibration = 100 - mean(all gaps)

# UnderstandIQ composite
understandiq = (accuracy * 0.5) + (calibration * 0.5)
```

Overconfidence detected when: `confidence ≥ 4` AND `incorrect`  
Underconfidence detected when: `confidence ≤ 2` AND `correct`

---

## Author

**Muhammad Rayan Shahid**  
Independent AI Researcher · Founder, ByteBrilliance AI  
[Website](https://muhammadrayanshahid.vercel.app) · [GitHub](https://github.com/RayanAIX) · [LinkedIn](https://linkedin.com/in/muhammadrayanshahid)

---

<div align="center">

*"Correctness is easy to fake. Understanding isn't."*

</div>
