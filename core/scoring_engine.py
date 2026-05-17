"""Scoring engine for calculating UnderstandIQ metrics."""

from typing import List, Dict


def calculate_calibration_score(questions: List[Dict]) -> float:
    """
    Calculate the calibration score based on confidence vs accuracy.

    For each question:
    - Convert confidence (1-5) to percentage: conf_pct = (confidence - 1) / 4 * 100
    - Convert correctness to binary: correct_pct = 100 if correct else 0
    - Calibration gap = abs(conf_pct - correct_pct)
    - Perfect calibration = gap of 0
    - Worst calibration = gap of 100

    Calibration score = 100 - mean(all gaps)

    Args:
        questions: List of question dicts with is_correct and confidence_rating

    Returns:
        Calibration score (0-100)
    """
    if not questions:
        return 0.0

    gaps = []
    for q in questions:
        confidence = q.get('confidence_rating', 3)
        is_correct = q.get('is_correct', False)

        conf_pct = (confidence - 1) / 4 * 100
        correct_pct = 100 if is_correct else 0

        gap = abs(conf_pct - correct_pct)
        gaps.append(gap)

    mean_gap = sum(gaps) / len(gaps)
    calibration_score = 100 - mean_gap

    return round(calibration_score, 1)


def calculate_accuracy_score(questions: List[Dict]) -> float:
    """
    Calculate the percentage of questions answered correctly.

    Args:
        questions: List of question dicts

    Returns:
        Accuracy score (0-100)
    """
    if not questions:
        return 0.0

    correct_count = sum(1 for q in questions if q.get('is_correct', False))
    return round((correct_count / len(questions)) * 100, 1)


def calculate_understandiq_score(accuracy: float, calibration: float) -> float:
    """
    Calculate the composite UnderstandIQ score.

    UnderstandIQ Score = (accuracy * 0.5) + (calibration * 0.5)

    Args:
        accuracy: Accuracy score (0-100)
        calibration: Calibration score (0-100)

    Returns:
        UnderstandIQ Score (0-100)
    """
    score = (accuracy * 0.5) + (calibration * 0.5)
    return round(score, 1)


def get_level_name(score: float) -> tuple[str, str]:
    """
    Get the level name and description based on UnderstandIQ score.

    Args:
        score: UnderstandIQ Score

    Returns:
        tuple: (level_name, description)
    """
    if score >= 85:
        return "Calibrated Mastery", "High accuracy + well-calibrated confidence"
    elif score >= 70:
        return "Solid Understanding", "Good accuracy, minor calibration gaps"
    elif score >= 55:
        return "Surface Knowledge", "Moderate accuracy but overconfidence detected"
    elif score >= 40:
        return "Knowledge Illusion", "Significant gap between confidence and reality"
    else:
        return "Foundational Gap", "Low accuracy with overconfidence — high-risk zone"


def get_calibration_status(answer: Dict) -> str:
    """
    Determine calibration status for a single answer.

    Args:
        answer: Answer dictionary with confidence_rating and is_correct

    Returns:
        "Well-calibrated", "Overconfident", or "Underconfident"
    """
    confidence = answer.get('confidence_rating', 3)
    is_correct = answer.get('is_correct', False)

    if confidence >= 4 and not is_correct:
        return "Overconfident"
    elif confidence <= 2 and is_correct:
        return "Underconfident"
    else:
        return "Well-calibrated"


def analyze_topic_performance(questions: List[Dict]) -> Dict[str, Dict]:
    """
    Analyze performance by topic tag.

    Args:
        questions: List of question dicts

    Returns:
        Dict mapping topic tags to performance metrics
    """
    topic_data = {}

    for q in questions:
        topic = q.get('topic_tag', 'Unknown')
        is_correct = q.get('is_correct', False)
        confidence = q.get('confidence_rating', 3)

        if topic not in topic_data:
            topic_data[topic] = {'correct': 0, 'total': 0, 'confidences': []}

        topic_data[topic]['total'] += 1
        if is_correct:
            topic_data[topic]['correct'] += 1
        topic_data[topic]['confidences'].append(confidence)

    results = {}
    for topic, data in topic_data.items():
        accuracy = (data['correct'] / data['total']) * 100 if data['total'] > 0 else 0
        avg_confidence = sum(data['confidences']) / len(data['confidences'])
        results[topic] = {
            'accuracy': round(accuracy, 1),
            'total': data['total'],
            'avg_confidence': round(avg_confidence, 1)
        }

    return results


def analyze_difficulty_performance(questions: List[Dict]) -> Dict[str, Dict]:
    """
    Analyze performance by difficulty level.

    Args:
        questions: List of question dicts

    Returns:
        Dict mapping difficulty to performance metrics
    """
    difficulty_data = {
        'surface': {'correct': 0, 'total': 0},
        'conceptual': {'correct': 0, 'total': 0},
        'applied': {'correct': 0, 'total': 0}
    }

    for q in questions:
        difficulty = q.get('difficulty', 'surface')
        is_correct = q.get('is_correct', False)

        if difficulty in difficulty_data:
            difficulty_data[difficulty]['total'] += 1
            if is_correct:
                difficulty_data[difficulty]['correct'] += 1

    results = {}
    for diff, data in difficulty_data.items():
        accuracy = (data['correct'] / data['total']) * 100 if data['total'] > 0 else 0
        results[diff] = {'accuracy': round(accuracy, 1), 'total': data['total']}

    return results