"""
Trace Timer system.

Таймер при подключении к вражеским системам.
Если не успеть завершить лабу до дедлайна — последствия.
"""

import time
from typing import Optional

from state import get_state

TRACE_DURATION = 180  # 3 minutes default


def get_trace_status() -> dict:
    state = get_state()
    if not state.trace_active:
        return {"active": False}
    remaining = max(0, state.trace_deadline - time.time())
    return {
        "active": True,
        "target": state.trace_target,
        "remaining_seconds": int(remaining),
        "remaining_minutes": round(remaining / 60, 1),
        "expired": remaining <= 0,
    }


def start_trace(target: str, duration: int = TRACE_DURATION) -> str:
    state = get_state()
    state.trace_active = True
    state.trace_deadline = time.time() + duration
    state.trace_target = target
    return (
        f"\n🔍 ТРАССИРОВКА! {target} нас засёк! "
        f"У тебя {duration // 60}:{duration % 60:02d} мин до обнаружения."
    )


def stop_trace() -> str:
    state = get_state()
    if not state.trace_active:
        return "Нет активной трассировки."
    state.trace_active = False
    state.trace_deadline = None
    state.trace_target = ""
    return "✅ Трассировка остановлена. Следы заметены."


def check_trace_expired() -> Optional[str]:
    """Проверить, истекла ли трассировка. Вызвать при старте любой лабы."""
    state = get_state()
    if not state.trace_active:
        return None
    if time.time() >= state.trace_deadline:
        state.trace_active = False
        from handlers.noise import add_noise

        add_noise(15)
        return f"\n💀 ТРАССИРОВКА ЗАВЕРШЕНА! {state.trace_target} обнаружил вторжение. +15 Noise."
    return None
