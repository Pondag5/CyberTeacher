"""Smart Hints — suggests correct commands when user types wrong ones.

When an unknown command is entered, this module finds the closest
matching command and suggests it. Also provides interactive tutorial
for first-time users.
"""

from difflib import get_close_matches
from typing import Any, Dict, List, Optional, Tuple


# ─── Command descriptions for tutorial ───
COMMAND_GUIDE = {
    "quiz": "\ud83d\udcdd /quiz — \u0413\u0435\u043d\u0435\u0440\u0430\u0446\u0438\u044f \u043a\u0432\u0438\u0437\u043e\u0432 \u043f\u043e \u043b\u044e\u0431\u043e\u0439 \u0442\u0435\u043c\u0435",
    "courses": "\ud83d\udcda /courses — \u0421\u043f\u0438\u0441\u043e\u043a \u043a\u0443\u0440\u0441\u043e\u0432 \u043f\u043e \u043a\u0438\u0431\u0435\u0440\u0431\u0435\u0437\u043e\u043f\u0430\u0441\u043d\u043e\u0441\u0442\u0438",
    "lab": "\ud83d\udc33 /lab list — \u0421\u043f\u0438\u0441\u043e\u043a Docker-\u043b\u0430\u0431\u043e\u0440\u0430\u0442\u043e\u0440\u0438\u0439 (DVWA, Juice Shop...)",
    "profile": "\ud83d\udc64 /profile — \u0412\u0430\u0448 \u043f\u0440\u043e\u0444\u0438\u043b\u044c, XP, \u043d\u0430\u0432\u044b\u043a\u0438, \u0440\u0430\u043d\u0433",
    "stats": "\ud83d\udcca /stats — \u0420\u0430\u0441\u0448\u0438\u0440\u0435\u043d\u043d\u0430\u044f \u0441\u0442\u0430\u0442\u0438\u0441\u0442\u0438\u043a\u0430 \u0438 \u0430\u043d\u0430\u043b\u0438\u0442\u0438\u043a\u0430",
    "daily": "\ud83c\udfaf /daily — \u0415\u0436\u0435\u0434\u043d\u0435\u0432\u043d\u044b\u0439 \u043a\u0432\u0438\u0437, \u043d\u0430\u0433\u0440\u0430\u0434\u044b +XP",
    "help": "\u2753 /help — \u041f\u043e\u043a\u0430\u0437\u0430\u0442\u044c \u0432\u0441\u0435 \u043a\u043e\u043c\u0430\u043d\u0434\u044b",
    "progress": "\ud83d\udcc8 /progress — \u041f\u0440\u043e\u0433\u0440\u0435\u0441\u0441 \u043f\u043e \u043a\u0443\u0440\u0441\u0430\u043c \u0438 \u043d\u0430\u0432\u044b\u043a\u0430\u043c",
    "achievements": "\ud83c\udfc6 /achievements — \u0412\u0430\u0448\u0438 \u0434\u043e\u0441\u0442\u0438\u0436\u0435\u043d\u0438\u044f",
    "story": "\ud83d\udcdc /story — \u0421\u0442\u043e\u0440\u0438\u0447\u043d\u044b\u0439 \u0440\u0435\u043b\u0438\u043c \u043e\u0431\u0443\u0447\u0435\u043d\u0438\u044f",
    "tracks": "\ud83d\udee4\ufe0f /tracks — \u0423\u0447\u0435\u0431\u043d\u044b\u0435 \u0442\u0440\u0435\u043a\u0438",
    "doctor": "\ud83e\ude7a /doctor — \u041f\u0440\u043e\u0432\u0435\u0440\u043a\u0430 \u043f\u043e\u0434\u043a\u043b\u044e\u0447\u0435\u043d\u0438\u044f AI",
    "context": "\ud83d\udcca /context stats — \u0421\u0442\u0430\u0442\u0438\u0441\u0442\u0438\u043a\u0430 \u043a\u043e\u043d\u0442\u0435\u043a\u0441\u0442\u0430",
}

TUTORIAL_STEPS = [
    {
        "message": "\ud83d\udc4b \u0414\u043e\u0431\u0440\u043e \u043f\u043e\u0436\u0430\u043b\u043e\u0432\u0430\u0442\u044c! \u042f \u0442\u0432\u043e\u0439 AI-\u043d\u0430\u0441\u0442\u0430\u0432\u043d\u0438\u043a \u043f\u043e \u043a\u0438\u0431\u0435\u0440\u0431\u0435\u0437\u043e\u043f\u0430\u0441\u043d\u043e\u0441\u0442\u0438. \u0414\u0430\u0432\u0430\u0439\u0442\u0435 \u043d\u0430\u0447\u043d\u0451\u043c!",
        "command": "/courses",
        "hint": "\u0412\u0432\u0435\u0434\u0438\u0442\u0435 /courses \u0447\u0442\u043e\u0431\u044b \u0443\u0432\u0438\u0434\u0435\u0442\u044c \u0434\u043e\u0441\u0442\u0443\u043f\u043d\u044b\u0435 \u043a\u0443\u0440\u0441\u044b.",
    },
    {
        "message": "\ud83d\udcda \u041a\u0443\u0440\u0441\u044b \u0433\u043e\u0442\u043e\u0432\u044b. \u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u0438\u043d\u0442\u0435\u0440\u0435\u0441\u0443\u044e\u0449\u0443\u044e \u0442\u0435\u043c\u0443 \u0438 \u043d\u0430\u0447\u043d\u0451\u043c!",
        "command": "/quiz",
        "hint": "\u0422\u0435\u043f\u0435\u0440\u044c \u043f\u043e\u043f\u0440\u043e\u0431\u0443\u0439\u0442\u0435 \u043a\u0432\u0438\u0437: /quiz",
    },
    {
        "message": "\ud83d\udcc8 \u041e\u0442\u043b\u0438\u0447\u043d\u043e! \u0412\u044b \u043f\u043e\u043b\u0443\u0447\u0438\u043b\u0438 +XP. \u041f\u043e\u0441\u043c\u043e\u0442\u0440\u0438\u0442\u0435 \u043f\u0440\u043e\u0444\u0438\u043b\u044c:",
        "command": "/profile",
        "hint": "/profile \u043f\u043e\u043a\u0430\u0436\u0435\u0442 \u0432\u0430\u0448 \u043f\u0440\u043e\u0433\u0440\u0435\u0441\u0441.",
    },
    {
        "message": "\u2705 \u0422\u0443\u0442\u043e\u0440\u0438\u0430\u043b \u0437\u0430\u0432\u0435\u0440\u0448\u0435\u043d! \u0412\u0432\u043e\u0434\u0438\u0442\u0435 /help \u0434\u043b\u044f \u0441\u043f\u0438\u0441\u043a\u0430 \u0432\u0441\u0435\u0445 \u043a\u043e\u043c\u0430\u043d\u0434.",
        "command": "/help",
        "hint": "/help \u043f\u043e\u043a\u0430\u0436\u0435\u0442 \u0432\u0441\u0435 \u043a\u043e\u043c\u0430\u043d\u0434\u044b.",
    },
]


def suggest_command(
    input_text: str, available_commands: Optional[List[str]] = None
) -> Optional[str]:
    """Suggest closest matching command for a wrong input."""
    if not input_text:
        return None

    cmd = input_text.strip().lower().split()[0]

    if available_commands is None:
        available_commands = list(COMMAND_GUIDE.keys())

    # Direct match
    if cmd in available_commands:
        return None  # No suggestion needed

    # Close match
    matches = get_close_matches(cmd, available_commands, n=1, cutoff=0.5)
    if matches:
        desc = COMMAND_GUIDE.get(matches[0], "")
        return f"\ud83d\udca1 \u0412\u043e\u0437\u043c\u043e\u0436\u043d\u043e, \u0432\u044b \u0438\u043c\u0435\u043b\u0438 \u0432 \u0432\u0438\u0434\u0443 /{matches[0]}? {desc}"

    return None


def get_hint_for_command(command: str) -> Optional[str]:
    """Get a helpful hint for a known command."""
    return COMMAND_GUIDE.get(command)


def get_tutorial_step(step: int) -> Optional[Dict[str, Any]]:
    """Get tutorial step by index. Returns None when tutorial is complete."""
    if step < 0 or step >= len(TUTORIAL_STEPS):
        return None
    return TUTORIAL_STEPS[step]


def get_total_tutorial_steps() -> int:
    return len(TUTORIAL_STEPS)
