# handlers/achievements.py
import json
import os
from typing import Any, Dict, List, Optional, Tuple

from rich.console import Console

from state import get_state

console = Console()


def handle_achievements(
    *args, **kwargs
) -> tuple[bool, Any | None, Any | None, bool]:
    """Управление достижениями: list, earn <id> (test mode), help"""
    try:
        action = args[0] if args else "achievements"
        parts = action.split() if isinstance(action, str) else ["achievements"]
        subcmd = parts[1] if len(parts) > 1 else "list"

        achievements_file = "data/achievements.json"
        if not os.path.exists(achievements_file):
            console.print("[yellow]Файл достижений не найден[/yellow]")
            return True, None, None, True

        with open(achievements_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        achievements = {ach["id"]: ach for ach in data.get("achievements", [])}

        # Получить текущие достижения из state
        state = get_state()
        earned_ids = state.earned_achievements

        # Подкоманда: earn <id> - получить достижение (тестовый режим)
        if subcmd == "earn":
            if len(parts) < 3:
                console.print("[cyan]Использование: /achievements earn <id>[/cyan]")
                console.print("Пример: /achievements earn first_blood")
                return True, None, None, True

            ach_id = parts[2]
            if ach_id not in achievements:
                console.print(f"[yellow]Достижение '{ach_id}' не найдено[/yellow]")
                console.print(
                    "[cyan]Доступные ID: "
                    + ", ".join(sorted(achievements.keys()))
                    + "[/cyan]"
                )
                return True, None, None, True

            ach = achievements[ach_id]
            # Проверяем, не получено ли уже
            if ach_id in earned_ids:
                console.print(f"[yellow]Достижение уже получено[/yellow]")
                return True, None, None, True

            # Добавляем
            state.earned_achievements.append(ach_id)
            xp = ach.get("points", 0)
            if xp > 0:
                state.points += xp
            console.print(f"[bold green]✅ Достижение получено![/bold green]")
            console.print(f"{ach.get('icon', '🏆')} **{ach.get('name')}** (+{xp} XP)")
            console.print(f"[dim]{ach.get('description', '')}[/dim]")
            return True, None, None, True

        # Подкоманда: help
        elif subcmd == "help":
            console.print("[bold cyan]🏆 Достижения — помощь[/bold cyan]\n")
            console.print("Команды:")
            console.print("  /achievements - показать список всех достижений")
            console.print(
                "  /achievements earn <id> - получить достижение (тестовый режим)"
            )
            console.print("  /achievements help - эта справка")
            return True, None, None, True

        # По умолчанию: list
        console.print("[bold cyan]🏆 Все достижения[/bold cyan]\n")
        for ach_id, ach in achievements.items():
            name = ach.get("name", "Без названия")
            description = ach.get("description", "")
            icon = ach.get("icon", "🏆")
            xp = ach.get("xp", 0)
            status = "(✅)" if ach_id in earned_ids else "(⬜)"

            console.print(f"{status} {icon} **{name}** (+{xp} XP)")
            if description:
                console.print(f"   {description}")
            console.print(f"   [dim]ID: {ach_id}[/dim]\n")

    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
        import traceback

        traceback.print_exc()
    return True, None, None, True
