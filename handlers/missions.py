"""Mission editor and runner"""

import json
import os
from typing import Any

from rich.console import Console
from rich.table import Table

from di import get_context
from handlers.types import HandlerResult


console = Console()

MISSIONS_DIR = os.path.join(os.path.dirname(__file__), "..", "missions")


def _load_mission(mission_id: str) -> Any | None:
    path = os.path.join(MISSIONS_DIR, f"{mission_id}.json")
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _list_missions_api() -> list[dict[str, Any]]:
    """Return missions as plain dicts for API consumption."""
    import glob as _glob

    ctx = get_context()
    state = ctx.state
    completed = set(
        state.missions_completed if hasattr(state, "missions_completed") else []
    )
    result = []
    for path in sorted(_glob.glob(os.path.join(MISSIONS_DIR, "*.json"))):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            mid = data.get("id", os.path.basename(path).replace(".json", ""))
            prereqs = data.get("prerequisites", [])
            locked = any(p not in completed for p in prereqs)
            result.append(
                {
                    "id": mid,
                    "name": data.get("title", ""),
                    "desc": data.get("description", ""),
                    "category": data.get("category", ""),
                    "difficulty": data.get("difficulty", "medium"),
                    "xp_reward": data.get("xp_reward", 0),
                    "completed": mid in completed,
                    "locked": locked,
                    "prerequisites": prereqs,
                }
            )
        except (OSError, IOError, json.JSONDecodeError):
            continue
    return result


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

    state = get_context().state
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
        except (OSError, IOError, json.JSONDecodeError):
            continue

    console.print(table)
    return ""


def _start_mission(mission_id: str) -> str:
    data = _load_mission(mission_id)
    if not data:
        return f"[red]Миссия '{mission_id}' не найдена[/red]"

    ctx = get_context()
    state = ctx.state
    if mission_id in (getattr(state, "missions_completed", [])):
        return f"[yellow]Миссия '{mission_id}' уже пройдена[/yellow]"

    # Check prerequisites
    prereqs = data.get("prerequisites", [])
    completed = set(getattr(state, "missions_completed", []))
    missing = [p for p in prereqs if p not in completed]
    if missing:
        names = ", ".join(missing)
        return f"[red]❌ Требуются миссии: {names}. Заверши их сначала.[/red]"

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
    # Reset hint counter for new mission
    state.hints_used = 0
    # Set trace timer if provided
    if "time_limit_minutes" in data:
        import time as _time

        state.trace_deadline = _time.time() + data["time_limit_minutes"] * 60
        state.trace_hint = "⏰ Время миссии истекло!"
    ctx.save_state()
    return ""


def _submit_mission(mission_id: str) -> str:
    data = _load_mission(mission_id)
    if not data:
        return f"[red]Миссия '{mission_id}' не найдена[/red]"

    ctx = get_context()
    state = ctx.state
    if mission_id in (getattr(state, "missions_completed", [])):
        return f"[yellow]Миссия '{mission_id}' уже завершена[/yellow]"

    # Check prerequisites
    prereqs = data.get("prerequisites", [])
    completed_set = set(getattr(state, "missions_completed", []))
    missing = [p for p in prereqs if p not in completed_set]
    if missing:
        names = ", ".join(missing)
        return f"[red]❌ Требуются миссии: {names}. Заверши их сначала.[/red]"

    # Check PoC steps if any
    steps = data.get("steps", [])
    exploit_steps = [s for s in steps if s.get("accepts_exploit", False)]
    if exploit_steps:
        # Verify all exploit steps are completed
        for step in exploit_steps:
            order = step.get("order")
            success_entry = next(
                (
                    d
                    for d in getattr(state, "exploit_success", [])
                    if d.get("mission_id") == mission_id
                    and d.get("step_order") == order
                ),
                None,
            )
            if not success_entry:
                return f"[red]❌ Шаг {order} не пройден через /exploit_submit. Используйте /exploit_submit <mission_id> {order} <script>[/red]"

    # All checks passed, complete mission
    if not hasattr(state, "missions_completed"):
        state.missions_completed = []
    if mission_id not in state.missions_completed:
        state.missions_completed.append(mission_id)
        from handlers.debt import clear_debt

        clear_debt("", count=1, prefix=f"Миссия: {mission_id}")
        try:
            from behavior_profile import record_action

            record_action(state, "mission_complete")
        except ImportError:
            pass
    xp = data.get("xp_reward", 0)
    state.points += xp
    # Auto-track skill from mission category
    try:
        from handlers.skills import guess_skill_from_topic

        topic = data.get("category", "") or data.get("title", "")
        skill = guess_skill_from_topic(topic)
        if skill:
            state.track_skill(skill, True, xp=xp)
    except ImportError:
        pass
    ctx.save_state()
    return f"[green]✅ Миссия '{mission_id}' завершена! +{xp} XP[/green]"


def handle_missions(action: str) -> HandlerResult:
    """Обработка команд миссий."""
    parts = action.split()
    if len(parts) == 1 or parts[0] != "mission":
        console.print("[cyan]Использование:[/cyan]")
        console.print("  /missions              - список миссий")
        console.print("  /mission start <id>    - начать миссию")
        console.print("  /mission submit <id>   - завершить миссию")
        return True, None, None, True

    cmd = parts[1] if len(parts) >= 2 else "list"
    if cmd in {"list", ""}:
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
