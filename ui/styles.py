"""CSS styles for UnderstandIQ app."""

THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Outfit:wght@300;400;500;600;700&display=swap');

:root {
    --bg-primary: #0A0A0F;
    --bg-surface: #111118;
    --border-color: #1E1E2E;
    --accent-primary: #6C63FF;
    --accent-success: #00D4AA;
    --accent-warning: #FFB347;
    --accent-danger: #FF6B6B;
    --text-primary: #E8E8F0;
    --text-secondary: #8888AA;
}

* {
    font-family: 'Outfit', sans-serif;
}

.stApp {
    background-color: var(--bg-primary);
    color: var(--text-primary);
}

[data-testid="stHeader"] {
    display: none;
}

[data-testid="stToolbar"] {
    display: none;
}

#MainMenu {
    display: none;
}

.stMarkdown {
    color: var(--text-primary);
}

/* Typography */
h1, h2, h3 {
    font-family: 'Outfit', sans-serif;
    font-weight: 600;
    color: var(--text-primary);
}

.metric-value {
    font-family: 'DM Mono', monospace;
    font-weight: 500;
}

/* Cards */
.uicard {
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-left: 3px solid var(--accent-primary);
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 16px;
}

.uicard-success {
    border-left-color: var(--accent-success);
}

.uicard-warning {
    border-left-color: var(--accent-warning);
}

.uicard-danger {
    border-left-color: var(--accent-danger);
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, var(--accent-primary), #5a52d5);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 12px 28px;
    font-family: 'Outfit', sans-serif;
    font-weight: 500;
    font-size: 16px;
    cursor: pointer;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 20px rgba(108, 99, 255, 0.4);
}

.stButton > button:disabled {
    background: #3a3a4a;
    color: #666;
    cursor: not-allowed;
    transform: none;
    box-shadow: none;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: var(--bg-surface);
    border: 2px dashed var(--border-color);
    border-radius: 12px;
    padding: 20px;
}

[data-testid="stFileUploader"]:hover {
    border-color: var(--accent-primary);
}

/* Radio buttons */
.stRadio > div {
    gap: 12px;
}

.stRadio label {
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 16px 20px;
    margin-bottom: 8px;
    cursor: pointer;
    transition: all 0.2s ease;
}

.stRadio label:hover {
    border-color: var(--accent-primary);
}

.stRadio input:checked + div > div > div:first-child {
    background: var(--accent-primary) !important;
}

/* Select box */
[data-testid="stSelectbox"] {
    background: var(--bg-surface);
}

/* Slider */
.stSlider > div > div > div {
    background: var(--accent-primary) !important;
}

.stSlider [data-baseweb="slider"] > div > div > div:first-child {
    background: var(--accent-primary) !important;
}

.stSlider [data-baseweb="slider"] > div > div > div:last-child {
    background: var(--accent-primary) !important;
}

/* Progress bar */
.stProgress > div > div > div {
    background: var(--accent-primary);
}

/* Tables */
[data-testid="stDataFrame"] {
    background: var(--bg-surface);
    border-radius: 12px;
    border: 1px solid var(--border-color);
}

/* Divider */
hr {
    border-color: var(--border-color);
}

/* Upload stage */
.upload-container {
    max-width: 700px;
    margin: 0 auto;
}

/* Question card */
.question-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    padding: 32px;
    margin-bottom: 24px;
}

.question-number {
    font-family: 'DM Mono', monospace;
    color: var(--accent-primary);
    font-size: 14px;
    margin-bottom: 12px;
}

.question-text {
    font-size: 22px;
    font-weight: 500;
    line-height: 1.5;
    margin-bottom: 24px;
}

/* Option buttons */
.option-button {
    display: block;
    width: 100%;
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: 10px;
    padding: 16px 20px;
    text-align: left;
    color: var(--text-primary);
    font-size: 16px;
    cursor: pointer;
    transition: all 0.2s ease;
    margin-bottom: 12px;
}

.option-button:hover {
    border-color: var(--accent-primary);
    background: rgba(108, 99, 255, 0.1);
}

.option-button.selected {
    border-color: var(--accent-primary);
    background: rgba(108, 99, 255, 0.15);
}

/* Confidence slider */
.confidence-section {
    background: rgba(108, 99, 255, 0.1);
    border-radius: 12px;
    padding: 24px;
    margin-top: 24px;
}

.confidence-label {
    font-size: 16px;
    font-weight: 500;
    margin-bottom: 16px;
    color: var(--text-primary);
}

.confidence-value {
    font-family: 'DM Mono', monospace;
    color: var(--accent-primary);
    font-weight: 500;
}

/* Results */
.verdict-card {
    text-align: center;
    padding: 40px;
    background: linear-gradient(135deg, rgba(108, 99, 255, 0.15), rgba(108, 99, 255, 0.05));
    border-radius: 16px;
    border: 1px solid var(--accent-primary);
    margin-bottom: 32px;
}

.verdict-title {
    font-size: 48px;
    font-family: 'DM Mono', monospace;
    font-weight: 700;
    color: var(--accent-primary);
    margin-bottom: 12px;
}

.verdict-description {
    font-size: 18px;
    color: var(--text-secondary);
}

/* Metric cards */
.metric-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 24px;
    text-align: center;
}

.metric-label {
    font-size: 14px;
    color: var(--text-secondary);
    margin-bottom: 8px;
}

.metric-value {
    font-family: 'DM Mono', monospace;
    font-size: 36px;
    font-weight: 600;
}

/* Breakdown table */
.breakdown-row {
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.breakdown-question {
    flex: 2;
    font-size: 14px;
    color: var(--text-primary);
}

.breakdown-topic {
    flex: 1;
    font-size: 12px;
    color: var(--text-secondary);
    text-align: center;
}

.breakdown-result {
    flex: 1;
    text-align: center;
    font-family: 'DM Mono', monospace;
}

.breakdown-confidence {
    flex: 1;
    text-align: center;
    font-family: 'DM Mono', monospace;
}

.breakdown-status {
    flex: 1;
    text-align: right;
    font-size: 12px;
    font-weight: 500;
}

/* Insights */
.insight-card {
    background: var(--bg-surface);
    border-left: 3px solid var(--accent-warning);
    border-radius: 8px;
    padding: 16px 20px;
    margin-bottom: 12px;
}

/* Recommendations */
.recommendation-card {
    background: var(--bg-surface);
    border-left: 3px solid var(--accent-success);
    border-radius: 8px;
    padding: 16px 20px;
    margin-bottom: 12px;
}

/* Hide some streamlit defaults */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Animation for loading */
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

.loading-text {
    animation: pulse 1.5s ease-in-out infinite;
}
</style>
"""


def get_theme_css():
    """Return the theme CSS."""
    return THEME_CSS