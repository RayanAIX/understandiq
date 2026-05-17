"""Question generator using OpenRouter API."""

import json
import os
from openai import OpenAI

QUESTION_GENERATION_PROMPT = """You are an expert educational assessment designer specializing in cognitive science.

Given the following text, generate {num_questions} assessment questions.

Rules:
1. Mix question depths: {depth_instruction}
2. Questions must test genuine understanding, not just recall of specific sentences
3. For MCQ: one clearly correct answer, three plausible distractors
4. Topic tags must be one word from the actual content
5. Do not generate trivial or trick questions

Return ONLY valid JSON in this exact format:
{{
  "questions": [
    {{
      "question_text": "...",
      "question_type": "mcq",
      "options": ["A. ...", "B. ...", "C. ...", "D. ..."],
      "correct_answer": "A. ...",
      "topic_tag": "...",
      "difficulty": "surface|conceptual|applied"
    }}
  ]
}}

Text to assess:
{text}
"""

DEPTH_INSTRUCTIONS = {
    "surface": "All questions should test recall and recognition of factual information.",
    "conceptual": "All questions should test understanding of concepts, relationships, and explanations.",
    "applied": "All questions should test ability to apply knowledge to new situations, analyze cases, or solve problems.",
    "mixed": "Mix surface (recall), conceptual (understanding), and applied (transfer) questions in roughly equal proportions."
}


def generate_questions(text: str, num_questions: int, depth: str) -> list[dict]:
    """
    Generate assessment questions using OpenRouter API.

    Args:
        text: The document text to generate questions from
        num_questions: Number of questions to generate (5, 8, or 10)
        depth: Question depth - surface, conceptual, applied, or mixed

    Returns:
        List of question dictionaries
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables")

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1"
    )

    depth_instruction = DEPTH_INSTRUCTIONS.get(depth, DEPTH_INSTRUCTIONS["mixed"])

    prompt = QUESTION_GENERATION_PROMPT.format(
        num_questions=num_questions,
        depth_instruction=depth_instruction,
        text=text[:12000]
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=8000,
        response_format={"type": "json_object"}
    )

    try:
        response_text = response.choices[0].message.content.strip()
        if response_text.startswith('```json'):
            response_text = response_text[7:]
        if response_text.startswith('```'):
            response_text = response_text[3:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]

        data = json.loads(response_text.strip())
        return data.get('questions', [])

    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse OpenRouter response as JSON: {e}")
    except Exception as e:
        raise ValueError(f"Error generating questions: {e}")