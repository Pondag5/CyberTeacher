# handlers/emotions.py — Teacher with emotions (M-19)
"""Sentiment analysis of student answers and teacher tone adaptation."""

import re
from typing import Any

from rich.console import Console
from rich.panel import Panel

from di import get_context

console = Console()

# Sentiment keywords
POSITIVE_KEYWORDS = [
    "спасибо", "понял", "круто", "отлично", "супер", "класс", "интересно",
    "здорово", "вау", "wow", "great", "thanks", "awesome", "nice",
    "разобрался", "получилось", "ура", "победа", "✅",
]

NEGATIVE_KEYWORDS = [
    "не понимаю", "сложно", "тупо", "бред", "ерунда", "плохо", "ужас",
    "не работает", "ошибка", "fail", "stupid", "bad", "hate", "confusing",
    "запутался", "ничего не ясно", "❌",
]

FRUSTRATION_KEYWORDS = [
    "бесишь", "заткнись", "идиот", "тупой", "хуй", "пизд", "ебать",
    "нахуй", "сука", "блять", "fuck", "shit", "damn", "idiot",
]

EMOTION_STATES = {
    "neutral": {
        "name": "Нейтральный",
        "emoji": "😐",
        "tone": "Стандартный тон учителя",
        "prompt_modifier": "",
    },
    "happy": {
        "name": "Радостный",
        "emoji": "😊",
        "tone": "Учитель доволен прогрессом ученика",
        "prompt_modifier": "Ученик в хорошем настроении и доволен. Будь позитивным, поддержи энтузиазм.",
    },
    "confused": {
        "name": "Озадаченный",
        "emoji": "🤔",
        "tone": "Ученик запутался — объясни проще",
        "prompt_modifier": "Ученик запутался. Объясни проще, используй аналогии, разбей на шаги.",
    },
    "frustrated": {
        "name": "Разочарованный",
        "emoji": "😤",
        "tone": "Ученик раздражён — будь терпеливее",
        "prompt_modifier": "Ученик раздражён. Будь терпеливее, не усложняй, предложи отдохнуть или сменить тему.",
    },
    "excited": {
        "name": "Взволнованный",
        "emoji": "🤩",
        "tone": "Ученик в восторге — дай более сложную задачу",
        "prompt_modifier": "Ученик в восторге! Предложи более сложную задачу или углублённую тему.",
    },
}


def analyze_sentiment(text: str) -> str:
    """Анализировать sentiment текста ученика."""
    text_lower = text.lower()

    positive_score = sum(1 for kw in POSITIVE_KEYWORDS if kw in text_lower)
    negative_score = sum(1 for kw in NEGATIVE_KEYWORDS if kw in text_lower)
    frustration_score = sum(1 for kw in FRUSTRATION_KEYWORDS if kw in text_lower)

    if frustration_score > 0:
        return "frustrated"
    if positive_score > 1:
        return "excited"
    if positive_score > 0:
        return "happy"
    if negative_score > 0:
        return "confused"
    return "neutral"


def handle_emotions(action: str) -> tuple[bool, Any | None, Any | None, bool]:
    """Manage teacher emotions."""
    ctx = get_context()
    state = ctx.state
    parts = action.split(maxsplit=1)

    if len(parts) == 1:
        current = getattr(state, "emotion_mode", "neutral")
        emotion = EMOTION_STATES.get(current, EMOTION_STATES["neutral"])

        console.print(Panel(
            f"[bold]Текущее состояние:[/bold] {emotion['emoji']} {emotion['name']}\n"
            f"[dim]{emotion['tone']}[/dim]\n\n"
            "Использование:\n"
            "  /emotions auto    — автоматический sentiment-анализ\n"
            "  /emotions set <state> — установить вручную\n"
            "  /emotions show    — показать все состояния\n\n"
            "Состояния: neutral, happy, confused, frustrated, excited",
            title="ЭМОЦИИ УЧИТЕЛЯ",
            border_style="cyan",
        ))
        return True, None, None, True

    subcommand = parts[1].lower()

    if subcommand == "auto":
        state.emotion_mode = "auto"
        ctx.save_state()
        console.print("[green]✅ Автоматический sentiment-анализ включён[/green]")
        return True, None, None, True

    if subcommand.startswith("set"):
        subparts = subcommand.split(maxsplit=1)
        if len(subparts) < 2:
            console.print("[yellow]/emotions set <state>[/yellow]")
            return True, None, None, True
        emotion_state = subparts[1].strip()
        if emotion_state not in EMOTION_STATES:
            console.print(f"[red]❌ Доступные: {', '.join(EMOTION_STATES.keys())}[/red]")
            return True, None, None, True
        state.emotion_mode = emotion_state
        ctx.save_state()
        e = EMOTION_STATES[emotion_state]
        console.print(f"[green]✅ Установлено: {e['emoji']} {e['name']}[/green]")
        return True, None, None, True

    if subcommand == "show":
        lines = []
        for eid, e in EMOTION_STATES.items():
            marker = " ← текущее" if eid == getattr(state, "emotion_mode", "neutral") else ""
            lines.append(f"  {e['emoji']} [cyan]{eid:<12}[/cyan] — {e['name']}{marker}")
            lines.append(f"     [dim]{e['tone']}[/dim]")
        console.print(Panel("\n".join(lines), title="СОСТОЯНИЯ", border_style="cyan"))
        return True, None, None, True

    console.print("[yellow]Неизвестная подкоманда. /emotions для справки.[/yellow]")
    return True, None, None, True


def get_emotion_prompt_modifier(user_input: str) -> str:
    """Get prompt modifier based on sentiment."""
    ctx = get_context()
    state = ctx.state
    emotion_mode = getattr(state, "emotion_mode", "neutral")

    if emotion_mode == "auto":
        sentiment = analyze_sentiment(user_input)
        state.emotion_mode = sentiment  # temporary, will reset
        return EMOTION_STATES.get(sentiment, {}).get("prompt_modifier", "")

    return EMOTION_STATES.get(emotion_mode, {}).get("prompt_modifier", "")


def get_emotion_status() -> dict[str, str]:
    """Get current emotion state."""
    ctx = get_context()
    state = ctx.state
    emotion_mode = getattr(state, "emotion_mode", "neutral")
    return EMOTION_STATES.get(emotion_mode, EMOTION_STATES["neutral"])
