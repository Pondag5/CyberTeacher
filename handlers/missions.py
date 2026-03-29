"""Mission editor and runner"""

import json
import os
from typing import Any

from rich.console import Console
from rich.table import Table

from state import get_state

console = Console()

MISSIONS_DIR = os.path.join(os.path.dirname(__file__), "..", "missions")


def _load_mission(mission_id: str) -> dict[str, Any] | None:
    path = os.path.join(MISSIONS_DIR, f"{mission_id}.json")
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _list_missions() -> str:
    files = [f for f in os.listdir(MISSIONS_DIR) if f.endswith(".json")]
    if not files:
        return "[yellow]Нет доступных миссий[/yellow]"

    table = Table(title="Доступные миссии")
    table.add_column("ID", style="cyan")
    table.add_column("Название", style="magenta")
    table.add_column("Категория", style="green")
    table.add_column("Сложность", justify="center")
    table.add_column("XP", justify="right")
    table.add_column("Лаб", style="yellow")

    state = get_state()
    completed = set(
        state.missions_completed if hasattr(state, "missions_completed") else []
    )

    for fname in sorted(files):
        try:
            with open(os.path.join(MISSIONS_DIR, fname), "r", encoding="utf-8") as f:
                data = json.load(f)
            mid = data.get("id", fname.replace(".json", ""))
            title = data.get("title", "—")
            cat = data.get("category", "?")
            diff = "★" * data.get("difficulty", 1)
            xp = str(data.get("xp_reward", 0))
            labs = ", ".join(data.get("labs", []))
            status = "[green]✅[/green]" if mid in completed else "[dim]⬜[/dim]"
            table.add_row(f"{status} {mid}", title, cat, diff, xp, labs)
        except Exception:
            continue

    console.print(table)
    return ""


def _start_mission(mission_id: str) -> str:
    data = _load_mission(mission_id)
    if not data:
        return f"[red]Миссия '{mission_id}' не найдена[/red]"

    state = get_state()
    # Check if already completed
    if mission_id in (getattr(state, "missions_completed", [])):
        return f"[yellow]Миссия '{mission_id}' уже пройдена[/yellow]"

    # Display mission info
    out = [
        f"╔══════════════════════════════════════╗",
        f"║ МИССИЯ: {data['title']}",
        f"╚══════════════════════════════════════╝",
        f"\n📖 {data['description']}",
        f"\n🎯 ЦЕЛИ:",
    ]
    for step in data.get("steps", []):
        out.append(f"  {step['order']}. {step['objective']}")
        out.append(f"     💡 Подсказка: {step.get('hint', '—')}")
        out.append(f"     🏴 Флаг: {step.get('flag', '—')}")
        if step.get("lab"):
            out.append(f"     🎮 Лаборатория: /lab start {step['lab']}")
        out.append("")

    out.append(f"⚡ XP награда: {data.get('xp_reward', 0)}")
    out.append("Используйте /mission submit <id> для завершения.")
    console.print("\n".join(out))

    # Set active mission in state
    state.active_mission = mission_id
    # Set trace timer if provided
    if "time_limit_minutes" in data:
        import time as _time

        state.trace_deadline = _time.time() + data["time_limit_minutes"] * 60
        state.trace_hint = "⏰ Время миссии истекло!"
    return ""


def _submit_mission(mission_id: str) -> str:
    data = _load_mission(mission_id)
    if not data:
        return f"[red]Миссия '{mission_id}' не найдена[/red]"

    state = get_state()
    if mission_id in (getattr(state, "missions_completed", [])):
        return f"[yellow]Миссия '{mission_id}' уже завершена[/yellow]"

    # Check flags (here we just simulate by asking console? In real, flags would be submitted via /flag. For simplicity, we mark complete immediately.)
    # For now, auto-complete (or later we can verify flags were collected via state.collected_flags)
    # Assume success
    if not hasattr(state, "missions_completed"):
        state.missions_completed = []
    state.missions_completed.append(mission_id)
    xp = data.get("xp_reward", 0)
    state.points += xp
    state.save_to_file()
    return f"[green]✅ Миссия '{mission_id}' завершена! +{xp} XP[/green]"


def handle_missions(action: str) -> tuple[bool, Any | None, Any | None, bool]:
    """Обработка команд миссий."""
    parts = action.split()
    if len(parts) == 1 or parts[0] != "mission":
        console.print("[cyan]Использование:[/cyan]")
        console.print("  /missions              - список миссий")
        console.print("  /mission start <id>    - начать миссию")
        console.print("  /mission submit <id>   - завершить миссию")
        return True, None, None, True

    cmd = parts[1] if len(parts) >= 2 else "list"
    if cmd == "list" or cmd == "":
        _list_missions()
        return True, None, None, True
    elif cmd == "start" and len(parts) >= 3:
        mid = parts[2]
        console.print(_start_mission(mid))
        return True, None, None, True
    elif cmd == "submit" and len(parts) >= 3:
        mid = parts[2]
        console.print(_submit_mission(mid))
        return True, None, None, True
    else:
        console.print(
            "[red]Неверная команда. Используйте: /mission start|submit <id>[/red]"
        )
        return True, None, None, True
