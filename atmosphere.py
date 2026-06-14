"""Atmosphere system — Ghost logs, Echo of past sessions, Teacher's doubt.

Three atmospheric layers that make the world feel alive:

1. Ghost Logs: rare system messages that appear unprompted,
   creating the illusion the system has its own life.
   Tied to cyberpsychosis level — more frequent at higher levels.

2. Echo of Past Sessions: the teacher occasionally remembers
   significant past events from episode memory, creating continuity.

3. Teacher's Doubt: the teacher occasionally expresses uncertainty,
   creating an illusion of internal conflict.
"""

import random
import time
from typing import Any, Dict, List, Optional


# ─── Ghost Logs ───
GHOST_LOGS: List[Dict[str, Any]] = [
    {
        "text": "[SYSTEM] Неопознанный запрос к порту 443... заблокирован.",
        "level": "normal",
        "weight": 3,
    },
    {"text": "[GHOST] Они знают, что ты здесь.", "level": "elevated", "weight": 1},
    {"text": "[SYSTEM] Шифрование сессии обновлено.", "level": "normal", "weight": 5},
    {"text": "[GHOST] Визит в страну... отмечен.", "level": "elevated", "weight": 1},
    {
        "text": "[SYSTEM] Аномалия в сетевом трафике. Источник неизвестен.",
        "level": "elevated",
        "weight": 2,
    },
    {"text": "[GHOST] Кто-то смотрит через стену.", "level": "critical", "weight": 1},
    {"text": "[SYSTEM] Пакет отброшен. Флаги: 0x1F.", "level": "normal", "weight": 4},
    {
        "text": "[GHOST] Тень на границе сети... исчезла.",
        "level": "elevated",
        "weight": 1,
    },
    {
        "text": "[SYSTEM] Reverse DNS lookup завершён. Результат: NULL.",
        "level": "normal",
        "weight": 3,
    },
    {
        "text": "[GHOST] Тот, кто пришёл раньше тебя, оставил след.",
        "level": "critical",
        "weight": 1,
    },
    {
        "text": "[SYSTEM] Неожиданный SYN-пакет. Сброс соединения.",
        "level": "elevated",
        "weight": 2,
    },
    {
        "text": "[GHOST] Шифрование сломано... нет, это была ложная тревога.",
        "level": "normal",
        "weight": 3,
    },
    {
        "text": "[SYSTEM] ARP-таблица обновлена. Новое устройство в сегменте.",
        "level": "normal",
        "weight": 4,
    },
    {
        "text": "[GHOST] Они уже здесь. Но пока наблюдают.",
        "level": "critical",
        "weight": 1,
    },
    {
        "text": "[SYSTEM] Heartbeat принят. Система стабильна... пока.",
        "level": "normal",
        "weight": 5,
    },
]


# ─── Echo Templates ───
ECHO_TEMPLATES: List[str] = [
    "Помнишь, как ты {action} в прошлый раз? Интересно, получится ли лучше.",
    "Хм, {action}... Я вспомнил, как ты тогда справлялся.",
    "О, снова {action}! В прошлый раз ты {result}. Надеюсь, на этот раз лучше.",
    "Знакомо... {action}. Давай проверим, помнишь ли ты основы.",
    "{action} — эх, в прошлый раз были проблемы с {issue}.",
    "Ты уже {action}, и тогда {result}. Хочешь попробовать по-другому?",
    "Интересно, помнишь {action}? Тогда {result}.",
]


# ─── Teacher Doubt Templates ───
DOUBT_TEMPLATES: List[str] = [
    "Хм... я не уверен, что это хорошая идея. Но если ты настаиваешь...",
    "Подожди. Ты уверен? Это может иметь последствия.",
    "Стоп. Я сомневаюсь в безопасности этого шага. Но решение за тобой.",
    "Мне не нравится, как это выглядит. Но ты здесь хозяин.",
    "Знаешь, я бы на твоём месте подумал дважды. Но кто я такой, чтобы запрещать.",
    "Это... рискованно. Я не говорю «нет», но предупреждаю.",
    "Я чуть было не сказал «не делай этого». Но ты взрослый.",
    "Мне кажется, здесь есть подводные камни. Или это только мне кажется?",
]


class AtmosphereEngine:
    """Generates atmospheric content based on world state."""

    def __init__(self) -> None:
        self._last_ghost_time: float = 0.0
        self._ghost_interval: float = 300.0  # 5 minutes between ghost logs
        self._session_messages: int = 0

    def should_show_ghost_log(self, cyberpsychosis_level: str) -> bool:
        """Determine if a ghost log should appear now."""
        now = time.time()
        if now - self._last_ghost_time < self._ghost_interval:
            return False

        # Probability increases with cyberpsychosis
        probs = {
            "normal": 0.02,
            "elevated": 0.08,
            "critical": 0.15,
            "dangerous": 0.30,
        }
        if random.random() < probs.get(cyberpsychosis_level, 0.02):
            self._last_ghost_time = now
            # More frequent at higher levels
            self._ghost_interval = max(
                60,
                300
                - int(cyberpsychosis_level == "critical") * 120
                - int(cyberpsychosis_level == "dangerous") * 200,
            )
            return True
        return False

    def get_ghost_log(self, cyberpsychosis_level: str) -> Optional[str]:
        """Get a random ghost log appropriate for the current level."""
        level_order = {"normal": 0, "elevated": 1, "critical": 2, "dangerous": 3}
        max_level = level_order.get(cyberpsychosis_level, 0)

        eligible = [
            gl for gl in GHOST_LOGS if level_order.get(gl["level"], 0) <= max_level
        ]

        if not eligible:
            return None

        # Weighted random selection
        weights = [gl["weight"] for gl in eligible]
        selected: Dict[str, Any] = random.choices(eligible, weights=weights, k=1)[0]
        result: str = selected["text"]
        return result

    def get_echo(self, memorable_events: List[Dict[str, Any]]) -> Optional[str]:
        """Generate a teacher echo referencing a past event."""
        if not memorable_events:
            return None

        # 15% chance per message
        if random.random() > 0.15:
            return None

        event: Dict[str, Any] = random.choice(memorable_events)
        action: str = event.get("action", "занимался кибербезопасностью")
        result: str = event.get("result", "справился")
        issue: str = event.get("issue", "ошибками")

        template: str = random.choice(ECHO_TEMPLATES)
        return template.format(action=action, result=result, issue=issue)

    def should_show_doubt(self, stress: float, recklessness: float) -> bool:
        """Determine if teacher should express doubt.

        More likely at higher stress + recklessness.
        """
        base_prob = 0.03
        if stress > 60:
            base_prob += 0.05
        if recklessness > 70:
            base_prob += 0.07
        if stress > 80 and recklessness > 80:
            base_prob += 0.10
        return random.random() < base_prob

    def get_doubt(self) -> str:
        """Get a random teacher doubt expression."""
        return random.choice(DOUBT_TEMPLATES)

    def increment_session(self) -> None:
        self._session_messages += 1


# Singleton
_atmosphere: Optional[AtmosphereEngine] = None


def get_atmosphere() -> AtmosphereEngine:
    global _atmosphere
    if _atmosphere is None:
        _atmosphere = AtmosphereEngine()
    return _atmosphere


# ─── Integration helpers for main.py ───


def maybe_get_atmospheric_message(
    cyberpsychosis_level: str = "normal",
    stress: float = 0.0,
    recklessness: float = 0.0,
    memorable_events: Optional[List[Dict[str, Any]]] = None,
) -> Optional[str]:
    """Maybe generate an atmospheric message. Called periodically in the main loop.

    Returns a string to append to the conversation, or None.
    """
    eng = get_atmosphere()
    eng.increment_session()

    # Ghost log
    if eng.should_show_ghost_log(cyberpsychosis_level):
        ghost = eng.get_ghost_log(cyberpsychosis_level)
        if ghost:
            return ghost

    # Echo of past sessions
    if memorable_events:
        echo = eng.get_echo(memorable_events)
        if echo:
            return f"[Учитель, pro se] {echo}"

    # Teacher's doubt
    if eng.should_show_doubt(stress, recklessness):
        doubt = eng.get_doubt()
        return f"[Учитель] {doubt}"

    return None
