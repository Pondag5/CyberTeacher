"""
Phantom Labs — временные призрачные лабы.
Появляются при высоком киберпсихозе, живут 6 часов, исчезают навсегда.
"""

import random
import time
from typing import Any, Dict, List, Optional

from state import get_state

PHANTOM_LIFETIME = 21600  # 6 hours in seconds
SPAWN_INTERVAL = 3600  # check spawn once per hour
MAX_PHANTOMS = 3
CP_SPAWN_THRESHOLD = 30  # cyberpsychosis level needed for spawns

PHANTOM_LABS_POOL = [
    {
        "id": "phantom_null",
        "name": "Null Pointer Lab",
        "desc": "Лаборатория исчезнувших указателей. Говорят, её нет.",
        "difficulty": "ghost",
    },
    {
        "id": "phantom_buffer",
        "name": "Buffer Overflow Ghost",
        "desc": "Стек переполнен. Призраки прошлых сессий бродят по памяти.",
        "difficulty": "haunted",
    },
    {
        "id": "phantom_reverse",
        "name": "Reverse Nightmare",
        "desc": "Бинарный код пульсирует. Кажется, он жив.",
        "difficulty": "cursed",
    },
    {
        "id": "phantom_watcher",
        "name": "Watcher Echo",
        "desc": "Чей-то лог. Watchers были здесь. Может, они всё ещё здесь.",
        "difficulty": "dangerous",
    },
    {
        "id": "phantom_teacher",
        "name": "Teacher's Shadow",
        "desc": "Тень учителя мерцает в терминале. Она не должна существовать.",
        "difficulty": "glitch",
    },
]

GLITCH_NAMES = [
    "Segfault Sector",
    "Dead Register",
    "Phantom Thread",
    "Stack Smash Echo",
    "Null Island",
    "Undefined Behavior Zone",
]


def _get_cyberpsychosis_level() -> float:
    try:
        from cyberpsychosis import CyberpsychosisState

        st = CyberpsychosisState()
        return (st.stress + st.obsession + st.recklessness) / 3
    except (ImportError, RuntimeError):
        return 0.0


def _spawn_chance(cp_level: float) -> float:
    if cp_level < CP_SPAWN_THRESHOLD:
        return 0.0
    return min(0.8, (cp_level - CP_SPAWN_THRESHOLD) / 100)


def _pick_phantom() -> Dict[str, Any]:
    base = random.choice(PHANTOM_LABS_POOL)
    now = time.time()
    name = random.choice(GLITCH_NAMES)
    return {
        "lab_id": base["id"],
        "name": f"👻 {name}",
        "description": base["desc"],
        "difficulty": base["difficulty"],
        "spawned_at": now,
        "expires_at": now + PHANTOM_LIFETIME,
        "completed": False,
    }


def _cleanup_expired(state) -> None:
    now = time.time()
    alive = []
    for lab in state.phantom_labs:
        if lab.get("expires_at", 0) > now:
            alive.append(lab)
        else:
            lid = lab.get("lab_id", "?")
            if lid not in state.phantom_labs_completed:
                pass
    state.phantom_labs = alive


def _maybe_spawn(state) -> None:
    _cleanup_expired(state)
    cp_level = _get_cyberpsychosis_level()
    chance = _spawn_chance(cp_level)
    if len(state.phantom_labs) >= MAX_PHANTOMS:
        return
    if random.random() < chance:
        state.phantom_labs.append(_pick_phantom())


def get_phantom_labs() -> List[Dict[str, Any]]:
    state = get_state()
    _cleanup_expired(state)
    _maybe_spawn(state)
    result = []
    for lab in state.phantom_labs:
        remaining = max(0, lab.get("expires_at", 0) - time.time())
        result.append(
            {
                "lab_id": lab.get("lab_id", ""),
                "name": lab.get("name", ""),
                "description": lab.get("description", ""),
                "difficulty": lab.get("difficulty", ""),
                "remaining": remaining,
                "completed": lab.get("completed", False),
            }
        )
    return result


def complete_phantom_lab(lab_id: str) -> Optional[str]:
    state = get_state()
    for lab in state.phantom_labs:
        if lab.get("lab_id") == lab_id and not lab.get("completed"):
            lab["completed"] = True
            if lab_id not in state.phantom_labs_completed:
                state.phantom_labs_completed.append(lab_id)
            return f"✅ Фантомная лаба '{lab.get('name', lab_id)}' завершена. Она больше не появится."
    return None


def force_spawn() -> Optional[str]:
    state = get_state()
    if len(state.phantom_labs) >= MAX_PHANTOMS:
        return "❌ Уже максимальное количество фантомных лаб."
    lab = _pick_phantom()
    state.phantom_labs.append(lab)
    return f"👻 Фантомная лаба '{lab['name']}' появилась. У тебя 6 часов."


def handle_phantom(action: str) -> tuple:
    from ui import console, Panel

    parts = action.strip().split()
    sub = parts[1].lower() if len(parts) > 1 else "list"
    if sub == "list":
        labs = get_phantom_labs()
        if not labs:
            console.print(
                "[dim]Фантомных лаб нет. Тишина в эфире. Слишком тихо...[/dim]"
            )
        else:
            lines = []
            for lab in labs:
                remaining = lab["remaining"]
                hours = int(remaining // 3600)
                mins = int((remaining % 3600) // 60)
                status = "✅" if lab["completed"] else "⏳"
                lines.append(
                    f"  {status} {lab['name']} [{lab['difficulty']}] — {hours}ч {mins}мин"
                )
            console.print(
                Panel("\n".join(lines), title="👻 Phantom Labs", border_style="purple")
            )
    elif sub == "force":
        msg = force_spawn()
        console.print(msg or "[yellow]Не удалось создать.[/yellow]")
    elif sub == "complete" and len(parts) > 2:
        msg = complete_phantom_lab(parts[2])
        console.print(msg or "[yellow]Лаба не найдена.[/yellow]")
    else:
        console.print(
            "[yellow]Используй: /phantom list, /phantom force, /phantom complete <id>[/yellow]"
        )
    return True, None, None, True
