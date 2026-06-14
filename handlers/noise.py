"""
Noise Level system.

Шкала шумности 0–100. Растёт от агрессивных действий (брутфорс, сканы).
Влияет на Watchers — при высоком шуме выше шанс контратаки.
Шум снижается на 1 ед. каждые 10 минут в stealth_mode, иначе каждые 30 минут.
"""

import time
from typing import Tuple

from state import get_state

THRESHOLD_WARNING = 40
THRESHOLD_CRITICAL = 70
THRESHOLD_ATTACK = 85


def get_noise_level() -> dict:
    state = get_state()
    _decay_noise(state)
    return {
        "level": state.noise_level,
        "status": _get_noise_status(state.noise_level),
        "stealth": state.stealth_mode,
    }


def _get_noise_status(level: int) -> str:
    if level <= 10:
        return "silent"
    if level <= THRESHOLD_WARNING:
        return "quiet"
    if level <= THRESHOLD_CRITICAL:
        return "noisy"
    if level <= THRESHOLD_ATTACK:
        return "loud"
    return "critical"


def add_noise(amount: int = 5) -> str:
    state = get_state()
    if state.stealth_mode:
        amount = max(1, amount // 2)
    state.noise_level = min(100, state.noise_level + amount)
    level = state.noise_level
    msg = ""
    if level >= THRESHOLD_ATTACK:
        msg = f"\n⚠️ ШУМ КРИТИЧЕСКИЙ ({level}%). Watchers могут атаковать!"
    elif level >= THRESHOLD_CRITICAL:
        msg = f"\n⚠️ Шум высокий ({level}%). Watchers засекли активность."
    elif level >= THRESHOLD_WARNING:
        msg = f"\n⚠️ Шум повышен ({level}%). Будь осторожнее."
    # Auto-trigger counterattack if conditions met
    try:
        from handlers.watchers import trigger_counterattack

        attack_msg = trigger_counterattack()
        if attack_msg:
            msg = msg + "\n" + attack_msg if msg else attack_msg
    except ImportError:
        pass
    return msg


def _decay_noise(state) -> None:
    """Снижать шум со временем."""
    if state.noise_level <= 0:
        return
    if state.stealth_mode and state.stealth_mode_until > time.time():
        decay_rate = 1  # 1 ед. за вызов
    else:
        decay_rate = 0  # пока не implemented — тикает при каждом запросе
    # Simplified: decay 1 every noise check if below 20
    if state.noise_level > 0 and state.noise_level < 20:
        state.noise_level = max(0, state.noise_level - 1)


def toggle_stealth() -> dict:
    state = get_state()
    if state.stealth_mode:
        state.stealth_mode = False
        state.stealth_mode_until = 0.0
        return {"active": False, "message": "Stealth mode отключён."}
    else:
        state.stealth_mode = True
        state.stealth_mode_until = time.time() + 600  # 10 minutes
        try:
            from behavior_profile import record_action

            record_action(state, "stealth_toggle_on")
        except ImportError:
            pass
        return {
            "active": True,
            "message": "Stealth mode включён на 10 мин. Шум снижен вдвое.",
        }
