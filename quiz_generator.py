"""
Генерация квизов и заданий на основе LLM и контекста state.
"""

import json
import logging
from typing import Any, Optional

from config import get_llm
from state import get_state
from utils.common import extract_json_block

logger = logging.getLogger(__name__)


def generate_quiz_question(
    topic: str, difficulty: str = "medium"
) -> Optional[dict[str, Any]]:
    state = get_state()
    if state.offline_mode:
        logger.info("Offline mode: quiz generation skipped")
        return None
    try:
        llm = get_llm()
        if llm is None:
            logger.warning("LLM not available for quiz generation")
            return None
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
        if not all(
            k in data for k in ["question", "options", "correct_answer", "explanation"]
        ):
            return None
        if not isinstance(data["options"], list) or len(data["options"]) < 2:
            return None
        if not (0 <= data["correct_answer"] < len(data["options"])):
            return None
        result: dict[str, Any] = data
        return result
    except Exception as e:
        logger.error(f"Error generating quiz: {e}")
        return None


def generate_assignment(
    topic: str, difficulty: str = "medium"
) -> Optional[dict[str, Any]]:
    state = get_state()
    if state.offline_mode:
        logger.info("Offline mode: assignment generation skipped")
        return None
    try:
        llm = get_llm()
        if llm is None:
            logger.warning("LLM not available for assignment generation")
            return None
        prompt = f"""Создай практическое задание по теме "{topic}" для студента. Сложность: {difficulty}.
Сформулируй в JSON:
{{
  "title": "Название задания",
  "description": "Краткое описание цели",
  "steps": ["шаг1", "шаг2"],
  "hints": ["подсказка1", "подсказка2"],
  "expected_flag": "FLAG{{...}}",
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
        result: dict[str, Any] = data
        return result
    except Exception as e:
        logger.error(f"Error generating assignment: {e}")
        return None


def generate_quiz(vectordb, topic: str | None = None, difficulty: str = "medium"):
    return generate_quiz_question(topic or "general", difficulty)


def generate_task(vectordb, category: str | None = None, difficulty: str = "medium"):
    return generate_assignment(category or "general", difficulty)
