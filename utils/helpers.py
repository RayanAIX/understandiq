"""Helper utilities for UnderstandIQ."""

import os
from datetime import datetime
from typing import List, Dict


def format_timestamp() -> str:
    """Get current timestamp formatted for reports."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def ensure_env_file():
    """Check if .env file exists, create if not."""
    env_path = os.path.join(os.getcwd(), '.env')
    if not os.path.exists(env_path):
        example_path = os.path.join(os.getcwd(), '.env.example')
        if os.path.exists(example_path):
            with open(example_path, 'r') as src:
                with open(env_path, 'w') as dst:
                    dst.write(src.read())


def truncate_text(text: str, max_length: int = 60) -> str:
    """Truncate text to max length with ellipsis."""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + '...'


def validate_questions(questions: List[Dict]) -> bool:
    """Validate that questions have required fields."""
    required_fields = ['question_text', 'question_type', 'topic_tag', 'difficulty']
    for q in questions:
        for field in required_fields:
            if field not in q:
                return False
    return True


def format_score_for_display(score: float) -> str:
    """Format score for display with appropriate decimal places."""
    return f"{score:.1f}"