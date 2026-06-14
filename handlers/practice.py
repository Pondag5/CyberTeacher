# handlers/practice.py
import os
from typing import Any, Optional

from rich.console import Console

from di import get_context
from handlers.types import HandlerResult


console = Console()


def handle_practice(action: str) -> HandlerResult:
    """Обработка команд /practice и /lab"""
    try:
        from practice import (
            get_all_running_labs,
            _list_labs,
            _start_lab,
            _stop_lab,
        )

        parts = action.split()

        if action in {"practice", "lab"}:
            # Показать список доступных лаб
            console.print(_list_labs())
            return True, None, None, True

        elif (
            parts[0] in ["lab", "practice"] and len(parts) >= 3 and parts[1] == "start"
        ):
            lab_name = parts[2]
            # Отмечаем запуск лаборатории в state (достижение)
            ctx = get_context()
            state = ctx.state
            state.start_lab()
            # Reset hint counter for new lab session
            state.hints_used = 0
            result = _start_lab(lab_name)
            console.print(result)
            # Проверяем, не заработано ли новое достижение
            newly_earned = state.check_achievements()
            if newly_earned:
                import json
                import os

                ach_file = "data/achievements.json"
                achievements_map: dict[str, Any] = {}
                if os.path.exists(ach_file):
                    with open(ach_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        achievements_map = {
                            a["id"]: a for a in data.get("achievements", [])
                        }
                for ach_id in newly_earned:
                    ach = achievements_map.get(ach_id, {})
                    name = ach.get("name", ach_id)
                    icon = ach.get("icon", "🏆")
                    points = ach.get("points", 0)
                    console.print(
                        f"[bold magenta]🏆 Достижение: {name} ({icon}) +{points} XP[/bold magenta]"
                    )
            return True, None, None, True

        elif parts[0] in ["lab", "practice"] and len(parts) >= 3 and parts[1] == "stop":
            lab_name = parts[2]
            result = _stop_lab(lab_name)
            console.print(result)
            # Сбросить таймер Trace при остановке лабы
            ctx = get_context()
            state = ctx.state
            state.trace_deadline = None
            state.trace_hint = None
            return True, None, None, True

        elif (
            parts[0] in ["lab", "practice"] and len(parts) >= 2 and parts[1] == "status"
        ):
            running = get_all_running_labs()
            if running:
                console.print("[bold cyan]🟢 Запущенные лаборатории:[/bold cyan]\n")
                for key, info in running.items():
                    console.print(f"  • {info['name']}: {info['status']}")
            else:
                console.print("[yellow]Нет запущенных лабораторий[/yellow]")
            return True, None, None, True

        elif action == "htb":
            # Рекомендации HTB машин — делегируем в htb handler
            from .htb import handle_htb

            return handle_htb(action)

        else:
            console.print("[cyan]Использование:[/cyan]")
            console.print("  /lab          - показать список всех лаб")
            console.print("  /lab start <name> - запустить лабораторию")
            console.print("  /lab stop <name>  - остановить лабораторию")
            console.print("  /lab status      - статус запущенных")
            console.print("  /htb             - рекомендации HTB машин")
            return True, None, None, True

    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
        import traceback

        traceback.print_exc()
        return True, None, None, True


def handle_container_check(
    action: str,
) -> HandlerResult:
    """Проверка статуса контейнеров"""
    try:
        from practice import get_all_running_labs

        running = get_all_running_labs()
        if running:
            console.print("[bold cyan]🐳 Статус контейнеров:[/bold cyan]\n")
            for key, info in running.items():
                console.print(f"  🟢 {info['name']}: {info['status']}")
        else:
            console.print("[yellow]Нет запущенных контейнеров[/yellow]")
        return True, None, None, True
    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
        return True, None, None, True
