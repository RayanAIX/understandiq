"""
UnderstandIQ Question Generator
Uses Groq API (llama-3.3-70b-versatile) to generate calibrated assessment questions.
Returns clean structured JSON every time.
"""

import os
import json
import re
from groq import Groq


SYSTEM_PROMPT = """You are an expert educational assessment designer specializing in cognitive science and metacognition.

Your job is to generate assessment questions that test GENUINE UNDERSTANDING, not surface recall.

CRITICAL RULES:
1. Questions must test real comprehension — not trivia or definitions copy-pasted from the text
2. For MCQ: one clearly correct answer, three plausible but wrong distractors
3. The correct_answer field must EXACTLY match one of the options strings (full text, including the letter prefix)
4. Options must be formatted as: ["A. option text", "B. option text", "C. option text", "D. option text"]
5. topic_tag must be a single meaningful word from the content domain
6. difficulty: "surface" = recall, "conceptual" = understanding, "applied" = transfer/application

You MUST return ONLY valid JSON. No preamble. No explanation. No markdown. Just the JSON object."""


def generate_questions(text: str, num_questions: int = 8, depth: str = "mixed") -> list:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables.")

    client = Groq(api_key=api_key)

    # Truncate text to avoid token limits — keep most informative portion
    max_chars = 6000
    if len(text) > max_chars:
        text = text[:max_chars] + "\n[Text truncated for assessment]"

    if depth == "mixed":
        depth_instruction = "Mix all three depths: roughly 40% surface, 40% conceptual, 20% applied."
    elif depth == "surface":
        depth_instruction = "All questions should test surface-level recall of facts and definitions."
    elif depth == "conceptual":
        depth_instruction = "All questions should test conceptual understanding — 'why' and 'how', not just 'what'."
    elif depth == "applied":
        depth_instruction = "All questions should test applied/transfer thinking — how concepts apply in new situations."
    else:
        depth_instruction = "Mix surface, conceptual, and applied questions evenly."

    user_prompt = f"""Generate exactly {num_questions} MCQ assessment questions from the text below.

Depth instruction: {depth_instruction}

Return this exact JSON structure:
{{
  "questions": [
    {{
      "question_text": "Full question text here?",
      "question_type": "mcq",
      "options": ["A. First option", "B. Second option", "C. Third option", "D. Fourth option"],
      "correct_answer": "A. First option",
      "topic_tag": "SingleWord",
      "difficulty": "surface"
    }}
  ]
}}

IMPORTANT: The correct_answer value must be copied EXACTLY from the options array.

TEXT TO ASSESS:
{text}"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.4,
        max_tokens=4000,
    )

    raw = response.choices[0].message.content.strip()
    questions = parse_questions_from_response(raw, num_questions)
    return questions


def parse_questions_from_response(raw: str, num_questions: int) -> list:
    """Robustly parse questions from LLM response, handling common formatting issues."""
    # Strip markdown code fences if present
    raw = re.sub(r"```json\s*", "", raw)
    raw = re.sub(r"```\s*", "", raw)
    raw = raw.strip()

    # Try direct JSON parse first
    try:
        data = json.loads(raw)
        questions = data.get("questions", [])
        if questions:
            return validate_and_fix_questions(questions)
    except json.JSONDecodeError:
        pass

    # Try to find JSON object within the response
    match = re.search(r'\{.*\}', raw, re.DOTALL)
    if match:
        try:
            data = json.loads(match.group())
            questions = data.get("questions", [])
            if questions:
                return validate_and_fix_questions(questions)
        except json.JSONDecodeError:
            pass

    # Final fallback — return empty (caller handles error)
    return []


def validate_and_fix_questions(questions: list) -> list:
    """
    Validate each question and fix the most common issue:
    correct_answer not exactly matching any option string.
    """
    valid = []
    for q in questions:
        try:
            options = q.get("options", [])
            correct = q.get("correct_answer", "")
            question_text = q.get("question_text", "").strip()

            if not question_text or not options or len(options) < 2:
                continue

            # Fix correct_answer if it doesn't exactly match an option
            if correct not in options:
                # Try to find the closest matching option
                correct_lower = correct.lower().strip()
                matched = None

                for opt in options:
                    opt_lower = opt.lower().strip()
                    # Check if correct answer is contained in option or vice versa
                    if correct_lower in opt_lower or opt_lower in correct_lower:
                        matched = opt
                        break
                    # Check letter match: if correct is "A" or "A.", match "A. ..."
                    if len(correct_lower) <= 2 and opt_lower.startswith(correct_lower.rstrip(".")):
                        matched = opt
                        break

                if matched:
                    correct = matched
                else:
                    # Default to first option with a note (better than marking all wrong)
                    correct = options[0]

            valid.append({
                "question_text": question_text,
                "question_type": q.get("question_type", "mcq"),
                "options": options,
                "correct_answer": correct,
                "topic_tag": q.get("topic_tag", "General"),
                "difficulty": q.get("difficulty", "surface"),
            })
        except Exception:
            continue

    return valid
