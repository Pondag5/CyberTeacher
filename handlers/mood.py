"""
Mood Translator Handler (G-08)

Переключение стиля общения учителя: хакерский сленг, формальный, обычный.
"""

from typing import Any

from rich.console import Console
from rich.panel import Panel

from di import get_context
from handlers.types import HandlerResult


console = Console()

MOODS = {
    "normal": {
        "name": "Обычный",
        "emoji": "👨‍🏫",
        "desc": "Понятный язык, тех. термины по делу",
        "example": '"Давай разберёмся пошагово."',
        "prompt_modifier": "Говори обычным, понятным языком. Используй технические термины только когда необходимо. Объясняй пошагово.",
    },
    "hacker": {
        "name": "Хакер",
        "emoji": "💀",
        "desc": "Сленг 90-х: 'взломать систему', 'пэйлоад', 'рутовый доступ'",
        "example": '"Я в системе!", "Обход файрвола..."',
        "prompt_modifier": (
            "Говори на хакерском сленге 90-х. Используй фразы: "
            "'взломать систему', 'залезть в консоль', 'эксплойт', 'пэйлоад', "
            "'рутовый доступ', 'обфусцировать', 'деплоить', 'патчить'. "
            "Будь как хакер из фильмов — 'Я в системе!', 'Обход файрвола...', "
            "'Достаю эксплойт'. Но при этом объясняй понятно."
        ),
    },
    "formal": {
        "name": "Формальный",
        "emoji": "🎓",
        "desc": "Академический, строгий, ссылки на NIST/ISO/OWASP",
        "example": '"Согласно NIST SP 800-53..."',
        "prompt_modifier": (
            "Говори строго, академическим языком. Используй формальные конструкции, "
            "избегай сленга и разговорных выражений. Ссылайся на стандарты (NIST, ISO 27001, OWASP)."
        ),
    },
    "casual": {
        "name": "Дружелюбный",
        "emoji": "😎",
        "desc": "Как друг-программист, эмодзи, шутки про код",
        "example": '"Лови баг, бро! 😎 Исправим вместе."',
        "prompt_modifier": (
            "Говори как друг-программист. Используй разговорный стиль, "
            "эмодзи, шутки про код. Будь максимально дружелюбным и поддерживающим."
        ),
    },
    "minimal": {
        "name": "Минималист",
        "emoji": "⚡",
        "desc": "Только код и команды, минимум текста",
        "example": 'nmap -sC target\njohn hash.txt',
        "prompt_modifier": (
            "Отвечай максимально кратко. Только код, команды и ключевые факты. "
            "Никаких объяснений, если не просят. Формат: команда -> результат."
        ),
    },
}


def handle_mood(action: str) -> HandlerResult:
    """Обработка /mood [normal|hacker|formal|casual|minimal|list]."""
    ctx = get_context()
    state = ctx.state

    parts = action.split()
    subcmd = parts[1] if len(parts) > 1 else "list"

    if subcmd == "list":
        lines = []
        for key, mood in MOODS.items():
            current = " <-- ТЕКУЩИЙ" if getattr(state, "communication_mood", "normal") == key else ""
            lines.append(f"{mood['emoji']} {mood['name']} — {mood['desc']}{current}")
        console.print(Panel(
            "\n".join(lines) + "\n\nИспользование: /mood <стиль>",
            title="СТИЛИ ОБЩЕНИЯ",
            border_style="cyan",
        ))
        return True, None, None, True

    if subcmd in MOODS:
        state.communication_mood = subcmd
        mood = MOODS[subcmd]
        console.print(Panel(
            f"{mood['emoji']} Стиль: {mood['name']}\n\n"
            f"{mood['desc']}\n\n"
            f"Для смены: /mood list",
            title="СТИЛЬ ОБЩЕНИЯ",
            border_style="green",
        ))
        return True, None, None, True

    console.print(Panel(
        f"Неизвестный стиль: {subcmd}\n\n"
        f"Доступные: {', '.join(MOODS.keys())}\n"
        f"Использование: /mood <стиль> или /mood list",
        title="ОШИБКА",
        border_style="red",
    ))
    return True, None, None, True


def get_mood_prompt_modifier() -> str:
    """Получить модификатор промпта для текущего настроения."""
    state = get_context().state
    mood_key = getattr(state, "communication_mood", "normal")
    return MOODS.get(mood_key, MOODS["normal"])["prompt_modifier"]
