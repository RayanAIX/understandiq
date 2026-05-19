"""
UnderstandIQ — Cognitive Assessment Engine
Author: Muhammad Rayan Shahid | ByteBrilliance AI
Research: HCMS — DOI: 10.5281/zenodo.18269740

Single-file architecture for Streamlit Cloud deployment.
All logic self-contained. No external module dependencies.
"""

import os, io, json, re, textwrap
from datetime import datetime
from collections import defaultdict

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="UnderstandIQ",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════════════════════════════
# CSS — Dark research-lab aesthetic
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Outfit:wght@300;400;500;600;700&display=swap');

:root {
    --bg:       #08080e;
    --surface:  #0f0f18;
    --surface2: #14141f;
    --border:   #1c1c2e;
    --accent:   #7c6fff;
    --accent2:  #a78bfa;
    --green:    #00d4aa;
    --amber:    #ffb347;
    --red:      #ff6b6b;
    --text:     #e8e8f2;
    --muted:    #8888aa;
    --faint:    #44445a;
}

html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif !important;
    background: var(--bg) !important;
    color: var(--text) !important;
}
#MainMenu, footer, header, [data-testid="stToolbar"], .stDeployButton { display:none!important; }

.main .block-container { max-width:800px; padding:1.5rem 1.5rem 5rem; }

/* ── Header ── */
.uiq-header { text-align:center; padding:2.5rem 0 2rem; border-bottom:1px solid var(--border); margin-bottom:2.5rem; }
.uiq-logo { font-family:'Outfit',sans-serif; font-size:52px; font-weight:700; letter-spacing:-0.03em; color:var(--text); }
.uiq-logo span { color:var(--accent); }
.uiq-sub { color:var(--muted); font-size:16px; font-weight:300; margin-top:0.4rem; }
.uiq-badge {
    display:inline-block; margin-top:0.9rem;
    font-family:'DM Mono',monospace; font-size:10px; padding:3px 12px;
    border:1px solid var(--border); border-radius:100px; color:var(--faint);
}

/* ── Cards ── */
.card {
    background:var(--surface); border:1px solid var(--border);
    border-radius:14px; padding:1.5rem; margin-bottom:1rem;
}
.card-accent  { border-left:3px solid var(--accent); }
.card-green   { border-left:3px solid var(--green);  background:rgba(0,212,170,.06); }
.card-amber   { border-left:3px solid var(--amber);  background:rgba(255,179,71,.06); }
.card-red     { border-left:3px solid var(--red);    background:rgba(255,107,107,.06); }

/* ── Verdict ── */
.verdict {
    background:linear-gradient(135deg,#0f0f18,#14141f);
    border:1px solid var(--border); border-top:3px solid var(--accent);
    border-radius:18px; padding:3rem 2rem; text-align:center; margin-bottom:1.5rem;
}
.verdict-score { font-family:'DM Mono',monospace; font-size:80px; font-weight:500; color:var(--accent); line-height:1; }
.verdict-level { font-size:24px; font-weight:700; color:var(--text); margin:.3rem 0; }
.verdict-desc  { font-size:14px; color:var(--muted); max-width:520px; margin:0 auto; line-height:1.7; }
.verdict-archetype {
    display:inline-block; margin-top:1rem;
    background:rgba(124,111,255,.12); border:1px solid rgba(124,111,255,.3);
    border-radius:100px; padding:5px 18px;
    font-family:'DM Mono',monospace; font-size:12px; color:var(--accent2);
}

/* ── Metrics ── */
.metrics { display:flex; gap:.75rem; margin-bottom:1.5rem; }
.metric {
    flex:1; background:var(--surface); border:1px solid var(--border);
    border-radius:12px; padding:1.25rem; text-align:center;
}
.metric-val { font-family:'DM Mono',monospace; font-size:38px; font-weight:500; line-height:1; margin-bottom:4px; }
.metric-lbl { font-size:11px; text-transform:uppercase; letter-spacing:.08em; color:var(--faint); }
.c-accent { color:var(--accent); }
.c-green  { color:var(--green);  }
.c-amber  { color:var(--amber);  }
.c-red    { color:var(--red);    }

/* ── Question ── */
.q-card {
    background:var(--surface); border:1px solid var(--border);
    border-radius:14px; padding:2rem; margin-bottom:1.5rem;
}
.q-meta { font-family:'DM Mono',monospace; font-size:10px; text-transform:uppercase;
          letter-spacing:.1em; color:var(--faint); margin-bottom:1rem; }
.q-text { font-size:19px; font-weight:500; color:var(--text); line-height:1.65; }
.q-type-badge {
    display:inline-block; font-family:'DM Mono',monospace; font-size:10px;
    padding:2px 10px; border-radius:100px; margin-bottom:.75rem;
    background:rgba(124,111,255,.1); border:1px solid rgba(124,111,255,.2); color:var(--accent2);
}

/* ── Progress ── */
.prog-lbl { font-family:'DM Mono',monospace; font-size:11px; color:var(--faint); text-align:right; margin-bottom:4px; }
.prog-wrap { background:var(--surface2); border-radius:100px; height:3px; overflow:hidden; margin-bottom:2rem; }
.prog-fill { background:linear-gradient(90deg,var(--accent),var(--accent2)); height:100%; border-radius:100px; }

/* ── Confidence ── */
.conf-label { font-family:'DM Mono',monospace; font-size:11px; text-transform:uppercase;
              letter-spacing:.08em; color:var(--faint); margin:1.25rem 0 .5rem; }

/* ── Breakdown ── */
.bk-row {
    background:var(--surface); border:1px solid var(--border);
    border-radius:9px; padding:.9rem 1.2rem; margin-bottom:.4rem;
    display:flex; align-items:flex-start; gap:1rem;
}
.bk-correct { border-left:3px solid var(--green); }
.bk-wrong   { border-left:3px solid var(--red);   }
.bk-icon  { font-size:16px; width:22px; flex-shrink:0; padding-top:1px; }
.bk-body  { flex:1; min-width:0; }
.bk-q     { font-size:13px; color:var(--text); line-height:1.5; }
.bk-meta  { display:flex; gap:.5rem; flex-wrap:wrap; margin-top:.35rem; align-items:center; }
.bk-tag   { font-family:'DM Mono',monospace; font-size:10px; padding:1px 8px;
            border-radius:100px; background:var(--surface2); color:var(--muted); }
.bk-calib { font-size:10px; }
.calib-over  { color:var(--red);   }
.calib-under { color:var(--amber); }
.calib-good  { color:var(--green); }
.bk-answer { font-size:11px; color:var(--muted); margin-top:.2rem; }

/* ── Insight / Rec ── */
.insight { background:var(--surface); border:1px solid var(--border); border-left:3px solid var(--accent);
           border-radius:9px; padding:1.1rem 1.4rem; margin-bottom:.6rem;
           font-size:14px; color:var(--muted); line-height:1.75; }
.rec     { background:rgba(0,212,170,.05); border:1px solid var(--border); border-left:3px solid var(--green);
           border-radius:9px; padding:1.1rem 1.4rem; margin-bottom:.6rem;
           font-size:14px; color:var(--muted); line-height:1.75; }

/* ── Section header ── */
.sh { font-family:'DM Mono',monospace; font-size:11px; text-transform:uppercase;
      letter-spacing:.1em; color:var(--faint); margin:2rem 0 .9rem; }

/* ── Alerts ── */
.info-box  { background:rgba(124,111,255,.07); border:1px solid rgba(124,111,255,.2);
             border-left:3px solid var(--accent); border-radius:9px;
             padding:.9rem 1.2rem; font-size:13px; color:var(--muted); margin-bottom:1rem; }
.ok-box    { background:rgba(0,212,170,.07); border:1px solid rgba(0,212,170,.2);
             border-left:3px solid var(--green); border-radius:9px;
             padding:.75rem 1.2rem; font-size:13px; color:var(--muted); margin-bottom:1rem; }
.err-box   { background:rgba(255,107,107,.07); border:1px solid rgba(255,107,107,.2);
             border-left:3px solid var(--red); border-radius:9px;
             padding:.75rem 1.2rem; font-size:13px; color:var(--muted); margin-bottom:1rem; }

/* ── Buttons ── */
.stButton>button {
    background:var(--surface2)!important; border:1px solid var(--border)!important;
    color:var(--text)!important; border-radius:9px!important;
    font-family:'Outfit',sans-serif!important; font-size:14px!important;
    font-weight:400!important; transition:all .15s!important;
}
.stButton>button:hover {
    border-color:var(--accent)!important; background:rgba(124,111,255,.08)!important;
}
.stButton>button:disabled { opacity:.4!important; }

/* ── Radio options ── */
[data-testid="stRadio"] label {
    background:var(--surface2); border:1px solid var(--border);
    border-radius:8px; padding:.7rem 1rem; margin-bottom:.4rem;
    display:block; cursor:pointer; font-size:14px; color:var(--text);
    transition:border-color .15s;
}
[data-testid="stRadio"] label:hover { border-color:var(--accent); }
[data-testid="stRadio"] [aria-checked="true"] + label,
[data-testid="stRadio"] input:checked + div { border-color:var(--accent)!important; }

/* ── Text area, inputs ── */
textarea, [data-testid="stTextInput"] input {
    background:var(--surface)!important; border-color:var(--border)!important;
    color:var(--text)!important; border-radius:9px!important;
}
[data-testid="stFileUploader"] {
    background:var(--surface)!important; border:1px dashed var(--border)!important;
    border-radius:12px!important;
}
select, [data-testid="stSelectbox"]>div>div {
    background:var(--surface)!important; border-color:var(--border)!important; color:var(--text)!important;
}
hr { border:none!important; border-top:1px solid var(--border)!important; margin:2rem 0!important; }

/* ── Reasoning box ── */
.reasoning-prompt {
    background:rgba(124,111,255,.05); border:1px solid rgba(124,111,255,.15);
    border-radius:9px; padding:.9rem 1.2rem; margin:.5rem 0 .75rem;
    font-size:13px; color:var(--muted); line-height:1.6;
}

/* ── Cognitive archetype panel ── */
.archetype-panel {
    background:linear-gradient(135deg,rgba(124,111,255,.08),rgba(167,139,250,.04));
    border:1px solid rgba(124,111,255,.2); border-radius:14px;
    padding:1.75rem; margin:1.5rem 0;
}
.archetype-title { font-size:11px; font-family:'DM Mono',monospace; text-transform:uppercase;
                   letter-spacing:.1em; color:var(--faint); margin-bottom:.5rem; }
.archetype-name  { font-size:26px; font-weight:700; color:var(--accent2); margin-bottom:.5rem; }
.archetype-desc  { font-size:14px; color:var(--muted); line-height:1.7; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════

def _init():
    defaults = {
        "stage":         "upload",   # upload | quiz | results
        "questions":     [],
        "current_q":     0,
        "answers":       [],
        "doc_text":      "",
        "filename":      "",
        "word_count":    0,
        "num_q":         8,
        "depth":         "mixed",
        "results":       None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init()


def _reset():
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# DOCUMENT PARSING
# ══════════════════════════════════════════════════════════════════════════════

def parse_document(uploaded_file=None, raw_text=""):
    if uploaded_file:
        name = uploaded_file.name
        ext  = name.lower().split(".")[-1]
        try:
            if ext == "pdf":
                import pdfplumber
                with pdfplumber.open(io.BytesIO(uploaded_file.read())) as pdf:
                    text = "\n".join(p.extract_text() or "" for p in pdf.pages)
            elif ext == "docx":
                from docx import Document
                doc  = Document(io.BytesIO(uploaded_file.read()))
                text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
            else:
                text = uploaded_file.read().decode("utf-8", errors="ignore")
        except Exception as e:
            return "", name, 0
        text = text.strip()
        return text, name, len(text.split())
    elif raw_text.strip():
        text = raw_text.strip()
        return text, "Pasted Text", len(text.split())
    return "", "", 0


# ══════════════════════════════════════════════════════════════════════════════
# QUESTION GENERATION — 4 types, strict JSON
# ══════════════════════════════════════════════════════════════════════════════

QUESTION_PROMPT = """\
You are an expert in cognitive science and educational assessment.
Generate exactly {n} questions from the text below.
Use EXACTLY this distribution of types:
  - {n_mcq} MCQ questions  (type: "mcq")
  - {n_sa}  Short-answer   (type: "short_answer")
  - {n_app} Application    (type: "application")
  - {n_eli} Explain-it     (type: "explain")

Depth: {depth_instruction}

STRICT RULES:
1. MCQ: 4 options formatted "A. text", "B. text", "C. text", "D. text".
   correct_answer MUST be copied EXACTLY from one option string.
2. Short-answer: a factual question with a concise correct answer (1 sentence max).
3. Application: "How would [concept] apply if..." — tests transfer thinking. correct_answer is a model answer.
4. Explain-it: "Explain [concept] as simply as possible" — tests depth. correct_answer is key points to cover.
5. topic_tag: ONE word from the content domain.
6. difficulty: "surface" | "conceptual" | "applied"

Return ONLY valid JSON — no markdown, no preamble:
{{
  "questions": [
    {{
      "question_text": "...",
      "question_type": "mcq|short_answer|application|explain",
      "options": ["A. ...", "B. ...", "C. ...", "D. ..."] or null,
      "correct_answer": "...",
      "topic_tag": "...",
      "difficulty": "surface|conceptual|applied",
      "scoring_criteria": "Brief note on what a good answer covers (for non-MCQ)"
    }}
  ]
}}

TEXT:
{text}"""


def _groq(messages: list, temperature=0.35, max_tokens=4000) -> str:
    from groq import Groq
    key = os.getenv("GROQ_API_KEY", "")
    if not key:
        raise ValueError("GROQ_API_KEY not set. Add it in Streamlit Cloud Secrets.")
    client = Groq(api_key=key)
    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return resp.choices[0].message.content.strip()


def generate_questions(text: str, n: int, depth: str) -> list:
    # Trim text to avoid token overflow
    text = text[:7000] if len(text) > 7000 else text

    depth_map = {
        "mixed":      "Mix all depths: 40% surface, 40% conceptual, 20% applied.",
        "surface":    "All questions test recall of specific facts and definitions.",
        "conceptual": "All questions test 'why' and 'how', not just 'what'.",
        "applied":    "All questions test transfer — applying concepts in new situations.",
    }

    # Question type distribution
    n_mcq = max(1, round(n * 0.45))
    n_sa  = max(1, round(n * 0.25))
    n_app = max(1, round(n * 0.15))
    n_eli = n - n_mcq - n_sa - n_app
    n_eli = max(1, n_eli)

    prompt = QUESTION_PROMPT.format(
        n=n, n_mcq=n_mcq, n_sa=n_sa, n_app=n_app, n_eli=n_eli,
        depth_instruction=depth_map.get(depth, depth_map["mixed"]),
        text=text,
    )

    raw = _groq([
        {"role": "system", "content": "You are an expert assessment designer. Return only valid JSON."},
        {"role": "user",   "content": prompt},
    ])

    return _parse_questions(raw)


def _parse_questions(raw: str) -> list:
    # Strip markdown fences
    raw = re.sub(r"```json\s*", "", raw)
    raw = re.sub(r"```\s*",     "", raw)
    raw = raw.strip()

    # Try direct parse
    for attempt in [raw, re.search(r'\{.*\}', raw, re.DOTALL)]:
        try:
            blob = attempt if isinstance(attempt, str) else (attempt.group() if attempt else None)
            if not blob:
                continue
            data = json.loads(blob)
            qs   = data.get("questions", [])
            if qs:
                return [_validate_q(q) for q in qs if _validate_q(q)]
        except Exception:
            continue
    return []


def _validate_q(q: dict) -> dict | None:
    try:
        qtype   = q.get("question_type", "mcq")
        options = q.get("options") or []
        correct = q.get("correct_answer", "").strip()
        text    = q.get("question_text", "").strip()
        if not text:
            return None

        # For MCQ — make sure correct_answer exactly matches an option
        if qtype == "mcq" and options:
            if correct not in options:
                # Try substring match
                for opt in options:
                    if correct.lower() in opt.lower() or opt.lower().startswith(correct.lower().rstrip(".") + "."):
                        correct = opt
                        break
                else:
                    correct = options[0]  # fallback

        return {
            "question_text":   text,
            "question_type":   qtype,
            "options":         options if options else None,
            "correct_answer":  correct,
            "topic_tag":       q.get("topic_tag",       "General").strip(),
            "difficulty":      q.get("difficulty",      "surface"),
            "scoring_criteria":q.get("scoring_criteria",""),
        }
    except Exception:
        return None


# ══════════════════════════════════════════════════════════════════════════════
# SCORING ENGINE
# ══════════════════════════════════════════════════════════════════════════════

def _check_correct(selected: str, correct: str, qtype: str) -> bool:
    if not selected or not correct:
        return False
    s, c = selected.strip().lower(), correct.strip().lower()
    if qtype == "mcq":
        return s == c

    # For open-ended: keyword overlap scoring (≥40% key words present)
    c_words = set(re.findall(r'\b\w{4,}\b', c))
    s_words = set(re.findall(r'\b\w{4,}\b', s))
    if not c_words:
        return len(s_words) >= 3
    overlap = len(c_words & s_words) / len(c_words)
    return overlap >= 0.35


def score_open_ended(selected: str, correct: str, reasoning: str) -> dict:
    """Returns partial credit 0.0-1.0 and quality label for open-ended answers."""
    if not selected:
        return {"credit": 0.0, "quality": "No answer", "is_correct": False}
    s_words = set(re.findall(r'\b\w{4,}\b', selected.lower()))
    c_words = set(re.findall(r'\b\w{4,}\b', correct.lower()))
    if not c_words:
        overlap = 0.5
    else:
        overlap = len(c_words & s_words) / len(c_words)

    # Boost for length and reasoning quality
    len_boost = min(0.15, len(selected.split()) / 200)
    credit = min(1.0, overlap + len_boost)

    if credit >= 0.75: quality = "Strong"
    elif credit >= 0.5: quality = "Partial"
    elif credit >= 0.25: quality = "Weak"
    else: quality = "Insufficient"

    return {"credit": credit, "quality": quality, "is_correct": credit >= 0.5}


def calculate_scores(answers: list) -> dict:
    if not answers:
        return {"accuracy": 0, "calibration": 0, "uiq": 0}

    # Accuracy (with partial credit for open-ended)
    total_credit = sum(a.get("credit", 1.0 if a["is_correct"] else 0.0) for a in answers)
    accuracy = (total_credit / len(answers)) * 100

    # Calibration
    gaps = []
    for a in answers:
        conf_pct = ((a["confidence_rating"] - 1) / 4) * 100
        perf_pct = a.get("credit", 1.0 if a["is_correct"] else 0.0) * 100
        gaps.append(abs(conf_pct - perf_pct))
    calibration = max(0, 100 - (sum(gaps) / len(gaps)))

    uiq = accuracy * 0.5 + calibration * 0.5
    return {"accuracy": accuracy, "calibration": calibration, "uiq": uiq}


def get_level(uiq: float) -> tuple:
    if uiq >= 85: return "Calibrated Mastery",   "High accuracy with well-calibrated confidence. You know what you know."
    if uiq >= 70: return "Solid Understanding",   "Good accuracy with minor calibration gaps. Strong foundation."
    if uiq >= 55: return "Surface Knowledge",     "Moderate accuracy but overconfidence detected in key areas."
    if uiq >= 40: return "Knowledge Illusion",    "Significant gap between confidence and actual performance."
    return               "Foundational Gap",      "Low accuracy with overconfidence — the highest-risk cognitive state."


def get_calibration_status(conf: int, is_correct: bool, credit: float = None) -> str:
    perf = credit if credit is not None else (1.0 if is_correct else 0.0)
    conf_pct = ((conf - 1) / 4)
    if conf_pct >= 0.75 and perf < 0.4:  return "Overconfident"
    if conf_pct <= 0.25 and perf > 0.6:  return "Underconfident"
    return "Well-calibrated"


# ══════════════════════════════════════════════════════════════════════════════
# AI-POWERED DEEP ANALYSIS — the core differentiator
# ══════════════════════════════════════════════════════════════════════════════

ANALYSIS_PROMPT = """\
You are a cognitive science expert analyzing a student's assessment results.
Perform a deep, precise, psychologically grounded analysis. Be specific — reference their actual data.
Do NOT be generic. Every insight must be earned by evidence in the data.

ASSESSMENT DATA:
{data}

Return ONLY valid JSON:
{{
  "archetype": {{
    "name": "Two or three word cognitive archetype name (e.g. 'Confident Executor', 'Reflective Analyst', 'Surface Memorizer', 'Knowledge Illusion Risk', 'Calibrated Thinker', 'Intuitive Guesser', 'Conceptual Reasoner')",
    "description": "2 sentences: what this archetype means for their learning, grounded in their data."
  }},
  "insights": [
    "Specific insight 1 — must reference actual topics, scores, or patterns from the data. 2-3 sentences.",
    "Specific insight 2 — different angle than insight 1.",
    "Specific insight 3 — must mention something the student likely didn't realize about themselves.",
    "Specific insight 4 — about their reasoning patterns if reasoning data is present."
  ],
  "misconceptions": [
    "If detectable, name one specific misconception suggested by wrong answers + high confidence. If none detectable, return empty string."
  ],
  "recommendations": [
    "Concrete action 1 — specific study technique matched to their archetype.",
    "Concrete action 2 — addresses their biggest weakness identified in the data.",
    "Concrete action 3 — leverages their strongest cognitive asset."
  ],
  "one_line_verdict": "One sentence that captures their cognitive state today. Honest but constructive."
}}"""


def generate_deep_analysis(answers: list, scores: dict) -> dict:
    """Call Groq with full assessment data for AI-powered cognitive analysis."""

    # Build rich data summary for the prompt
    topic_data   = defaultdict(lambda: {"correct": 0, "total": 0, "avg_conf": 0, "confidences": []})
    type_data    = defaultdict(lambda: {"correct": 0, "total": 0})
    over_conf    = []
    under_conf   = []
    reasoning_samples = []

    for a in answers:
        t = a.get("topic_tag", "General")
        topic_data[t]["total"]       += 1
        topic_data[t]["confidences"].append(a["confidence_rating"])
        if a["is_correct"]:
            topic_data[t]["correct"] += 1

        qt = a.get("question_type", "mcq")
        type_data[qt]["total"] += 1
        if a["is_correct"]:
            type_data[qt]["correct"] += 1

        calib = a.get("calibration_status", "")
        if calib == "Overconfident":
            over_conf.append(f"{t}: '{a['question_text'][:60]}'")
        elif calib == "Underconfident":
            under_conf.append(f"{t}: '{a['question_text'][:60]}'")

        if a.get("reasoning") and len(a["reasoning"]) > 10:
            reasoning_samples.append({
                "q": a["question_text"][:60],
                "reasoning": a["reasoning"][:120],
                "correct": a["is_correct"],
                "conf": a["confidence_rating"],
            })

    topic_summary = {
        t: {
            "accuracy_pct": round(d["correct"]/d["total"]*100),
            "avg_confidence": round(sum(d["confidences"])/len(d["confidences"]), 1),
            "questions_tested": d["total"],
        }
        for t, d in topic_data.items()
    }

    type_summary = {
        qt: {
            "accuracy_pct": round(d["correct"]/d["total"]*100) if d["total"] else 0,
            "count": d["total"],
        }
        for qt, d in type_data.items()
    }

    data = {
        "overall_scores": {
            "accuracy":    round(scores["accuracy"], 1),
            "calibration": round(scores["calibration"], 1),
            "uiq_score":   round(scores["uiq"], 1),
        },
        "total_questions": len(answers),
        "correct_count":   sum(1 for a in answers if a["is_correct"]),
        "topic_breakdown": topic_summary,
        "question_type_performance": type_summary,
        "overconfident_on": over_conf[:3],
        "underconfident_on": under_conf[:3],
        "reasoning_samples": reasoning_samples[:4],
    }

    try:
        raw = _groq([
            {"role": "system", "content": "You are a cognitive science expert. Return only valid JSON."},
            {"role": "user",   "content": ANALYSIS_PROMPT.format(data=json.dumps(data, indent=2))},
        ], temperature=0.5, max_tokens=1500)

        raw = re.sub(r"```json\s*", "", raw)
        raw = re.sub(r"```\s*",     "", raw)
        return json.loads(raw.strip())
    except Exception:
        # Fallback: rule-based analysis if AI call fails
        return _fallback_analysis(answers, scores, over_conf, under_conf, topic_summary, type_summary)


def _fallback_analysis(answers, scores, over_conf, under_conf, topic_summary, type_summary) -> dict:
    acc, cal, uiq = scores["accuracy"], scores["calibration"], scores["uiq"]

    # Archetype
    if acc >= 75 and cal >= 75:
        arch_name = "Calibrated Thinker"
        arch_desc = "You know the material and you know that you know it. Rare combination."
    elif acc >= 65 and cal < 55:
        arch_name = "Confident Executor"
        arch_desc = "You perform well but your confidence runs ahead of your actual knowledge in places."
    elif acc < 55 and cal < 55:
        arch_name = "Knowledge Illusion Risk"
        arch_desc = "High confidence despite gaps — the most dangerous learning state."
    elif acc < 55 and cal >= 65:
        arch_name = "Reflective Learner"
        arch_desc = "You know what you don't know. The gaps are real but so is your self-awareness."
    else:
        arch_name = "Surface Memorizer"
        arch_desc = "Strong on recall, weaker on conceptual depth."

    weak_topics  = [t for t, d in topic_summary.items() if d["accuracy_pct"] < 50]
    strong_topics = [t for t, d in topic_summary.items() if d["accuracy_pct"] >= 75]

    insights = [
        f"Your accuracy was {acc:.0f}% and calibration was {cal:.0f}%. The {abs(acc-cal):.0f}-point gap between them is the key signal — it reveals how well your self-assessment tracks your actual performance.",
        f"Overconfidence detected in {len(over_conf)} questions. " + (f"Particularly in: {', '.join(over_conf[:2])}." if over_conf else "None detected."),
        f"Weakest topics: {', '.join(weak_topics[:3]) if weak_topics else 'None — strong across the board'}. " + (f"Strongest: {', '.join(strong_topics[:2])}." if strong_topics else ""),
        "Open-ended questions reveal understanding depth that MCQs cannot. Review your short-answer responses — they show where language and concept meet."
    ]
    recs = [
        "For overconfident topics: use the 'explain from scratch' method — write out the concept without looking at any source material.",
        "For weak topics: don't re-read. Do active recall: close the book, write down everything you remember, then check.",
        "Your strongest asset: " + ("metacognitive awareness — leverage it by predicting your score before each study session." if cal >= 65 else "willingness to attempt hard questions — now pair that with slower, deeper reading."),
    ]
    return {
        "archetype":       {"name": arch_name, "description": arch_desc},
        "insights":        insights,
        "misconceptions":  [""],
        "recommendations": recs,
        "one_line_verdict": f"UnderstandIQ score of {uiq:.0f} — {'strong foundation with calibration to work on' if uiq >= 60 else 'significant gaps in both knowledge and self-assessment accuracy'}.",
    }


# ══════════════════════════════════════════════════════════════════════════════
# PDF GENERATION — robust Unicode handling
# ══════════════════════════════════════════════════════════════════════════════

def _safe(text: str) -> str:
    """Strip all non-latin-1 characters for FPDF compatibility."""
    replacements = {
        "\u2014": "-", "\u2013": "-", "\u2019": "'", "\u2018": "'",
        "\u201c": '"', "\u201d": '"', "\u2022": "*", "\u2192": "->",
        "\u2026": "...", "\u00b0": "deg",
        # emoji strip
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    # Remove anything not encodable in latin-1
    return text.encode("latin-1", "replace").decode("latin-1")


def generate_pdf(results: dict) -> bytes:
    from fpdf import FPDF

    class PDF(FPDF):
        def header(self):
            self.set_font("Helvetica", "B", 10)
            self.set_text_color(124, 111, 255)
            self.cell(0, 8, "UnderstandIQ | Cognitive Assessment Report", align="R", new_x="LMARGIN", new_y="NEXT")
            self.set_draw_color(28, 28, 46)
            self.line(10, self.get_y(), 200, self.get_y())
            self.ln(3)

        def footer(self):
            self.set_y(-15)
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(68, 68, 90)
            self.cell(0, 5, _safe(f"Page {self.page_no()} | HCMS Research DOI: 10.5281/zenodo.18269740 | Muhammad Rayan Shahid"), align="C")

    pdf = PDF()
    pdf.set_margins(15, 15, 15)
    pdf.add_page()
    pdf.set_auto_page_break(True, 20)

    def h1(t): pdf.set_font("Helvetica","B",20); pdf.set_text_color(232,232,240); pdf.cell(0,10,_safe(t),new_x="LMARGIN",new_y="NEXT"); pdf.ln(2)
    def h2(t): pdf.set_font("Helvetica","B",12); pdf.set_text_color(200,200,220); pdf.cell(0,8,_safe(t),new_x="LMARGIN",new_y="NEXT"); pdf.ln(1)
    def body(t,color=(136,136,170)):
        pdf.set_font("Helvetica","",9); pdf.set_text_color(*color)
        pdf.multi_cell(0, 5, _safe(t)); pdf.ln(1)
    def rule():
        pdf.set_draw_color(28,28,46); pdf.line(15, pdf.get_y(), 195, pdf.get_y()); pdf.ln(4)

    # Title
    pdf.set_font("Helvetica","B",28); pdf.set_text_color(124,111,255)
    pdf.cell(0, 14, "UnderstandIQ", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica","",11); pdf.set_text_color(136,136,170)
    pdf.cell(0, 6, "Cognitive Assessment Report", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica","",9)
    pdf.cell(0, 5, _safe(f"Document: {results['filename']}  |  {results['timestamp']}"), align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8); rule()

    # Score block
    scores = results["scores"]
    level, ldesc = get_level(scores["uiq"])
    pdf.set_font("Helvetica","B",48); pdf.set_text_color(124,111,255)
    pdf.cell(0, 22, str(int(scores["uiq"])), align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica","B",14); pdf.set_text_color(232,232,240)
    pdf.cell(0, 8, _safe(level), align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica","",10); pdf.set_text_color(136,136,170)
    pdf.cell(0, 6, _safe(ldesc), align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)

    # Metrics row
    for label, val, unit in [
        ("Accuracy",    scores["accuracy"],    "%"),
        ("Calibration", scores["calibration"], "%"),
        ("UnderstandIQ",scores["uiq"],         ""),
    ]:
        pdf.set_font("Helvetica","B",10); pdf.set_text_color(180,180,220)
        pdf.cell(60, 7, f"{label}: {val:.0f}{unit}", new_x="RIGHT", new_y="LAST")
    pdf.ln(10); rule()

    # Archetype
    analysis = results.get("analysis", {})
    if analysis.get("archetype"):
        h2("Cognitive Archetype")
        arch = analysis["archetype"]
        pdf.set_font("Helvetica","B",13); pdf.set_text_color(167,139,250)
        pdf.cell(0, 8, _safe(arch.get("name","Unknown")), new_x="LMARGIN", new_y="NEXT")
        body(arch.get("description",""))
        pdf.ln(2); rule()

    # One-line verdict
    if analysis.get("one_line_verdict"):
        h2("Verdict")
        body(analysis["one_line_verdict"], color=(232,232,240))
        pdf.ln(2); rule()

    # Insights
    if analysis.get("insights"):
        h2("Learning Insights")
        for i, ins in enumerate(analysis["insights"], 1):
            if ins:
                pdf.set_font("Helvetica","B",9); pdf.set_text_color(124,111,255)
                pdf.cell(0, 5, f"Insight {i}", new_x="LMARGIN", new_y="NEXT")
                body(ins)
        rule()

    # Recommendations
    if analysis.get("recommendations"):
        h2("Recommended Actions")
        for rec in analysis["recommendations"]:
            if rec:
                pdf.set_font("Helvetica","",9); pdf.set_text_color(0,212,170)
                pdf.cell(6,5,"->",new_x="RIGHT",new_y="LAST")
                pdf.set_text_color(160,160,190)
                pdf.multi_cell(0, 5, _safe(rec)); pdf.ln(1)
        rule()

    # Question breakdown
    h2("Question Breakdown")
    for i, a in enumerate(results["answers"], 1):
        corr_label = "CORRECT" if a["is_correct"] else f"WRONG (quality: {a.get('quality','-')})"
        calib_lbl  = a.get("calibration_status","")
        q_text     = a["question_text"][:70] + ("..." if len(a["question_text"]) > 70 else "")
        pdf.set_font("Helvetica","B",8)
        pdf.set_text_color(0,212,170) if a["is_correct"] else pdf.set_text_color(255,107,107)
        pdf.cell(14, 5, f"Q{i}", new_x="RIGHT", new_y="LAST")
        pdf.set_text_color(200,200,220)
        pdf.cell(95, 5, _safe(q_text), new_x="RIGHT", new_y="LAST")
        pdf.set_font("Helvetica","",8)
        pdf.cell(35, 5, _safe(corr_label), new_x="RIGHT", new_y="LAST")
        pdf.cell(20, 5, f"Conf:{a['confidence_rating']}/5", new_x="RIGHT", new_y="LAST")
        pdf.cell(0,  5, _safe(calib_lbl[:12]), new_x="LMARGIN", new_y="NEXT")

    pdf.ln(6)
    pdf.set_font("Helvetica","I",8); pdf.set_text_color(68,68,90)
    pdf.cell(0, 5, "Built on HCMS Research | ByteBrilliance AI", align="C")

    return bytes(pdf.output())


# ══════════════════════════════════════════════════════════════════════════════
# UI HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def header():
    st.markdown("""
    <div class="uiq-header">
        <div class="uiq-logo">Understand<span>IQ</span></div>
        <div class="uiq-sub">Discover the gap between what you think you know — and what you actually know.</div>
        <div class="uiq-badge">Built on HCMS Research · DOI: 10.5281/zenodo.18269740</div>
    </div>
    """, unsafe_allow_html=True)

def section(title): st.markdown(f'<div class="sh">{title}</div>', unsafe_allow_html=True)
def info(msg):       st.markdown(f'<div class="info-box">{msg}</div>', unsafe_allow_html=True)
def ok(msg):         st.markdown(f'<div class="ok-box">&#10003; {msg}</div>', unsafe_allow_html=True)
def err(msg):        st.markdown(f'<div class="err-box">&#9888; {msg}</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# STAGE 1 — UPLOAD
# ══════════════════════════════════════════════════════════════════════════════

def show_upload():
    header()
    info("Upload any PDF, DOCX, or text — lecture notes, research papers, articles, or study guides. "
         "UnderstandIQ measures not just whether you answer correctly, but whether your confidence matches reality. "
         "It also captures your reasoning, enabling deep cognitive pattern detection.")

    c1, c2 = st.columns(2)
    with c1:
        uf = st.file_uploader("Upload document", type=["pdf","txt","docx"], label_visibility="collapsed")
    with c2:
        rt = st.text_area("Or paste text", height=120, placeholder="Paste notes, article, or study material here…", label_visibility="collapsed")

    text, fname, wc = parse_document(uf, rt)

    if text:
        ok(f"{fname} · {wc:,} words · ~{max(1,wc//200)} min read")
        st.session_state.doc_text   = text
        st.session_state.filename   = fname
        st.session_state.word_count = wc

        section("Configure Assessment")
        c1, c2 = st.columns(2)
        with c1:
            nq = st.selectbox("Questions", [5, 8, 10], index=1,
                              help="More questions = more precise cognitive data")
        with c2:
            depth = st.selectbox("Depth", ["mixed","surface","conceptual","applied"],
                                 format_func=lambda x: {
                                     "mixed":"Mixed — Recommended",
                                     "surface":"Surface — Recall",
                                     "conceptual":"Conceptual — Understanding",
                                     "applied":"Applied — Transfer"}[x])
        st.session_state.num_q = nq
        st.session_state.depth = depth

        st.markdown("<br>", unsafe_allow_html=True)
        info("Questions include: <b>MCQ</b> (recall speed), <b>Short Answer</b> (articulation), "
             "<b>Application</b> (transfer thinking), and <b>Explain-It</b> (depth of understanding). "
             "You will also capture your reasoning on each question — this is what enables the deep cognitive analysis.")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Generate Assessment →", use_container_width=True):
            if wc < 50:
                err("Please provide at least 50 words for a meaningful assessment.")
            else:
                with st.spinner("Reading your document and generating cognitive assessment…"):
                    try:
                        qs = generate_questions(text, nq, depth)
                        if not qs:
                            err("Could not generate questions. Check your GROQ_API_KEY in Streamlit Secrets, or try different content.")
                        else:
                            st.session_state.questions = qs
                            st.session_state.current_q = 0
                            st.session_state.answers   = []
                            st.session_state.stage     = "quiz"
                            st.rerun()
                    except Exception as e:
                        err(f"Error: {e}")
    elif uf or rt.strip():
        err("Could not extract text. Try a different file or paste text directly.")


# ══════════════════════════════════════════════════════════════════════════════
# STAGE 2 — QUIZ (with reasoning capture)
# ══════════════════════════════════════════════════════════════════════════════

QTYPE_LABELS = {
    "mcq":          "Multiple Choice",
    "short_answer": "Short Answer",
    "application":  "Application",
    "explain":      "Explain It",
}

QTYPE_PROMPTS = {
    "mcq":          "Select the best answer.",
    "short_answer": "Write a concise, accurate answer in 1-3 sentences.",
    "application":  "Explain how this concept applies. Think through it carefully — there may not be one right answer.",
    "explain":      "Explain this concept as simply and completely as you can, as if teaching someone new to it.",
}

CONFIDENCE_LABELS = [
    "1 — Just guessing",
    "2 — Somewhat unsure",
    "3 — Neutral",
    "4 — Fairly confident",
    "5 — Completely certain",
]


def show_quiz():
    qs = st.session_state.questions
    if not qs:
        st.session_state.stage = "upload"; st.rerun(); return

    cur   = st.session_state.current_q
    total = len(qs)
    q     = qs[cur]
    qtype = q.get("question_type", "mcq")

    # Progress
    pct = int((cur / total) * 100)
    st.markdown(f'<div class="prog-lbl">{cur+1} of {total}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="prog-wrap"><div class="prog-fill" style="width:{pct}%"></div></div>', unsafe_allow_html=True)

    # Question card
    type_label = QTYPE_LABELS.get(qtype, qtype.replace("_"," ").title())
    st.markdown(f"""
    <div class="q-card">
        <div class="q-meta">Q{cur+1}/{total} · {q.get('difficulty','').title()} · {q.get('topic_tag','')}</div>
        <div class="q-type-badge">{type_label}</div>
        <div class="q-text">{q['question_text']}</div>
    </div>
    """, unsafe_allow_html=True)

    # Answer input
    type_prompt = QTYPE_PROMPTS.get(qtype, "")
    st.caption(type_prompt)

    options = q.get("options")
    if qtype == "mcq" and options:
        selected = st.radio("Answer", options, key=f"ans_{cur}", index=None, label_visibility="collapsed")
    else:
        selected = st.text_area(
            "Your answer",
            key=f"ans_{cur}",
            height=110,
            placeholder="Type your answer here…",
            label_visibility="collapsed",
        )
        selected = selected.strip() if selected else None

    # Reasoning capture — the key differentiator
    st.markdown('<div class="reasoning-prompt">&#128161; <b>Optional but powerful:</b> In one sentence, '
                'why did you choose this answer? This reveals your reasoning patterns for deep cognitive analysis.</div>',
                unsafe_allow_html=True)
    reasoning = st.text_input("Reasoning (optional)", key=f"rsn_{cur}", placeholder="I chose this because…", label_visibility="collapsed")

    # Confidence
    st.markdown('<div class="conf-label">Rate your confidence before seeing the result</div>', unsafe_allow_html=True)
    conf_sel = st.select_slider("Confidence", options=CONFIDENCE_LABELS,
                                value="3 — Neutral", key=f"conf_{cur}",
                                label_visibility="collapsed")
    conf_val = CONFIDENCE_LABELS.index(conf_sel) + 1

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns([1, 2])

    with c1:
        if cur > 0:
            if st.button("← Back", use_container_width=True):
                if st.session_state.answers:
                    st.session_state.answers.pop()
                st.session_state.current_q -= 1
                st.rerun()

    with c2:
        is_last    = (cur == total - 1)
        btn_label  = "Finish — See My Cognitive Profile →" if is_last else "Next Question →"
        can_go     = bool(selected)

        if st.button(btn_label, disabled=not can_go, use_container_width=True):
            # Score this answer
            if qtype == "mcq":
                is_correct = _check_correct(selected or "", q.get("correct_answer",""), "mcq")
                credit     = 1.0 if is_correct else 0.0
                quality    = "Correct" if is_correct else "Incorrect"
            else:
                result = score_open_ended(selected or "", q.get("correct_answer",""), reasoning)
                is_correct = result["is_correct"]
                credit     = result["credit"]
                quality    = result["quality"]

            record = {
                "question_text":   q["question_text"],
                "question_type":   qtype,
                "selected_answer": selected,
                "correct_answer":  q.get("correct_answer",""),
                "scoring_criteria":q.get("scoring_criteria",""),
                "reasoning":       reasoning,
                "confidence_rating": conf_val,
                "topic_tag":       q.get("topic_tag","General"),
                "difficulty":      q.get("difficulty","surface"),
                "is_correct":      is_correct,
                "credit":          credit,
                "quality":         quality,
                "calibration_status": get_calibration_status(conf_val, is_correct, credit),
            }
            st.session_state.answers.append(record)

            if is_last:
                _finalize_results()
            else:
                st.session_state.current_q += 1
                st.rerun()

    if not can_go:
        st.markdown('<div style="text-align:center;font-size:12px;color:var(--faint);margin-top:.4rem;">Enter an answer to continue</div>',
                    unsafe_allow_html=True)


def _finalize_results():
    answers = st.session_state.answers
    scores  = calculate_scores(answers)
    level, ldesc = get_level(scores["uiq"])

    with st.spinner("Running cognitive analysis — this takes 10-15 seconds…"):
        analysis = generate_deep_analysis(answers, scores)

    st.session_state.results = {
        "scores":   scores,
        "level":    level,
        "ldesc":    ldesc,
        "analysis": analysis,
        "answers":  answers,
        "filename": st.session_state.filename,
        "timestamp":datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    st.session_state.stage = "results"
    st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# STAGE 3 — RESULTS
# ══════════════════════════════════════════════════════════════════════════════

def show_results():
    r = st.session_state.results
    if not r:
        st.session_state.stage = "upload"; st.rerun(); return

    scores   = r["scores"]
    analysis = r.get("analysis", {})
    answers  = r["answers"]
    arch     = analysis.get("archetype", {})

    # ── Verdict ──────────────────────────────────────────────────────────────
    verdict_one_line = _safe(analysis.get("one_line_verdict",""))
    archetype_name   = arch.get("name","")
    st.markdown(f"""
    <div class="verdict">
        <div class="verdict-score">{scores['uiq']:.0f}</div>
        <div class="verdict-level">{r['level']}</div>
        <div class="verdict-desc">{verdict_one_line}</div>
        {"<div class='verdict-archetype'>" + archetype_name + "</div>" if archetype_name else ""}
    </div>
    """, unsafe_allow_html=True)

    # ── Metrics ───────────────────────────────────────────────────────────────
    acc, cal, uiq = scores["accuracy"], scores["calibration"], scores["uiq"]
    acc_c = "green" if acc >= 70 else ("amber" if acc >= 50 else "red")
    cal_c = "green" if cal >= 70 else ("amber" if cal >= 50 else "red")
    st.markdown(f"""
    <div class="metrics">
        <div class="metric"><div class="metric-val c-{acc_c}">{acc:.0f}%</div><div class="metric-lbl">Accuracy</div></div>
        <div class="metric"><div class="metric-val c-{cal_c}">{cal:.0f}%</div><div class="metric-lbl">Calibration</div></div>
        <div class="metric"><div class="metric-val c-accent">{uiq:.0f}</div><div class="metric-lbl">UnderstandIQ</div></div>
    </div>
    """, unsafe_allow_html=True)

    # ── Archetype panel ───────────────────────────────────────────────────────
    if arch:
        st.markdown(f"""
        <div class="archetype-panel">
            <div class="archetype-title">Your Cognitive Archetype</div>
            <div class="archetype-name">{arch.get('name','')}</div>
            <div class="archetype-desc">{arch.get('description','')}</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Calibration chart ─────────────────────────────────────────────────────
    section("Calibration Gap Analysis")
    _chart(answers)

    # ── Question breakdown ────────────────────────────────────────────────────
    section("Question-by-Question Breakdown")
    for i, a in enumerate(answers):
        correct   = a["is_correct"]
        q_text    = a["question_text"]
        calib     = a.get("calibration_status","Well-calibrated")
        qtype     = QTYPE_LABELS.get(a.get("question_type","mcq"), a.get("question_type",""))
        quality   = a.get("quality","")
        reasoning = a.get("reasoning","")
        credit    = a.get("credit",1.0 if correct else 0.0)

        row_cls   = "bk-correct" if correct else "bk-wrong"
        icon      = "&#10003;" if correct else "&#10007;"
        calib_cls = {"Overconfident":"calib-over","Underconfident":"calib-under","Well-calibrated":"calib-good"}.get(calib,"calib-good")

        credit_bar = ""
        if a.get("question_type") != "mcq":
            pct = int(credit * 100)
            credit_bar = f'<div style="height:3px;background:rgba(255,255,255,.08);border-radius:100px;margin-top:4px"><div style="height:100%;width:{pct}%;background:{"var(--green)" if pct>=75 else ("var(--amber)" if pct>=40 else "var(--red)")};border-radius:100px"></div></div>'

        reasoning_html = f'<div class="bk-answer">Reasoning: "{reasoning[:100]}"</div>' if reasoning else ""

        st.markdown(f"""
        <div class="bk-row {row_cls}">
            <div class="bk-icon">{icon}</div>
            <div class="bk-body">
                <div class="bk-q">{q_text}</div>
                <div class="bk-meta">
                    <span class="bk-tag">{qtype}</span>
                    <span class="bk-tag">{a.get('topic_tag','')}</span>
                    <span class="bk-tag">{a.get('difficulty','').title()}</span>
                    <span class="bk-calib {calib_cls}">{calib} · {a['confidence_rating']}/5</span>
                    {f'<span class="bk-tag">Quality: {quality}</span>' if quality else ""}
                </div>
                {credit_bar}
                {reasoning_html}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Misconceptions ────────────────────────────────────────────────────────
    misconceptions = [m for m in analysis.get("misconceptions", []) if m and len(m) > 10]
    if misconceptions:
        section("Misconception Detection")
        for m in misconceptions:
            st.markdown(f'<div class="card card-amber"><b>Detected pattern:</b> {m}</div>', unsafe_allow_html=True)

    # ── Insights ──────────────────────────────────────────────────────────────
    section("Deep Cognitive Insights")
    insights = [i for i in analysis.get("insights", []) if i and len(i) > 10]
    for ins in insights:
        st.markdown(f'<div class="insight">&#128161; {ins}</div>', unsafe_allow_html=True)

    # ── Recommendations ───────────────────────────────────────────────────────
    section("Personalised Recommendations")
    recs = [r2 for r2 in analysis.get("recommendations", []) if r2 and len(r2) > 10]
    for rec in recs:
        st.markdown(f'<div class="rec">&#8594; {rec}</div>', unsafe_allow_html=True)

    # ── Correct answers reveal ────────────────────────────────────────────────
    section("Correct Answers & Scoring Criteria")
    for i, a in enumerate(answers, 1):
        with st.expander(f"Q{i}: {a['question_text'][:60]}…"):
            st.markdown(f"**Your answer:** {a.get('selected_answer','—')}")
            st.markdown(f"**Correct answer / Key points:** {a.get('correct_answer','—')}")
            if a.get("scoring_criteria"):
                st.markdown(f"**Scoring criteria:** {a['scoring_criteria']}")

    # ── Export ────────────────────────────────────────────────────────────────
    st.markdown("---")
    section("Export Report")
    try:
        pdf_bytes = generate_pdf(r)
        st.download_button(
            "⬇ Download Full PDF Report",
            data=pdf_bytes,
            file_name=f"UnderstandIQ_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
    except Exception as e:
        err(f"PDF generation error: {e}")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Start New Assessment", use_container_width=True):
        _reset()


def _chart(answers: list):
    import plotly.graph_objects as go

    nums  = list(range(1, len(answers) + 1))
    confs = [((a["confidence_rating"] - 1) / 4) * 100 for a in answers]
    perfs = [a.get("credit", 1.0 if a["is_correct"] else 0.0) * 100 for a in answers]
    corr  = [a["is_correct"] for a in answers]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=[x - 0.22 for x in nums], y=confs, name="Confidence",
        marker_color="#7c6fff", width=0.38,
        hovertemplate="Q%{x:.0f}<br>Confidence: %{y:.0f}%<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        x=[x + 0.22 for x in nums], y=perfs, name="Performance",
        marker_color=["#00d4aa" if c else "#ff6b6b" for c in corr], width=0.38,
        hovertemplate="Q%{x:.0f}<br>Performance: %{y:.0f}%<extra></extra>",
    ))

    # Annotate large gaps
    for i, (c, p) in enumerate(zip(confs, perfs)):
        if abs(c - p) >= 45:
            fig.add_annotation(
                x=i + 1, y=max(c, p) + 8,
                text=f"{abs(c-p):.0f}pt gap",
                showarrow=False,
                font=dict(size=9, color="#ffb347"),
            )

    fig.update_layout(
        template="plotly_dark", plot_bgcolor="#0f0f18", paper_bgcolor="#0f0f18",
        font=dict(family="Outfit, sans-serif", color="#8888aa", size=12),
        xaxis=dict(title="Question", tickmode="linear", tick0=1, dtick=1, gridcolor="#1c1c2e", zeroline=False),
        yaxis=dict(title="Score (%)", range=[0, 115], gridcolor="#1c1c2e", zeroline=False),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        margin=dict(t=50, b=40, l=50, r=20), height=310, bargap=0.12,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


# ══════════════════════════════════════════════════════════════════════════════
# MAIN ROUTER
# ══════════════════════════════════════════════════════════════════════════════

stage = st.session_state.get("stage", "upload")
if   stage == "upload":  show_upload()
elif stage == "quiz":    show_quiz()
elif stage == "results": show_results()
