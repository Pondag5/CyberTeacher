"""
Dirty Logs system.

Каждая активность в лабах оставляет грязные логи.
Watchers видят их. /wipe_logs — чистит.
"""

import time
from typing import List

from state import get_state


def add_log(source: str, detail: str = "") -> None:
    """Добавить запись в грязные логи."""
    state = get_state()
    logs = getattr(state, "dirty_logs", [])
    logs.append(
        {
            "source": source,
            "detail": detail,
            "time": time.time(),
        }
    )
    state.dirty_logs = logs
    if len(logs) >= 5:
        from handlers.noise import add_noise

        add_noise(3)


def check_logs() -> dict:
    """Вернуть список грязных логов."""
    state = get_state()
    logs = getattr(state, "dirty_logs", [])
    return {
        "count": len(logs),
        "logs": [
            {
                "source": log["source"],
                "detail": log["detail"],
                "time_ago": _time_ago(log["time"]),
            }
            for log in logs[-10:]
        ],
    }


def wipe_logs() -> str:
    """Очистить все грязные логи."""
    state = get_state()
    count = len(getattr(state, "dirty_logs", []))
    if count == 0:
        return "Логи чисты. Нечего заметать."
    state.dirty_logs = []
    # Снижает шум при очистке
    from handlers.noise import add_noise

    state.noise_level = max(0, state.noise_level - 10)
    try:
        from behavior_profile import record_action

        record_action(state, "wipe_logs")
    except ImportError:
        pass
    return f"✅ Логи очищены! Удалено {count} записей. Noise -10."


def _time_ago(t: float) -> str:
    secs = int(time.time() - t)
    if secs < 60:
        return f"{secs}с назад"
    mins = secs // 60
    if mins < 60:
        return f"{mins}мин назад"
    hours = mins // 60
    return f"{hours}ч {mins % 60}мин назад"
