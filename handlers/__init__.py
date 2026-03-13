# handlers/__init__.py
"""CyberTeacher – обработчики команд.

Экспортируем все функции,
чтобы старый код
`from handlers import …` продолжал работать.
"""

# ── Константы & утилиты ────────────────────────────────────────
from .core import (
    handle_commands,
    handle_mode,
)  # основной диспетчер

# ── Обработчики команд ───────────────────────────────────────
from .practice import handle_practice, handle_container_check
from .quiz      import handle_quiz_action, handle_task_action, handle_quiz_generation, handle_code_review
from .flags     import handle_flag_check
from .achievements import handle_achievements
from .threats   import handle_threats, handle_groups, handle_threat_summary
from .news      import handle_security_news, get_last_news
from .misc      import (
    handle_story_mode,
    handle_history,
    handle_course,
    handle_version,
    handle_writeup,
    handle_terminal_log,
    handle_add_book,
)

__all__ = [
    "handle_commands",
    "handle_mode",
    "handle_practice",
    "handle_container_check",
    "handle_quiz_action",
    "handle_task_action",
    "handle_quiz_generation",
    "handle_code_review",
    "handle_flag_check",
    "handle_achievements",
    "handle_threats",
    "handle_groups",
    "handle_threat_summary",
    "handle_security_news",
    "get_last_news",
    "handle_story_mode",
    "handle_history",
    "handle_course",
    "handle_version",
    "handle_writeup",
    "handle_terminal_log",
    "handle_add_book",
]