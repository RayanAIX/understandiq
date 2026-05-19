"""UnderstandIQ Theme CSS"""


def get_theme_css() -> str:
    return """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Outfit:wght@300;400;500;600;700&display=swap');

:root {
    --bg: #09090f;
    --surface: #111118;
    --surface2: #16161f;
    --border: #1e1e30;
    --accent: #7c6fff;
    --accent-dim: #7c6fff22;
    --success: #00d4aa;
    --success-dim: #00d4aa18;
    --warning: #ffb347;
    --warning-dim: #ffb34718;
    --danger: #ff6b6b;
    --danger-dim: #ff6b6b18;
    --text: #e8e8f0;
    --text-secondary: #8888aa;
    --text-muted: #55557a;
}

html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
[data-testid="stToolbar"] { display: none; }

/* Main container */
.main .block-container {
    max-width: 780px;
    padding: 2rem 1.5rem 4rem;
}

/* Typography */
h1 { font-family: 'Outfit', sans-serif; font-weight: 700; color: var(--text) !important; }
h2, h3 { font-family: 'Outfit', sans-serif; font-weight: 600; color: var(--text) !important; }
p, li { color: var(--text-secondary); }

/* Cards */
.uiq-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}
.uiq-card-accent {
    border-left: 3px solid var(--accent);
}
.uiq-card-success {
    border-left: 3px solid var(--success);
    background: var(--success-dim);
}
.uiq-card-warning {
    border-left: 3px solid var(--warning);
    background: var(--warning-dim);
}
.uiq-card-danger {
    border-left: 3px solid var(--danger);
    background: var(--danger-dim);
}

/* Verdict block */
.verdict-block {
    background: linear-gradient(135deg, #111118 0%, #16161f 100%);
    border: 1px solid var(--border);
    border-top: 3px solid var(--accent);
    border-radius: 16px;
    padding: 2.5rem;
    text-align: center;
    margin-bottom: 1.5rem;
}
.verdict-score {
    font-family: 'DM Mono', monospace;
    font-size: 72px;
    font-weight: 500;
    color: var(--accent);
    line-height: 1;
    margin-bottom: 0.25rem;
}
.verdict-level {
    font-size: 22px;
    font-weight: 600;
    color: var(--text);
    margin-bottom: 0.5rem;
}
.verdict-desc {
    font-size: 14px;
    color: var(--text-secondary);
    max-width: 480px;
    margin: 0 auto;
}

/* Metric cards */
.metric-row {
    display: flex;
    gap: 1rem;
    margin-bottom: 1.5rem;
}
.metric-card {
    flex: 1;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.25rem;
    text-align: center;
}
.metric-value {
    font-family: 'DM Mono', monospace;
    font-size: 36px;
    font-weight: 500;
    line-height: 1;
    margin-bottom: 0.25rem;
}
.metric-label {
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--text-muted);
}
.metric-accent { color: var(--accent); }
.metric-success { color: var(--success); }
.metric-warning { color: var(--warning); }
.metric-danger { color: var(--danger); }

/* Question card */
.question-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 2rem;
    margin-bottom: 1.5rem;
}
.question-number {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--text-muted);
    margin-bottom: 1rem;
    font-family: 'DM Mono', monospace;
}
.question-text {
    font-size: 18px;
    font-weight: 500;
    color: var(--text);
    line-height: 1.6;
}

/* Option buttons */
.stButton > button {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
    padding: 0.75rem 1.25rem !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 14px !important;
    font-weight: 400 !important;
    text-align: left !important;
    transition: all 0.15s ease !important;
    width: 100% !important;
}
.stButton > button:hover {
    border-color: var(--accent) !important;
    background: var(--accent-dim) !important;
    color: var(--text) !important;
}

/* Selected option styling - applied via selected_option state */
.option-selected > button {
    border-color: var(--accent) !important;
    background: var(--accent-dim) !important;
    color: var(--accent) !important;
    font-weight: 500 !important;
}

/* Confidence section */
.confidence-label {
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--text-muted);
    margin-bottom: 0.75rem;
    font-family: 'DM Mono', monospace;
}

/* Progress bar */
.progress-wrap {
    background: var(--surface2);
    border-radius: 100px;
    height: 4px;
    margin-bottom: 2rem;
    overflow: hidden;
}
.progress-fill {
    background: linear-gradient(90deg, var(--accent), #a78bfa);
    height: 100%;
    border-radius: 100px;
    transition: width 0.3s ease;
}
.progress-label {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    color: var(--text-muted);
    text-align: right;
    margin-bottom: 0.5rem;
}

/* Breakdown rows */
.breakdown-row {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 1rem;
}
.breakdown-correct { border-left: 3px solid var(--success); }
.breakdown-wrong { border-left: 3px solid var(--danger); }
.breakdown-status { font-size: 18px; width: 24px; flex-shrink: 0; }
.breakdown-question { flex: 1; font-size: 13px; color: var(--text); }
.breakdown-tag {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    padding: 2px 8px;
    border-radius: 100px;
    background: var(--surface2);
    color: var(--text-muted);
    white-space: nowrap;
}
.breakdown-calibration {
    font-size: 11px;
    color: var(--text-muted);
    white-space: nowrap;
}
.calib-over { color: var(--danger); }
.calib-under { color: var(--warning); }
.calib-good { color: var(--success); }

/* Insight cards */
.insight-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent);
    border-radius: 8px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 0.75rem;
    font-size: 14px;
    line-height: 1.7;
    color: var(--text-secondary);
}

/* Recommendation cards */
.rec-card {
    background: var(--success-dim);
    border: 1px solid var(--border);
    border-left: 3px solid var(--success);
    border-radius: 8px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 0.75rem;
    font-size: 14px;
    line-height: 1.7;
    color: var(--text-secondary);
}

/* Divider */
hr {
    border: none;
    border-top: 1px solid var(--border) !important;
    margin: 2rem 0 !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: var(--surface) !important;
    border: 1px dashed var(--border) !important;
    border-radius: 12px !important;
}

/* Select boxes */
[data-testid="stSelectbox"] > div > div {
    background: var(--surface) !important;
    border-color: var(--border) !important;
    color: var(--text) !important;
}

/* Slider */
[data-testid="stSlider"] > div > div > div > div {
    background: var(--accent) !important;
}

/* Text area */
textarea {
    background: var(--surface) !important;
    border-color: var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
}

/* Header area */
.app-header {
    text-align: center;
    padding: 3rem 0 2rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 2.5rem;
}
.app-title {
    font-family: 'Outfit', sans-serif;
    font-size: 48px;
    font-weight: 700;
    color: var(--text);
    letter-spacing: -0.02em;
    margin: 0;
}
.app-title span {
    color: var(--accent);
}
.app-tagline {
    font-size: 16px;
    color: var(--text-secondary);
    margin-top: 0.5rem;
    font-weight: 300;
}
.app-badge {
    display: inline-block;
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    padding: 4px 12px;
    border: 1px solid var(--border);
    border-radius: 100px;
    color: var(--text-muted);
    margin-top: 1rem;
}

/* Section headers */
.section-header {
    font-size: 13px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--text-muted);
    font-family: 'DM Mono', monospace;
    margin: 2rem 0 1rem;
}

/* Info box */
.info-box {
    background: var(--accent-dim);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent);
    border-radius: 8px;
    padding: 1rem 1.25rem;
    font-size: 13px;
    color: var(--text-secondary);
    margin-bottom: 1rem;
}

/* Success box */
.success-box {
    background: var(--success-dim);
    border: 1px solid var(--border);
    border-left: 3px solid var(--success);
    border-radius: 8px;
    padding: 0.75rem 1.25rem;
    font-size: 13px;
    color: var(--text-secondary);
    margin-bottom: 1rem;
}

/* Error box */
.error-box {
    background: var(--danger-dim);
    border: 1px solid var(--border);
    border-left: 3px solid var(--danger);
    border-radius: 8px;
    padding: 0.75rem 1.25rem;
    font-size: 13px;
    color: var(--text-secondary);
    margin-bottom: 1rem;
}
</style>
"""
