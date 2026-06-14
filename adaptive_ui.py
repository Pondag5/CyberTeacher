"""Adaptive Difficulty — dynamically adjusts interface and content based on user level.

Levels:
- beginner: simplified interface, fewer commands, no cyberpsychosis, guided hints
- intermediate: normal interface, all commands, mild atmosphere
- advanced: complex topics, risk tracking, full atmosphere
- hardcore: no hints, strict timers, maximum risk, full atmosphere

Auto-promotion based on XP, achievements, and session count.
"""

from typing import Any, Dict, List, Optional


# ─── Difficulty Levels ───
DIFFICULTY_LEVELS = ["beginner", "intermediate", "advanced", "hardcore"]

DIFFICULTY_CONFIG = {
    "beginner": {
        "visible_commands": {
            "quiz",
            "lab",
            "courses",
            "help",
            "profile",
            "daily",
            "progress",
            "chat",
        },
        "hidden_commands": {
            "ctf",
            "exploits",
            "osint",
            "scan",
            "malware",
            "versus",
            "admin",
            "shodan",
            "censys",
            "pcap",
            "msf",
            "jupyter",
            "bounty",
            "phishing",
        },
        "cyberpsychosis_enabled": False,
        "hints_always": True,
        "atmosphere_level": "none",
        "difficulty_label": "\ud83e\udd13 \u041d\u043e\u0432\u0438\u0447\u043e\u043a",
        "color": "#4caf50",
        "description": "\u0423\u043f\u0440\u043e\u0449\u0451\u043d\u043d\u044b\u0439 \u0438\u043d\u0442\u0435\u0440\u0444\u0435\u0439\u0441 \u0434\u043b\u044f \u043d\u0430\u0447\u0438\u043d\u0430.",
        "max_quiz_questions": 5,
        "lab_difficulty_max": "easy",
        "hint_cooldown": 0,
    },
    "intermediate": {
        "visible_commands": set(),  # All commands visible
        "hidden_commands": set(),
        "cyberpsychosis_enabled": True,
        "hints_always": False,
        "atmosphere_level": "mild",
        "difficulty_label": "\u2696\ufe0f \u0421\u0442\u0443\u0434\u0435\u043d\u0442",
        "color": "#00B4D8",
        "description": "\u0421\u0442\u0430\u043d\u0434\u0430\u0440\u0442\u043d\u044b\u0439 \u0438\u043d\u0442\u0435\u0440\u0444\u0435\u0439\u0441.",
        "max_quiz_questions": 10,
        "lab_difficulty_max": "medium",
        "hint_cooldown": 30,
    },
    "advanced": {
        "visible_commands": set(),
        "hidden_commands": set(),
        "cyberpsychosis_enabled": True,
        "hints_always": False,
        "atmosphere_level": "full",
        "difficulty_label": "\u26a1 \u041f\u0440\u043e\u0444\u0438",
        "color": "#FF6A00",
        "description": "\u041f\u043e\u043b\u043d\u044b\u0439 \u0434\u043e\u0441\u0442\u0443\u043f \u043a\u043e \u0432\u0441\u0435\u043c \u0444\u0438\u0447\u0430\u043c.",
        "max_quiz_questions": 15,
        "lab_difficulty_max": "hard",
        "hint_cooldown": 60,
    },
    "hardcore": {
        "visible_commands": set(),
        "hidden_commands": set(),
        "cyberpsychosis_enabled": True,
        "hints_always": False,
        "atmosphere_level": "intense",
        "difficulty_label": "\ud83d\udd25 \u0425\u0430\u0440\u0434\u043a\u043e\u0440",
        "color": "#f44336",
        "description": "\u0411\u0435\u0437 \u043f\u043e\u0434\u0441\u043a\u0430\u0437\u043e\u043a. \u041c\u0430\u043a\u0441\u0438\u043c\u0430\u043b\u044c\u043d\u044b\u0439 \u0440\u0438\u0441\u043a.",
        "max_quiz_questions": 20,
        "lab_difficulty_max": "expert",
        "hint_cooldown": 300,
    },
}

# ─── Auto-promotion thresholds ───
PROMOTION_THRESHOLDS = {
    "beginner": {"xp": 500, "quizzes": 10, "labs": 3},
    "intermediate": {"xp": 2000, "quizzes": 30, "labs": 10},
    "advanced": {"xp": 5000, "quizzes": 60, "labs": 25},
}


def get_difficulty_config(level: str) -> Dict[str, Any]:
    """Get configuration for a difficulty level."""
    return DIFFICULTY_CONFIG.get(level, DIFFICULTY_CONFIG["beginner"])


def get_visible_commands(
    level: str, all_commands: Optional[List[str]] = None
) -> List[str]:
    """Get list of commands visible to this difficulty level."""
    config = get_difficulty_config(level)
    hidden = config["hidden_commands"]
    if not all_commands:
        all_commands = _get_default_commands()
    if not hidden:
        return all_commands
    return [cmd for cmd in all_commands if cmd not in hidden]


def is_command_available(command: str, level: str) -> bool:
    """Check if a command is available at this difficulty level."""
    config = get_difficulty_config(level)
    if not config["hidden_commands"]:
        return True
    return command not in config["hidden_commands"]


def get_system_prompt_prefix(level: str) -> str:
    """Get a system prompt modifier based on difficulty level."""
    if level == "beginner":
        return (
            "\n\n[DIFFICULTY: BEGINNER] Ты говоришь с начинающим. "
            "Избегай сложных терминов. Объясняй просто. "
            "Подсказывай команды: /quiz, /courses, /lab. "
            "Не упоминай киберпсихоз, взлом, эксплойты."
        )
    if level == "hardcore":
        return (
            "\n\n[DIFFICULTY: HARDCORE] Ты говоришь с экспертом. "
            "Будь лаконичен. Не объясняй очевидного. "
            "Не давай подсказок, пока не спросят. "
            "Повышай сложность вопросов."
        )
    return ""


def check_auto_promotion(state: Any) -> Optional[str]:
    """Check if user qualifies for auto-promotion. Returns new level or None."""
    current = getattr(state, "difficulty_level", "beginner")
    if current == "hardcore":
        return None

    idx = DIFFICULTY_LEVELS.index(current)
    if idx >= len(DIFFICULTY_LEVELS) - 1:
        return None

    next_level = DIFFICULTY_LEVELS[idx + 1]
    threshold = PROMOTION_THRESHOLDS.get(current, {})
    if not threshold:
        return None

    xp = getattr(state, "xp", 0)
    quizzes = getattr(state, "quizzes_taken", 0)
    labs = getattr(state, "labs_started", 0)

    if (
        xp >= threshold.get("xp", 999999)
        and quizzes >= threshold.get("quizzes", 999999)
        and labs >= threshold.get("labs", 999999)
    ):
        return next_level

    return None


def get_progress_hint(level: str, state: Any) -> Optional[str]:
    """Get a hint about how close the user is to promotion."""
    current = getattr(state, "difficulty_level", "beginner")
    if current == "hardcore":
        return None

    threshold = PROMOTION_THRESHOLDS.get(current)
    if not threshold:
        return None

    xp = getattr(state, "xp", 0)
    quizzes = getattr(state, "quizzes_taken", 0)
    labs = getattr(state, "labs_started", 0)

    parts = []
    if xp < threshold.get("xp", 0):
        needed = threshold["xp"] - xp
        parts.append(f"{needed} XP")
    if quizzes < threshold.get("quizzes", 0):
        needed = threshold["quizzes"] - quizzes
        parts.append(f"{needed} \u043a\u0432\u0438\u0437\u043e\u0432")
    if labs < threshold.get("labs", 0):
        needed = threshold["labs"] - labs
        parts.append(
            f"{needed} \u043b\u0430\u0431\u043e\u0440\u0430\u0442\u043e\u0440\u0438\u0439"
        )

    if parts:
        return f"\u0414\u043e \u0441\u043b\u0435\u0434\u0443\u044e\u0449\u0435\u0433\u043e \u0443\u0440\u043e\u0432\u043d\u044f: \u043e\u0441\u0442\u0430\u043b\u043e\u0441\u044c {', '.join(parts)}."
    return None


def _get_default_commands() -> List[str]:
    """Default command list."""
    return [
        "quiz",
        "lab",
        "courses",
        "help",
        "profile",
        "daily",
        "progress",
        "chat",
        "ctf",
        "exploits",
        "osint",
        "scan",
        "malware",
        "versus",
        "admin",
        "shodan",
        "censys",
        "pcap",
        "msf",
        "jupyter",
        "bounty",
        "phishing",
        "news",
        "threats",
        "story",
        "tracks",
        "skills",
        "achievements",
    ]
