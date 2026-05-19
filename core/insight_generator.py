"""
UnderstandIQ Insight Generator
Generates human-readable insights and recommendations from assessment results.
Pure rule-based logic — fast, reliable, no extra API call.
"""

from collections import defaultdict


def generate_insights(answers: list, accuracy: float, calibration: float, uiq_score: float) -> list:
    insights = []

    if not answers:
        return ["No answers recorded — please complete the assessment."]

    total = len(answers)
    correct = sum(1 for a in answers if a["is_correct"])
    overconfident = [a for a in answers if a.get("calibration_status") == "Overconfident"]
    underconfident = [a for a in answers if a.get("calibration_status") == "Underconfident"]
    well_calibrated = [a for a in answers if a.get("calibration_status") == "Well-calibrated"]

    # Insight 1: Overall calibration narrative
    if calibration >= 80:
        insights.append(
            f"Your confidence and accuracy are tightly aligned — you correctly identified what you knew "
            f"and what you didn't. This metacognitive awareness is genuinely rare and predicts strong long-term retention."
        )
    elif len(overconfident) > len(answers) * 0.4:
        topics = list(set(a["topic_tag"] for a in overconfident))
        topic_str = ", ".join(topics[:3])
        insights.append(
            f"Overconfidence detected in {len(overconfident)} of {total} questions — particularly around: {topic_str}. "
            f"You answered incorrectly while feeling certain. This 'Knowledge Illusion' is the most common "
            f"cause of exam failure and learning stagnation."
        )
    elif len(underconfident) > len(answers) * 0.3:
        insights.append(
            f"You underestimated yourself on {len(underconfident)} correct answers. "
            f"Your knowledge is stronger than your confidence suggests — this often reflects test anxiety "
            f"or imposter syndrome rather than an actual knowledge gap."
        )

    # Insight 2: Topic-level analysis
    topic_accuracy = defaultdict(lambda: {"correct": 0, "total": 0})
    for a in answers:
        tag = a.get("topic_tag", "General")
        topic_accuracy[tag]["total"] += 1
        if a["is_correct"]:
            topic_accuracy[tag]["correct"] += 1

    weak_topics = [(t, d) for t, d in topic_accuracy.items() if d["total"] > 1 and d["correct"] / d["total"] < 0.5]
    strong_topics = [(t, d) for t, d in topic_accuracy.items() if d["total"] > 1 and d["correct"] / d["total"] >= 0.8]

    if weak_topics:
        wt_names = ", ".join(t for t, _ in weak_topics[:2])
        insights.append(
            f"Your accuracy was below 50% in: {wt_names}. "
            f"These topics are not yet consolidated in memory — focused review here will yield the fastest improvement."
        )

    if strong_topics:
        st_names = ", ".join(t for t, _ in strong_topics[:2])
        insights.append(
            f"Strong performance in: {st_names}. "
            f"These concepts are well-understood. You can safely move to applying them in new contexts."
        )

    # Insight 3: Difficulty pattern
    by_difficulty = defaultdict(lambda: {"correct": 0, "total": 0})
    for a in answers:
        diff = a.get("difficulty", "surface")
        by_difficulty[diff]["total"] += 1
        if a["is_correct"]:
            by_difficulty[diff]["correct"] += 1

    surface_acc = _pct(by_difficulty["surface"])
    conceptual_acc = _pct(by_difficulty["conceptual"])
    applied_acc = _pct(by_difficulty["applied"])

    if by_difficulty["surface"]["total"] > 0 and by_difficulty["conceptual"]["total"] > 0:
        if surface_acc >= 70 and conceptual_acc < 50:
            insights.append(
                f"You recall facts well ({surface_acc:.0f}% on surface questions) but struggle with "
                f"conceptual reasoning ({conceptual_acc:.0f}% on conceptual questions). "
                f"This is the classic gap between memorization and genuine understanding."
            )
        elif conceptual_acc >= 70:
            insights.append(
                f"Strong conceptual reasoning detected ({conceptual_acc:.0f}% accuracy on deeper questions). "
                f"Your understanding goes beyond surface recall — a strong signal of durable learning."
            )

    # Insight 4: Confidence trend
    avg_conf = sum(a["confidence_rating"] for a in answers) / total
    if avg_conf >= 4.0 and accuracy < 60:
        insights.append(
            f"Your average confidence was {avg_conf:.1f}/5 — but your accuracy was only {accuracy:.0f}%. "
            f"This high-confidence, low-accuracy pattern is the strongest predictor of future learning problems. "
            f"Treating this material as familiar when it isn't prevents deeper encoding."
        )
    elif avg_conf <= 2.5 and accuracy >= 65:
        insights.append(
            f"You scored {accuracy:.0f}% while averaging only {avg_conf:.1f}/5 in confidence. "
            f"You know more than you think. Building awareness of your own competence is the next step."
        )

    return insights[:5] if insights else ["Assessment complete. Review the question breakdown for detailed feedback."]


def generate_recommendations(answers: list, accuracy: float, calibration: float, insights: list) -> list:
    recs = []

    overconfident = [a for a in answers if a.get("calibration_status") == "Overconfident"]
    underconfident = [a for a in answers if a.get("calibration_status") == "Underconfident"]

    if accuracy < 50:
        recs.append(
            "Return to the source material and read actively — highlight key concepts and write one-sentence "
            "summaries for each section before testing again."
        )
    elif accuracy < 70:
        recs.append(
            "You have a partial grasp of this material. Focus your review on the incorrectly answered questions "
            "specifically — don't re-read everything, target the gaps."
        )
    else:
        recs.append(
            "Your accuracy is solid. The next level is application — try using these concepts to solve a novel "
            "problem or explain the material to someone else without notes."
        )

    if len(overconfident) >= 2:
        topics = list(set(a["topic_tag"] for a in overconfident))
        recs.append(
            f"For topics where you were overconfident ({', '.join(topics[:3])}): practice the 'explain it from scratch' "
            f"technique. If you can't explain a concept without the source material, you don't yet understand it."
        )

    if len(underconfident) >= 2:
        recs.append(
            "Your calibration shows underconfidence — you know more than you feel you do. "
            "Practice low-stakes retrieval: write down everything you remember about each topic before checking. "
            "This builds accurate self-assessment over time."
        )

    if calibration < 60:
        recs.append(
            "Before your next study session, try predicting your score before you start. "
            "This metacognitive habit trains your brain to monitor its own understanding in real time."
        )

    return recs[:3]


def _pct(d: dict) -> float:
    if d["total"] == 0:
        return 0.0
    return (d["correct"] / d["total"]) * 100
