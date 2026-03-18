# handlers/flags.py
import json
import os
import re
from typing import Any, Dict, Optional, Tuple

from rich.console import Console

from state import get_state

console = Console()


def handle_flag_check(
    flag: str | None = None,
) -> tuple[bool, Any | None, Any | None, bool]:
    """Проверка флага"""
    if not flag:
        console.print("[cyan]Использование: /flag <FLAG{...}>[/cyan]")
        return True, None, None, True
    pattern = r"FLAG\{[^}]+\}"
    if not re.fullmatch(pattern, flag.strip()):
        console.print(f"[bold red]❌ Флаг '{flag}' неверного формата.[/bold red]")
        return True, None, None, True
    try:
        # Проверка в активном задании
        state = get_state()
        if state.active_assignment:
            success, points = state.collect_flag(flag)
            if success:
                console.print(
                    f"[bold green]✅ Флаг найден в активном задании! +{points} очков[/bold green]"
                )
                from memory import init_db, update_stats

                conn2 = init_db()
                update_stats(conn2, points)
                state.increment_flag()
                newly_earned = state.check_achievements()
                if newly_earned:
                    for ach in newly_earned:
                        console.print(
                            f"[bold magenta]🏆 Достижение: {ach['name']} ({ach['icon']}) +{ach.get('points', 0)} XP[/bold magenta]"
                        )
                if state.is_assignment_complete():
                    console.print(
                        "[bold cyan]🎉 Задание завершено! Все флаги собраны.[/bold cyan]"
                    )
                    state.complete_assignment()
                    newly_earned = state.check_achievements()
                    if newly_earned:
                        for ach in newly_earned:
                            console.print(
                                f"[bold magenta]🏆 Достижение: {ach['name']} ({ach['icon']}) +{ach.get('points', 0)} XP[/bold magenta]"
                            )
                return True, None, None, True
        # Проверка в глобальной базе флагов
        flags_file = "data/flags.json"
        if not os.path.exists(flags_file):
            console.print(
                "[yellow]База флагов не найдена. Создайте data/flags.json[/yellow]"
            )
            return True, None, None, True
        with open(flags_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        for fdata in data.get("flags", []):
            if fdata["flag"] == flag:
                pts = fdata.get("points", 10)
                console.print(f"[bold green]✅ Флаг верный! +{pts} очков[/bold green]")
                from memory import init_db, update_stats

                conn2 = init_db()
                update_stats(conn2, pts)
                state = get_state()
                state.increment_flag()
                newly_earned = state.check_achievements()
                if newly_earned:
                    for ach in newly_earned:
                        console.print(
                            f"[bold magenta]🏆 Достижение: {ach['name']} ({ach['icon']}) +{ach.get('points', 0)} XP[/bold magenta]"
                        )
                # Remove flag after use to prevent reuse
                data["flags"] = [f for f in data["flags"] if f["flag"] != flag]
                with open(flags_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                return True, None, None, True
        console.print(f"[bold red]❌ Флаг '{flag}' неверный.[/bold red]")
    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
    return True, None, None, True
