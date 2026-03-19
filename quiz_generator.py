"""
Генерация квизов и заданий на основе LLM и контекста state.
"""

import json
import logging
import re
from typing import Any, Dict, Optional

from config import get_llm
from state import get_state

logger = logging.getLogger(__name__)


def extract_json_block(text: str) -> Optional[str]:
    """Извлечь JSON блок из текста (мерез ```json ... ```)."""
    match = re.search(
        r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL | re.IGNORECASE
    )
    if match:
        return match.group(1).strip()
    # Fallback: ищем первый JSON-объект
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return match.group(0).strip()
    return None


def generate_quiz_question(
    topic: str, difficulty: str = "medium"
) -> Optional[Dict[str, Any]]:
    """
    Сгенерировать вопрос квиза по теме с помощью LLM.
    Возвращает dict с полями: question, options (list), correct_answer (int), explanation.
    Или None при ошибке.
    """
    try:
        llm = get_llm()
        prompt = f"""Создай вопрос multiple choice по теме "{topic}", сложность: {difficulty}.
Ответь строго в JSON:
{{
  "question": "текст вопроса",
  "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
  "correct_answer": 0-3,
  "explanation": "объяснение"
}}"""
        response = llm.invoke(prompt)
        if hasattr(response, "content"):
            response = response.content
        json_text = extract_json_block(str(response))
        if not json_text:
            logger.warning("No JSON block in LLM response for quiz")
            return None
        data = json.loads(json_text)
        # Валидация
        required = ["question", "options", "correct_answer", "explanation"]
        if not all(k in data for k in required):
            return None
        if not isinstance(data["options"], list) or len(data["options"]) < 2:
            return None
        if not (0 <= data["correct_answer"] < len(data["options"])):
            return None
        return data
    except Exception as e:
        logger.error(f"Error generating quiz: {e}")
        return None


def generate_assignment(
    topic: str, difficulty: str = "medium"
) -> Optional[Dict[str, Any]]:
    """
    Сгенерировать практическое задание (assignment) по теме.
    Возвращает dict: title, description, steps (list), hints (list), expected_flag (str), points (int).
    """
    try:
        llm = get_llm()
        prompt = f"""Создай практическое задание по теме "{topic}"" для студента. Сложность: {difficulty}.
Сформулируй в JSON:
{{
  "title": "Название задания",
  "description": "Краткое описание цели",
  "steps": ["шаг1", "шаг2"],
  "hints": ["подсказка1", "подсказка2"],
  "expected_flag": "FLAG{...}",
  "points": 100
}}"""
        response = llm.invoke(prompt)
        if hasattr(response, "content"):
            response = response.content
        json_text = extract_json_block(str(response))
        if not json_text:
            logger.warning("No JSON block in LLM response for assignment")
            return None
        data = json.loads(json_text)
        required = ["title", "description", "steps", "hints", "expected_flag", "points"]
        if not all(k in data for k in required):
            return None
        return data
    except Exception as e:
        logger.error(f"Error generating assignment: {e}")
        return None


# Алиасы для совместимости с handlers.quiz (принимают vectordb первый аргумент)
def generate_quiz(vectordb, topic: str = None, difficulty: str = "medium"):
    """Compatibility wrapper for generate_quiz_question."""
    return generate_quiz_question(topic or "general", difficulty)


def generate_task(vectordb, category: str = None, difficulty: str = "medium"):
    """Compatibility wrapper for generate_assignment."""
    return generate_assignment(category or "general", difficulty)
