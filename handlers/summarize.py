# handlers/summarize.py — Summarization истории чата (M-22)
"""Автосворачивание истории каждые N сообщений через LLM."""

import logging
from typing import Any

from rich.console import Console
from rich.panel import Panel

from state import get_state

console = Console()
logger = logging.getLogger(__name__)

SUMMARY_INTERVAL = 20  # сообщений между суммаризациями


def handle_summarize(action: str) -> tuple[bool, Any | None, Any | None, bool]:
    """Ручная суммаризация истории."""
    try:
        from memory import get_chat_history

        history = get_chat_history(limit=50)
        if len(history) < 5:
            console.print("[yellow]История слишком короткая для суммаризации[/yellow]")
            return True, None, None, True

        summary = _generate_summary(history)
        if summary:
            console.print(Panel(summary, title="📝 СУММАРИЗАЦИЯ", border_style="cyan"))
        else:
            console.print("[red]Не удалось сгенерировать суммаризацию[/red]")
    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
    return True, None, None, True


def _generate_summary(history: list[dict]) -> str | None:
    """Сгенерировать суммаризацию через LLM."""
    from config import LazyLoader

    llm = LazyLoader.get_llm()
    if llm is None:
        return None

    # Берём последние 30 сообщений для контекста
    recent = history[-30:]
    context = "\n".join([f"{m['role']}: {m['content'][:150]}" for m in recent])

    prompt = f"""Ты — учитель кибербезопасности. Сделай краткое резюме диалога с учеником.
Выдели:
1. Какие темы обсуждались
2. Что ученик изучил
3. Какие были проблемы/ошибки
4. Рекомендации на будущее

Диалог:
{context}

Ответь кратко (3-5 предложений) на русском."""

    try:
        response = llm.invoke(prompt)
        return response.content if hasattr(response, "content") else str(response)
    except Exception as e:
        logger.error(f"Summarization failed: {e}")
        return None


def check_auto_summarize(conn) -> None:
    """Проверить, нужна ли автосуммаризация (вызывается после каждого сообщения)."""
    try:
        from memory import get_chat_history

        state = get_state()
        msg_count = getattr(state, "_msg_count_since_summary", 0)
        msg_count += 1

        if msg_count >= SUMMARY_INTERVAL:
            history = get_chat_history(conn, limit=SUMMARY_INTERVAL)
            if len(history) >= 10:
                summary = _generate_summary(history)
                if summary:
                    console.print(Panel(
                        summary,
                        title="📝 АВТО-СУММАРИЗАЦИЯ",
                        border_style="dim",
                    ))
                    # Сохраняем суммаризацию в историю
                    from memory import save_message
                    save_message(conn, "system", f"[SUMMARY] {summary}", "teacher")
            msg_count = 0

        state._msg_count_since_summary = msg_count
    except Exception as e:
        logger.debug(f"Auto-summarize check failed: {e}")
