# handlers/practice.py
import os
from typing import Any, Dict, Optional, Tuple

from rich.console import Console

from state import get_state

console = Console()


def handle_practice(action: str) -> tuple[bool, Any | None, Any | None, bool]:
    """Обработка команд /practice и /lab"""
    try:
        from practice import (
            HTB_MACHINES,
            get_all_running_labs,
            get_htb_recommendation,
            list_labs,
            start_lab,
            stop_lab,
        )

        parts = action.split()

        if action == "practice" or action == "lab":
            # Показать список доступных лаб
            console.print(list_labs())
            return True, None, None, True

        elif (
            parts[0] in ["lab", "practice"] and len(parts) >= 3 and parts[1] == "start"
        ):
            lab_name = parts[2]
            # Отмечаем запуск лаборатории в state (достижение)
            get_state().start_lab()
            result = start_lab(lab_name)
            console.print(result)
            # Проверяем, не заработано ли новое достижение
            newly_earned = get_state().check_achievements()
            if newly_earned:
                for ach in newly_earned:
                    console.print(
                        f"[bold magenta]🏆 Достижение: {ach['name']} ({ach['icon']}) +{ach.get('points', 0)} XP[/bold magenta]"
                    )
            return True, None, None, True

        elif parts[0] in ["lab", "practice"] and len(parts) >= 3 and parts[1] == "stop":
            lab_name = parts[2]
            result = stop_lab(lab_name)
            console.print(result)
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
            # Рекомендации HTB машин
            console.print(get_htb_recommendation())
            return True, None, None, True

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
) -> tuple[bool, Any | None, Any | None, bool]:
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
