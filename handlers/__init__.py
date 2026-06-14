# handlers/__init__.py
"""CyberTeacher – обработчики команд.

Экспортируем все функции,
чтобы старый код
`from handlers import …` продолжал работать.
"""

from __future__ import annotations
from typing import Any, NamedTuple

from handlers.types import HandlerResult


# ── Константы & утилиты ────────────────────────────────────────
from .achievements import handle_achievements

# ── Обработчики команд ───────────────────────────────────────
from .code_review_v2 import handle_code_review_v2
from .core import (  # основной диспетчер
    handle_commands,
)
from .flags import handle_flag_check
from .lang import handle_lang
from .metasploit import handle_msf_action
from .misc import (
    handle_add_book,
    handle_course,
    handle_history,
    handle_story_mode,
    handle_terminal_log,
    handle_version,
    handle_writeup,
)
from .mood import handle_mood
from .news import get_last_news, handle_security_news
from .offline import handle_offline
from .pcap_analyzer import handle_pcap_action
from .practice import handle_container_check, handle_practice
from .quiz import (
    handle_code_review,
    handle_quiz_action,
    handle_quiz_generation,
    handle_task_action,
)
from .shop import handle_shop
from .threats import handle_groups, handle_threat_summary, handle_threats
from .tryhackme import handle_thm_action

__all__ = [
    "get_last_news",
    "handle_achievements",
    "handle_add_book",
    "handle_code_review",
    "handle_code_review_v2",
    "handle_commands",
    "handle_container_check",
    "handle_course",
    "handle_flag_check",
    "handle_groups",
    "handle_history",
    "handle_lang",
    "handle_mood",
    "handle_msf_action",
    "handle_offline",
    "handle_pcap_action",
    "handle_practice",
    "handle_quiz_action",
    "handle_quiz_generation",
    "handle_security_news",
    "handle_story_mode",
    "handle_task_action",
    "handle_terminal_log",
    "handle_thm_action",
    "handle_threat_summary",
    "handle_threats",
    "handle_version",
    "handle_writeup",
]
