"""
Secret language — тайные фразы, меняющие поведение учителя.

Фразы можно писать в чат в любом диалоге.
"""

from typing import Optional

SECRET_PHRASES = {
    "echo, помоги": {
        "response": "Эхо откликается: «Смотри в /var/log/syslog. Там подсказка.»",
        "effect": "hint",
    },
    "rick, будь серьёзнее": {
        "response": "Rick вздыхает: «Ладно. Без сарказма. На сегодня.»",
        "effect": "mood_serious",
    },
    "ghost, покажи мне правду": {
        "response": "Ghost открывает скрытый лог: доступ к /ghost_log разрешён.",
        "effect": "unlock_ghost_log",
    },
    "спаси меня": {
        "response": "Учитель: «Я здесь. Ты не один. Вот подсказка: попробуй другую атаку.»",
        "effect": "hint",
    },
    "я не вернусь": {
        "response": "Долгая пауза. Учитель: «Я буду ждать. Сколько потребуется.»",
        "effect": "none",
    },
}


def detect_secret_phrase(text: str) -> Optional[dict]:
    """Проверить, содержит ли текст секретную фразу."""
    lowered = text.lower().strip()
    for phrase, data in SECRET_PHRASES.items():
        if phrase in lowered:
            return {
                "phrase": phrase,
                "response": data["response"],
                "effect": data["effect"],
            }
    return None
