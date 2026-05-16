"""Обработчик команды /daily — ежедневные челленджи."""

from typing import Any

from daily_challenge import generate_daily_challenge, get_daily_status, get_hint, submit_daily_answer
from state import get_state
from ui import console


def handle_daily(action: str) -> tuple[bool, Any | None, Any | None, bool]:
    """Обработать команду /daily и её подкоманды."""
    state = get_state()
    parts = action.split(maxsplit=1)
    subcmd = parts[0].lower() if len(parts) > 0 else ""
    arg = parts[1].strip() if len(parts) > 1 else ""

    if subcmd in ("", "daily", "challenge"):
        # Показать текущий челлендж
        challenge = generate_daily_challenge()
        console.print(get_daily_status())
        console.print(f"\n[bold]Задание:[/bold] {challenge['desc']}")
        console.print(f"[dim]Сложность: {challenge['difficulty']}[/dim]")
        console.print("[dim]Ответь текстом или используй /daily hint[/dim]")
        return True, None, None, True

    if subcmd == "hint":
        console.print(f"[yellow]💡 Подсказка:[/yellow] {get_hint()}")
        return True, None, None, True

    if subcmd == "status":
        console.print(get_daily_status())
        return True, None, None, True

    if subcmd == "force":
        # Для тестирования — перегенерировать челлендж
        import os
        from daily_challenge import CHALLENGE_FILE, _get_today_str
        if os.path.exists(CHALLENGE_FILE):
            import json
            with open(CHALLENGE_FILE, "r") as f:
                data = json.load(f)
            today = _get_today_str()
            data.get("history", {}).pop(today, None)
            with open(CHALLENGE_FILE, "w") as f:
                json.dump(data, f)
        challenge = generate_daily_challenge(difficulty=arg if arg else None)
        console.print(get_daily_status())
        console.print(f"\n[bold]Задание:[/bold] {challenge['desc']}")
        return True, None, None, True

    # Всё остальное считаем ответом на челлендж
    result = submit_daily_answer(action)
    if result["correct"]:
        console.print(f"[green]✅ {result['feedback']}[/green]")
        console.print(f"[bold]+{result['xp_reward']} XP[/bold]")
        state.points += result["xp_reward"]
        if result.get("streak_bonus", 0) > 0:
            console.print(f"[yellow]🔥 Бонус за стрик: +{result['streak_bonus']} XP[/yellow]")
    else:
        console.print(f"[yellow]❌ {result['feedback']}[/yellow]")

    return True, None, None, True
