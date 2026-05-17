# UnderstandIQ

**Stop measuring what students get right. Start measuring whether they truly understand.**

UnderstandIQ is a metacognitive assessment engine built on research in confidence calibration
and cognitive stability. Upload any learning material. Answer questions. Discover the gap
between what you think you know — and what you actually know.

---

## The Core Insight

Traditional assessment asks: *Did you get it right?*

UnderstandIQ asks: *Do you know whether you got it right?*

That second question reveals something the first one never can: **the Illusion of Understanding** —
the gap between perceived and actual knowledge that predicts future learning failure.

This tool operationalizes research from the Human Cognition Measurement System (HCMS),
a DOI-backed cognitive science framework by Muhammad Rayan Shahid.

---

## Features

- Upload PDF, DOCX, or paste text
- AI-generated questions at surface, conceptual, and applied depth levels
- Per-question confidence capture before results are shown
- Calibration gap analysis — where confidence diverges from reality
- Overconfidence and underconfidence detection
- Natural language learning insights
- Downloadable PDF report
- UnderstandIQ Score: a composite of accuracy + calibration

---

## Quick Start

```bash
git clone https://github.com/RayanAIX/understandiq
cd understandiq
pip install -r requirements.txt
cp .env.example .env
# Add your Gemini API key to .env
streamlit run app.py
```

---

## Research Foundation

Built on HCMS — Human Cognition Measurement System
Preprint: [DOI: 10.5281/zenodo.18269740](https://doi.org/10.5281/zenodo.18269740)
Author: Muhammad Rayan Shahid

---

## Use Cases

- EdTech platforms wanting richer assessment signals
- Researchers studying metacognition and learning
- Tutors assessing student self-awareness
- Self-directed learners auditing their own understanding

---

*"Correctness is easy to fake. Understanding isn't."*