"""Real-time hints system (M-30)"""

import json
import os
import re
import time
from typing import Any

from rich.console import Console
from rich.panel import Panel

from config import get_llm
from state import get_state

console = Console()

# Default patterns (can be extended from hints/patterns.json)
DEFAULT_PATTERNS = [
    {
        "regex": r"""['"]\s*OR\s*['"]?1['"]?\s*=\s*['"]?1['"]""",
        "hint": "💡 Попробуй добавить `UNION SELECT` для извлечения данных",
        "tags": ["sqli"],
    },
    {
        "regex": r"nmap\s+-p-",
        "hint": "💡 Сканирование всех 65535 портов очень долгое. Уточни диапазон: `-p 1-1000` или используй `-sV` для определения служб",
        "tags": ["recon"],
    },
    {
        "regex": r"sqlmap\s+-u\s+\S+\s+--dbs",
        "hint": "💡 Хорошо! После определения БД, используй `--tables` для списка таблиц, затем `--dump` для извлечения данных",
        "tags": ["sqli"],
    },
    {
        "regex": r"gobuster\s+dir\s+-u\s+\S+\s+-w\s+\S+",
        "hint": "💡 Если находишь `/admin`, попробуй `/admin.php`, `/admin/login`. Также добавь `-x .php,.txt` для расширений",
        "tags": ["recon"],
    },
    {
        "regex": r"curl\s+(http|https)://.*\?id=\d+",
        "hint": "💡 Параметр `id` часто уязвим к SQLi. Попробуй `id=1' OR '1'='1`",
        "tags": ["sqli"],
    },
    {
        "regex": r"<\s*script\s*>",
        "hint": "💡 Для XSS попробуй `<script>alert(1)</script>` или `<img src=x onerror=alert(1)>`",
        "tags": ["xss"],
    },
    {
        "regex": r"burp|proxy|intercept",
        "hint": "💡 Не забудь включить proxying в браузере и forwarded requests в Burp",
        "tags": ["proxy"],
    },
    {
        "regex": r"hydra\s+-l\s+\S+\s+-P\s+\S+\s+\S+\s+\S+",
        "hint": "💡 Если brute force не работает, попробуй найти правильный логин через рекогносцировку или используй `--username` для перебора только логинов",
        "tags": ["bruteforce"],
    },
]


def _load_patterns() -> list[dict]:
    """Load hint patterns from hints/patterns.json or use defaults."""
    patterns_path = os.path.join("hints", "patterns.json")
    if os.path.exists(patterns_path):
        try:
            with open(patterns_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
        except Exception:
            pass
    return DEFAULT_PATTERNS


def generate_contextual_hint(user_input: str, context: dict[str, Any]) -> str | None:
    """Generate a hint based on user input patterns.

    Args:
        user_input: The command/user typed
        context: Learning context (current_mission, active_lab, etc.)

    Returns:
        Hint string or None if no hint applicable
    """
    state = get_state()
    patterns = _load_patterns()

    # Convert to lowercase for matching (but keep case in regex where needed)
    input_lower = user_input.lower()

    for p in patterns:
        try:
            if re.search(p["regex"], user_input, re.IGNORECASE):
                return p["hint"]
        except re.error:
            continue

    # If no pattern match, we could use LLM to generate a generic hint based on context
    # But to avoid unnecessary LLM calls, we'll return None here
    # Later we can add LLM fallback with rate limiting
    return None


def handle_hint(action: str) -> tuple[bool, None, None, bool]:
    """Handle /hint commands.

    Commands:
    - /hint on/off — enable/disable automatic hints
    - /hints — show statistics
    - /hint get — manually request a hint (uses credit)
    - /hint clear — reset counters
    """
    parts = action.split(maxsplit=1)
    subcmd = parts[1].lower() if len(parts) > 1 else "status"

    state = get_state()

    # Initialize hint fields if not present
    if not hasattr(state, "hint_enabled"):
        state.hint_enabled = True
    if not hasattr(state, "hint_credits"):
        state.hint_credits = 3  # default credits
    if not hasattr(state, "hints_used"):
        state.hints_used = 0
    if not hasattr(state, "last_hint_time"):
        state.last_hint_time = 0
    if not hasattr(state, "hint_cooldown"):
        state.hint_cooldown = 30  # seconds

    if subcmd in ("on", "enable", "вкл"):
        state.hint_enabled = True
        console.print("[green]✅ Автоматические подсказки включены[/green]")
        return True, None, None, True

    elif subcmd in ("off", "disable", "выкл"):
        state.hint_enabled = False
        console.print("[yellow]⚠️ Автоматические подсказки выключены[/yellow]")
        return True, None, None, True

    elif subcmd in ("status", "stats", "статус"):
        console.print(
            Panel(
                f"""[bold]📊 Статистика подсказок[/bold]

Автоматические: {"✅ Вкл" if state.hint_enabled else "❌ Выкл"}
Кредитов: {state.hint_credits}
Использовано: {state.hints_used}
Лимит на сессию: 3
Кулдаун: {state.hint_cooldown} сек
Последняя подсказка: {time.strftime("%H:%M:%S", time.localtime(state.last_hint_time)) if state.last_hint_time > 0 else "ещё не было"}
""",
                title="Hints",
                border_style="cyan",
            )
        )
        return True, None, None, True

    elif subcmd in ("get", "взять"):
        # Manual hint request
        if state.hint_credits <= 0:
            console.print("[red]❌ Нет доступных кредитов[/red]")
            return True, None, None, True

        if time.time() - state.last_hint_time < state.hint_cooldown:
            remaining = state.hint_cooldown - (time.time() - state.last_hint_time)
            console.print(
                f"[yellow]⏳ Подождите {remaining:.0f} сек перед следующей подсказкой[/yellow]"
            )
            return True, None, None, True

        # Generate hint based on context (no specific input, so use generic)
        # For manual hint, we can try to infer from active mission/lab
        context = state.get_learning_context()
        hint = None

        # If there's an active mission, maybe provide a general hint for current step
        if state.active_mission:
            from handlers.missions import _load_mission

            mission = _load_mission(state.active_mission)
            if mission:
                # Find current step (could store current_step in state, but for simplicity, first uncompleted)
                pass  # TODO: improve

        if not hint:
            hint = "💡 Попробуй систематически: разведка (nmap, gobuster) → поиск уязвимостей → эксплуатация"

        # Deduct credit
        state.hint_credits -= 1
        state.hints_used += 1
        state.last_hint_time = time.time()
        state.points = max(0, state.points * 0.95)  # 5% penalty for manual hint

        console.print(Panel(hint, title="Ручная подсказка", border_style="yellow"))
        console.print(f"[dim]Осталось кредитов: {state.hint_credits}[/dim]")
        return True, None, None, True

    elif subcmd in ("clear", "сброс"):
        state.hints_used = 0
        console.print("[green]✅ Счётчики подсказок сброшены[/green]")
        return True, None, None, True

    else:
        console.print("[cyan]Использование:[/cyan]")
        console.print("  /hint on/off — включить/выключить авто-подсказки")
        console.print("  /hints — статистика")
        console.print("  /hint get — получить ручную подсказка")
        console.print("  /hint clear — сбросить счётчики")
        return True, None, None, True
