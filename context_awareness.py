"""Context Awareness — time of day, session patterns, user behavior.

Provides atmospheric context for the teacher personality system.
Detects when the user is studying and adapts behavior accordingly.
"""

import logging
from datetime import datetime, timezone
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


def _get_hour() -> int:
    """Get current hour in local timezone."""
    return datetime.now(timezone.utc).hour


def get_time_of_day() -> str:
    """Detect time of day for atmospheric adaptation.

    Returns:
        'morning'    (6-12)
        'afternoon'  (12-18)
        'evening'    (18-23)
        'night'      (23-3)
        'late_night' (3-6)
    """
    hour = _get_hour()
    if 6 <= hour < 12:
        return "morning"
    elif 12 <= hour < 18:
        return "afternoon"
    elif 18 <= hour < 23:
        return "evening"
    elif 23 <= hour or hour < 3:
        return "night"
    else:  # 3-6
        return "late_night"


TIME_OF_DAY_LABELS = {
    "morning": "утро",
    "afternoon": "день",
    "evening": "вечер",
    "night": "ночь",
    "late_night": "глубокая ночь",
}

TIME_OF_DAY_MOOD = {
    "morning": "fresh",
    "afternoon": "focused",
    "evening": "relaxed",
    "night": "quiet",
    "late_night": "hacker",
}


def get_session_duration_minutes(session_start: float) -> float:
    """Calculate session duration in minutes."""
    import time

    if session_start <= 0:
        return 0
    return (time.time() - session_start) / 60


def detect_session_pattern(
    messages_this_session: int,
    duration_minutes: float,
    hour: Optional[int] = None,
) -> str:
    """Detect user activity pattern based on behavior.

    Returns one of:
        'normal'         — standard learning session
        'binge_learning' — many messages in short time
        'night_owl'      — studying late at night
        'perfectionist'  — long session, few messages (reading carefully)
        'chaotic'        — rapid switches, many commands
    """
    if hour is None:
        hour = _get_hour()

    msgs_per_min = messages_this_session / max(duration_minutes, 1)

    if hour >= 23 or hour < 5:
        if messages_this_session > 10:
            return "night_owl"
        return "night_owl"

    if msgs_per_min > 2:
        return "binge_learning"

    if duration_minutes > 60 and messages_this_session < 5:
        return "perfectionist"

    if msgs_per_min > 1 and duration_minutes < 10:
        return "chaotic"

    return "normal"


PATTERN_LABELS = {
    "normal": "обычная сессия",
    "binge_learning": "интенсивное обучение",
    "night_owl": "ночная сессия",
    "perfectionist": "глубокое изучение",
    "chaotic": "хаотичная сессия",
}


def get_context_info(
    session_start: float = 0,
    messages_this_session: int = 0,
) -> Dict[str, Any]:
    """Build complete context awareness dict.

    Returns:
        {
            'time_of_day': str,
            'time_label': str,
            'mood': str,
            'session_pattern': str,
            'session_pattern_label': str,
            'session_duration_minutes': float,
            'is_late_night': bool,
            'is_long_session': bool,
        }
    """
    hour = _get_hour()
    tod = get_time_of_day()
    duration = get_session_duration_minutes(session_start)
    pattern = detect_session_pattern(messages_this_session, duration, hour)

    return {
        "time_of_day": tod,
        "time_label": TIME_OF_DAY_LABELS.get(tod, tod),
        "mood": TIME_OF_DAY_MOOD.get(tod, "normal"),
        "session_pattern": pattern,
        "session_pattern_label": PATTERN_LABELS.get(pattern, pattern),
        "session_duration_minutes": round(duration, 1),
        "is_late_night": tod in ("night", "late_night"),
        "is_long_session": duration > 60,
    }


def get_atmosphere_hint(context: Dict[str, Any]) -> str:
    """Generate a short atmospheric comment based on context.

    Returns a string like:
        "...утро, ранний червяк."
        "...3 часа ночи. Мы оба ещё не спим."
        "...вечер, расслабься."
    Returns empty string if no special atmosphere applies.
    """
    if context.get("is_late_night") and context.get("session_duration_minutes", 0) > 30:
        return "...3 часа ночи. Мы оба ещё не спим. Не забудь про глаза."

    if context.get("session_pattern") == "binge_learning":
        return "...ты в ударе. Не забывай делать перерывы."

    if context.get("session_pattern") == "perfectionist":
        return "...глубокое погружение. Хорошая стратегия."

    if context.get("session_pattern") == "night_owl":
        return "...ночная сессия. Осторожно с опечатками."

    return ""
