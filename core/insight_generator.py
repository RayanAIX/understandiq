"""Insight generator using rule-based logic and OpenRouter API."""

import json
import os
from openai import OpenAI
from typing import List, Dict
from .scoring_engine import analyze_topic_performance, analyze_difficulty_performance


INSIGHT_GENERATION_PROMPT = """You are a cognitive assessment expert. Based on these results, generate 3-4 precise,
honest insights about this learner's understanding. Be specific to their data.
Do not be generic. Reference their actual performance patterns.

Results data:
{results_json}

Return only a JSON array of insight strings. Example:
["insight 1", "insight 2", "insight 3"]
"""


def generate_insights(questions: List[Dict], accuracy: float, calibration: float,
                     understandiq_score: float) -> List[str]:
    """
    Generate natural language insights based on assessment results.

    Uses rule-based logic first, then enhances with Gemini if available.

    Args:
        questions: List of question dicts with answers
        accuracy: Accuracy score
        calibration: Calibration score
        understandiq_score: Composite score

    Returns:
        List of insight strings
    """
    insights = []

    topic_perf = analyze_topic_performance(questions)
    difficulty_perf = analyze_difficulty_performance(questions)

    overconfident_topics = []
    underconfident_topics = []
    accurate_topics = []

    for topic, data in topic_perf.items():
        if data['avg_confidence'] > 3.5 and data['accuracy'] < 60:
            overconfident_topics.append(topic)
        elif data['avg_confidence'] < 2.5 and data['accuracy'] > 70:
            underconfident_topics.append(topic)
        elif data['accuracy'] >= 80:
            accurate_topics.append(topic)

    if accuracy >= 85 and calibration >= 80:
        insights.append(
            "Your accuracy and calibration are both strong — you know the material and you know what you know. This metacognitive precision is rare and indicates deep understanding."
        )
    elif accuracy >= 70 and calibration < 50:
        gap = accuracy - calibration
        insights.append(
            f"You scored {accuracy}% accuracy but your confidence was calibrated to around {calibration}%. That {gap}% gap is the 'Illusion of Understanding' — you performed reasonably but overestimated your knowledge."
        )
    elif accuracy < 50 and calibration > 70:
        insights.append(
            "You showed strong awareness of what you don't know — your confidence accurately reflected lower performance. This metacognitive honesty is actually a good foundation for learning."
        )
    elif accuracy < 50 and calibration < 50:
        insights.append(
            "Both accuracy and calibration are low — you're uncertain about material you also don't know well. This is a foundational gap zone; building core knowledge should be your priority."
        )

    if overconfident_topics:
        topics_str = ", ".join(overconfident_topics)
        insights.append(
            f"You were most overconfident in questions tagged '{topics_str}' — this is where your surface-level knowledge may be masking conceptual gaps."
        )

    if 'surface' in difficulty_perf and 'conceptual' in difficulty_perf:
        surface_acc = difficulty_perf['surface']['accuracy']
        conceptual_acc = difficulty_perf['conceptual']['accuracy']

        if surface_acc >= 80 and conceptual_acc < 60:
            insights.append(
                f"Your accuracy on surface questions was {surface_acc}%, but dropped to {conceptual_acc}% on conceptual questions. You recall well but struggle with deeper understanding."
            )
        elif conceptual_acc >= surface_acc + 20:
            insights.append(
                "You perform better on conceptual questions than surface recall — you prefer understanding over memorizing. Consider building more factual anchors to support your reasoning."
            )

    if 'applied' in difficulty_perf:
        applied_acc = difficulty_perf['applied']['accuracy']
        if applied_acc < 50:
            insights.append(
                f"Applied questions (only {applied_acc}% accuracy) reveal difficulty transferring knowledge to new contexts. Practice with real-world scenarios would help bridge this gap."
            )
        elif applied_acc >= 80:
            insights.append(
                "Strong performance on applied questions shows you can transfer knowledge to new situations — this is a hallmark of genuine understanding versus rote memorization."
            )

    overconfident_count = sum(
        1 for q in questions
        if q.get('confidence_rating', 3) >= 4 and not q.get('is_correct', False)
    )
    underconfident_count = sum(
        1 for q in questions
        if q.get('confidence_rating', 3) <= 2 and q.get('is_correct', False)
    )

    if overconfident_count > len(questions) * 0.3:
        insights.append(
            f"You showed overconfidence in {overconfident_count} questions — answering incorrectly while feeling certain. Be wary of these 'knowledge illusions'."
        )
    if underconfident_count > len(questions) * 0.3:
        insights.append(
            f"You underconfident in {underconfident_count} questions — answering correctly while doubting yourself. Trust your preparation more."
        )

    if len(insights) < 3:
        try:
            enhanced_insights = enhance_insights_with_gemini(
                questions, accuracy, calibration, understandiq_score
            )
            if enhanced_insights:
                insights = insights[:2] + enhanced_insights[:3-len(insights)]
        except Exception:
            pass

    return insights[:5]


def enhance_insights_with_gemini(questions: List[Dict], accuracy: float,
                                   calibration: float, score: float) -> List[str]:
    """Use OpenRouter to generate additional insights."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return []

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1"
    )

    results_data = {
        'accuracy': accuracy,
        'calibration': calibration,
        'understandiq_score': score,
        'total_questions': len(questions),
        'topic_performance': analyze_topic_performance(questions),
        'difficulty_performance': analyze_difficulty_performance(questions)
    }

    prompt = INSIGHT_GENERATION_PROMPT.format(
        results_json=json.dumps(results_data, indent=2)
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"}
    )

    try:
        text = response.choices[0].message.content.strip()
        if text.startswith('```json'):
            text = text[7:]
        if text.startswith('```'):
            text = text[3:]
        if text.endswith('```'):
            text = text[:-3]

        insights = json.loads(text.strip())
        return [str(i) for i in insights if isinstance(i, str)]
    except Exception:
        return []


def generate_recommendations(questions: List[Dict], accuracy: float,
                               calibration: float, insights: List[str]) -> List[str]:
    """
    Generate actionable recommendations based on results.

    Args:
        questions: List of question dicts
        accuracy: Accuracy score
        calibration: Calibration score
        insights: Generated insights

    Returns:
        List of recommendation strings
    """
    recommendations = []
    topic_perf = analyze_topic_performance(questions)

    overconfident_topics = [
        topic for topic, data in topic_perf.items()
        if data['avg_confidence'] > 3.5 and data['accuracy'] < 60
    ]

    if overconfident_topics:
        recommendations.append(
            f"Re-read the sections on {', '.join(overconfident_topics)} and try to explain "
            "each concept to someone without looking at notes. Teaching reveals gaps."
        )

    if calibration < 50:
        recommendations.append(
            "Before answering, pause 3 seconds to genuinely assess your certainty. "
            "This practice builds metacognitive awareness over time."
        )

    if accuracy >= 80 and calibration >= 70:
        recommendations.append(
            "Move to applied exercises and case studies — your understanding foundation "
            "is solid, now test transfer to new contexts."
        )

    if accuracy < 50:
        recommendations.append(
            "Start with core definitions and key concepts before testing again. "
            "Build factual anchors before attempting conceptual integration."
        )

    if 'applied' in [q.get('difficulty') for q in questions]:
        applied_correct = sum(
            1 for q in questions
            if q.get('difficulty') == 'applied' and q.get('is_correct', False)
        )
        if applied_correct < len([q for q in questions if q.get('difficulty') == 'applied']) * 0.5:
            recommendations.append(
                "Practice applying concepts through real-world examples or problems. "
                "Application bridges abstract knowledge to practical understanding."
            )

    weak_topics = [
        topic for topic, data in topic_perf.items()
        if data['accuracy'] < 60
    ]
    if weak_topics:
        recommendations.append(
            f"Focus study time on {', '.join(weak_topics)} — these topics show the most "
            "knowledge gaps and should be prioritized in review."
        )

    return recommendations[:3]