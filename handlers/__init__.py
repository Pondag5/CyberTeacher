# handlers/__init__.py
"""CyberTeacher – обработчики команд.

Экспортируем все функции,
чтобы старый код
`from handlers import …` продолжал работать.
"""

# ── Константы & утилиты ────────────────────────────────────────
from .achievements import handle_achievements
from .core import (
    handle_commands,
)  # основной диспетчер
from .flags import handle_flag_check
from .misc import (
    handle_add_book,
    handle_course,
    handle_history,
    handle_story_mode,
    handle_terminal_log,
    handle_version,
    handle_writeup,
)
from .news import get_last_news, handle_security_news

# ── Обработчики команд ───────────────────────────────────────
from .practice import handle_container_check, handle_practice
from .quiz import (
    handle_code_review,
    handle_quiz_action,
    handle_quiz_generation,
    handle_task_action,
)
from .threats import handle_groups, handle_threat_summary, handle_threats
from .shop import handle_shop

__all__ = [
    "get_last_news",
    "handle_achievements",
    "handle_add_book",
    "handle_code_review",
    "handle_commands",
    "handle_container_check",
    "handle_course",
    "handle_flag_check",
    "handle_groups",
    "handle_history",
    "handle_practice",
    "handle_quiz_action",
    "handle_quiz_generation",
    "handle_security_news",
    "handle_story_mode",
    "handle_task_action",
    "handle_terminal_log",
    "handle_threat_summary",
    "handle_threats",
    "handle_version",
    "handle_writeup",
]
