"""Общие утилиты для повторного использования во всём проекте."""

import json
import re
from typing import Any


def extract_json_block(text: str) -> str | None:
    """Извлечь первый JSON-блок из текста (stack-based парсер).

    Корректно обрабатывает вложенные объекты.
    """
    if not text:
        return None
    stack = []
    start = None
    for i, ch in enumerate(text):
        if ch == "{":
            if start is None:
                start = i
            stack.append(ch)
        elif ch == "}":
            if stack:
                stack.pop()
                if not stack:
                    end = i + 1
                    return text[start:end]
    return None


def parse_json_response(message: Any) -> dict:
    """Извлечь и распарсить JSON из ответа LLM.

    Принимает str или AIMessage, возвращает dict (пустой при ошибке).
    """
    if hasattr(message, "content"):
        text = str(message.content)
    else:
        text = str(message)

    # Попробовать найти markdown-блок
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL | re.IGNORECASE)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass

    # Fallback: stack-based парсер
    json_str = extract_json_block(text)
    if json_str:
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            pass

    return {}


def ask_confirm(message: str) -> bool:
    """Спросить подтверждение у пользователя."""
    try:
        from rich.prompt import Confirm

        return Confirm.ask(message)
    except Exception:
        resp = input(f"{message} (yn): ").strip().lower()
        return resp in ("y", "yes", "true", "1")


def clear_chat_db(conn: Any) -> None:
    """Очистить историю чата в БД."""
    try:
        from memory import clear_chat as db_clear_chat

        db_clear_chat(conn)
    except Exception:
        pass


def check_open_answer_heuristic(
    question: str,
    user_ans: str,
    key_points: list[str] | None = None,
) -> dict[str, Any]:
    """Эвристическая проверка ответа по ключевым словам.

    Не использует LLM, работает мгновенно.
    """
    score = 0
    feedback = "Спасибо за ответ."
    if user_ans and len(user_ans.strip()) > 0:
        score = 6
        if "правильно" in user_ans.lower() or "верно" in user_ans.lower():
            score = 9
            feedback = "Отлично!"
    if key_points:
        found = 0
        upp = user_ans.lower() if user_ans else ""
        for kp in key_points:
            if kp.lower() in upp:
                found += 1
        if found >= max(1, len(key_points) // 2):
            score = min(10, score + 2)
            feedback = "Частично на ключевых моментах."
    return {"score": score, "feedback": feedback}
