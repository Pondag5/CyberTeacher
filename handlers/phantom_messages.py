"""
Phantom Messages (MF-02) — Background lab scanner that sends ghost messages.
Scans labs every 2 hours of real time, sends chat message + CP++, glitch after 3x.
"""

import time
import random
from typing import Any, List, Dict, Optional
from datetime import datetime

from state import get_state
from cyberpsychosis import get_cyberpsychosis
from handlers.types import HandlerResult


# Phantom message templates
PHANTOM_MESSAGES = [
    {
        "id": "phantom_01",
        "trigger": "uncompleted_lab",
        "text": "Ты начал {lab}, но не закончил. Код ждёт. Он не простит.",
        "cp_delta": 5,
    },
    {
        "id": "phantom_02",
        "trigger": "uncompleted_lab",
        "text": "В {lab} остался открытый сеанс. Кто-то... или что-то использует его.",
        "cp_delta": 5,
    },
    {
        "id": "phantom_03",
        "trigger": "uncompleted_lab",
        "text": "Логи {lab} показывают активность в 03:14. Ты там не был.",
        "cp_delta": 7,
    },
    {
        "id": "phantom_04",
        "trigger": "night_session",
        "text": "3 часа ночи. Идеальное время для {lab}. Никто не увидит.",
        "cp_delta": 3,
    },
    {
        "id": "phantom_05",
        "trigger": "night_session",
        "text": "Ты пробудился, а терминал всё ещё горит. {lab} не завершён.",
        "cp_delta": 5,
    },
    {
        "id": "phantom_06",
        "trigger": "high_noise",
        "text": "Шум в {lab} превысил порог. Они слышат. Очисти следы.",
        "cp_delta": 8,
    },
    {
        "id": "phantom_07",
        "trigger": "trace_active",
        "text": "Трассировка в {lab} активна. Время уходит. Твой выбор?",
        "cp_delta": 10,
    },
    {
        "id": "phantom_08",
        "trigger": "debt_warning",
        "text": "Долги накапливаются. {lab} — старый друг. Он ждёт платежа.",
        "cp_delta": 5,
    },
    {
        "id": "phantom_09",
        "trigger": "random",
        "text": "В памяти системы найден фрагмент: {lab}. Код: 0xDEADBEEF.",
        "cp_delta": 3,
    },
    {
        "id": "phantom_10",
        "trigger": "random",
        "text": "Кто-то оставил записку в {lab}: 'Не доверяй учителю. Он знает слишком много.'",
        "cp_delta": 7,
    },
]


def _get_uncompleted_labs(state) -> List[str]:
    """Get list of labs that were started but not completed."""
    labs = []
    for lab in getattr(state, "running_labs", []):
        if lab not in getattr(state, "phantom_labs_completed", []):
            labs.append(lab)
    if getattr(state, "active_mission", None):
        labs.append(state.active_mission)
    if getattr(state, "current_challenge", None):
        labs.append(state.current_challenge)
    return labs


def _get_eligible_messages(state) -> List[Dict]:
    """Get all phantom messages eligible for current state."""
    hour = datetime.now().hour
    noise = getattr(state, "noise_level", 0)
    trace_active = getattr(state, "trace_active", False)
    debts = getattr(state, "digital_debts", 0)
    uncompleted = _get_uncompleted_labs(state)

    eligible = []

    for msg in PHANTOM_MESSAGES:
        trigger = msg["trigger"]
        if trigger == "uncompleted_lab" and uncompleted:
            for lab in uncompleted:
                eligible.append({
                    "id": msg["id"],
                    "text": msg["text"].format(lab=lab),
                    "trigger": trigger,
                    "cp_delta": msg["cp_delta"],
                })
        elif trigger == "night_session" and (hour >= 23 or hour <= 5):
            eligible.append({
                "id": msg["id"],
                "text": msg["text"].format(lab="ночная сессия"),
                "trigger": trigger,
                "cp_delta": msg["cp_delta"],
            })
        elif trigger == "high_noise" and noise >= 50:
            eligible.append({
                "id": msg["id"],
                "text": msg["text"].format(lab=f"shum={noise}"),
                "trigger": trigger,
                "cp_delta": msg["cp_delta"],
            })
        elif trigger == "trace_active" and trace_active:
            target = getattr(state, "trace_target", "цель")
            eligible.append({
                "id": msg["id"],
                "text": msg["text"].format(lab=target),
                "trigger": trigger,
                "cp_delta": msg["cp_delta"],
            })
        elif trigger == "debt_warning" and debts > 3:
            eligible.append({
                "id": msg["id"],
                "text": msg["text"].format(lab="долги"),
                "trigger": trigger,
                "cp_delta": msg["cp_delta"],
            })
        elif trigger == "random":
            eligible.append({
                "id": msg["id"],
                "text": msg["text"].format(lab="система"),
                "trigger": trigger,
                "cp_delta": msg["cp_delta"],
            })

    return eligible


def scan_phantom_labs() -> Optional[Dict]:
    """Background scanner — call from main loop every 2 hours real time.
    
    Returns a phantom message dict if one should fire, else None.
    """
    from di import get_context
    try:
        state = get_context().state
    except RuntimeError:
        from state import get_state
        state = get_state()
    now = time.time()

    # Check 2-hour cooldown
    if now - getattr(state, "last_phantom_check", 0) < 7200:
        return None

    state.last_phantom_check = now

    # Initialize if first run
    if not hasattr(state, "phantom_message_count"):
        state.phantom_message_count = 0
        state.phantom_messages = []
        return None

    # Check if conditions exist
    uncompleted = _get_uncompleted_labs(state)
    hour = datetime.now().hour
    noise = getattr(state, "noise_level", 0)
    trace_active = getattr(state, "trace_active", False)
    debts = getattr(state, "digital_debts", 0)

    if not uncompleted and not (hour >= 23 or hour <= 5) and noise < 50 and not trace_active and debts <= 3:
        return None  # No reason to send

    # 30% chance to send even if conditions met
    if random.random() > 0.3:
        return None

    eligible = _get_eligible_messages(state)

    # Don't repeat same message
    sent_ids = {m.get("id") for m in state.phantom_messages}
    eligible = [m for m in eligible if m["id"] not in sent_ids]

    if not eligible:
        return None

    # Pick random
    msg = random.choice(eligible)
    cp_delta = msg["cp_delta"]

    # Apply CP increase
    cp = get_cyberpsychosis()
    cp.on_risky_action(cp_delta * 5)

    # Record in state
    state.phantom_message_count += 1
    state.phantom_messages.append({
        "id": msg["id"],
        "text": msg["text"],
        "trigger": msg["trigger"],
        "cp_delta": cp_delta,
        "timestamp": now,
    })

    # Force state save
    state.save_to_file(force=True)

    return {
        "id": msg["id"],
        "text": msg["text"],
        "trigger": msg["trigger"],
        "cp_delta": cp_delta,
        "total_count": state.phantom_message_count,
    }


def get_phantom_status() -> Dict[str, Any]:
    """Get phantom messages status for API/UI."""
    from di import get_context
    try:
        state = get_context().state
    except RuntimeError:
        from state import get_state
        state = get_state()
    return {
        "total_count": getattr(state, "phantom_message_count", 0),
        "messages": getattr(state, "phantom_messages", []),
        "last_check": getattr(state, "last_phantom_check", 0),
    }


def handle_phantom_message(action: str) -> HandlerResult:
    """Handle /phantom [list|status|reset|force] command."""
    from di import get_context
    from ui import console
    from rich.panel import Panel
    from handlers.types import HandlerResult

    state = get_context().state
    parts = action.split()
    sub = parts[1] if len(parts) > 1 else "status"

    if sub == "list":
        msgs = getattr(state, "phantom_messages", [])
        if not msgs:
            console.print("[yellow]Phantom messages пуст[/yellow]")
        else:
            for m in msgs:
                console.print(
                    Panel(
                        f"[magenta]{m['text']}[/magenta]\n\n"
                        f"[dim]Trigger: {m['trigger']} | CP +{m['cp_delta']}[/dim]",
                        title=f"Phantom {m['id']}",
                        border_style="magenta",
                    )
                )
        return True, None, None, True

    elif sub == "reset":
        state.phantom_message_count = 0
        state.phantom_messages = []
        state.last_phantom_check = 0
        console.print("[green]Phantom messages сброшен[/green]")
        return True, None, None, True

    elif sub == "force":
        # Force scan regardless of cooldown
        state.last_phantom_check = 0
        from handlers.phantom_messages import scan_phantom_labs
        result = scan_phantom_labs()
        if result:
            console.print(
                Panel(
                    f"[bold]{result['text']}[/bold]\n\n"
                    f"[red]CP +{result['cp_delta']}[/red] | [dim]Trigger: {result['trigger']}[/dim]",
                    title="Phantom Message",
                    border_style="magenta",
                )
            )
        else:
            console.print("[green]Фантомов не обнаружено[/green]")
        return True, None, None, True

    else:  # status
        status = get_phantom_status()
        console.print(
            Panel(
                f"Всего получено: [bold]{status['total_count']}[/bold]\n"
                f"Последняя проверка: {time.ctime(status['last_check']) if status['last_check'] else 'никогда'}",
                title="Phantom Messages",
                border_style="magenta",
            )
        )
        return True, None, None, True