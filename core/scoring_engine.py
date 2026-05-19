"""
UnderstandIQ Scoring Engine
Calculates accuracy, calibration, and composite UnderstandIQ scores.
"""


def calculate_accuracy_score(answers: list) -> float:
    if not answers:
        return 0.0
    correct = sum(1 for a in answers if a.get("is_correct", False))
    return (correct / len(answers)) * 100


def calculate_calibration_score(answers: list) -> float:
    """
    For each question:
      conf_pct = (confidence 1-5 → 0-100)
      correct_pct = 100 if correct else 0
      gap = abs(conf_pct - correct_pct)
    Calibration = 100 - mean(gaps)
    """
    if not answers:
        return 0.0
    gaps = []
    for a in answers:
        conf = a.get("confidence_rating", 3)
        conf_pct = ((conf - 1) / 4) * 100
        correct_pct = 100.0 if a.get("is_correct", False) else 0.0
        gaps.append(abs(conf_pct - correct_pct))
    return max(0.0, 100.0 - (sum(gaps) / len(gaps)))


def calculate_understandiq_score(accuracy: float, calibration: float) -> float:
    return (accuracy * 0.5) + (calibration * 0.5)


def get_level_name(score: float) -> tuple:
    if score >= 85:
        return ("Calibrated Mastery", "High accuracy with well-calibrated confidence — you know what you know.")
    elif score >= 70:
        return ("Solid Understanding", "Good accuracy with minor calibration gaps. Strong foundation.")
    elif score >= 55:
        return ("Surface Knowledge", "Moderate accuracy but overconfidence detected in key areas.")
    elif score >= 40:
        return ("Knowledge Illusion", "Significant gap between confidence and actual performance.")
    else:
        return ("Foundational Gap", "Low accuracy with overconfidence — the highest-risk cognitive state.")


def get_calibration_status(answer: dict) -> str:
    conf = answer.get("confidence_rating", 3)
    correct = answer.get("is_correct", False)
    if conf >= 4 and not correct:
        return "Overconfident"
    elif conf <= 2 and correct:
        return "Underconfident"
    else:
        return "Well-calibrated"
