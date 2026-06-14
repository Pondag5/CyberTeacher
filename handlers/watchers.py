"""
Watchers counterattack system.

Watchers атакуют при высоком шуме + грязные логи + риск.
Эффекты: фейковые сообщения, блокировка действий, стресс.
"""

import time
from typing import Optional

from state import get_state

ATTACK_COOLDOWN = 1800  # 30 minutes between attacks
ATTACK_DURATION = 300  # 5 minutes of "blocked" effects
NOISE_THRESHOLD = 70
LOG_THRESHOLD = 3
RISK_THRESHOLD = 50

ATTACK_MESSAGES = [
    "🚨 Watchers засекли твою активность. Наслаждайся последствиями.",
    "⚠️ WATCHERS: Твой IP залогирован. Атака запущена.",
    "🔥 Watchers ответили. Ожидай помех.",
    "💀 Тебя засекли. Watchers не прощают ошибок.",
    "🕵️ Watchers: «Мы следим за тобой уже неделю.»",
]


def get_watchers_status() -> dict:
    state = get_state()
    now = time.time()
    if state.watcher_attack_active and now > state.watcher_attack_until:
        state.watcher_attack_active = False
        state.watcher_attack_until = 0.0
    cooldown_remaining = max(0, ATTACK_COOLDOWN - (now - state.last_watcher_attack))
    return {
        "attack_active": state.watcher_attack_active,
        "attack_remaining": max(0, state.watcher_attack_until - now)
        if state.watcher_attack_active
        else 0,
        "cooldown_remaining": cooldown_remaining,
        "noise_level": state.noise_level,
        "dirty_logs": len(state.dirty_logs),
        "risk_level": state.risk_level,
    }


def _can_trigger() -> bool:
    state = get_state()
    now = time.time()
    if state.watcher_attack_active:
        return False
    if now - state.last_watcher_attack < ATTACK_COOLDOWN:
        return False
    if state.noise_level < NOISE_THRESHOLD:
        return False
    if len(state.dirty_logs) < LOG_THRESHOLD:
        return False
    if state.risk_level < RISK_THRESHOLD:
        return False
    return True


def trigger_counterattack() -> Optional[str]:
    if not _can_trigger():
        return None
    state = get_state()
    now = time.time()
    state.watcher_attack_active = True
    state.watcher_attack_until = now + ATTACK_DURATION
    state.last_watcher_attack = now
    state.noise_level = min(100, state.noise_level + 20)
    state.risk_level = min(100, state.risk_level + 15)
    msg = ATTACK_MESSAGES[int(now) % len(ATTACK_MESSAGES)]
    return msg


def handle_watchers(action: str) -> tuple:
    from ui import console, Panel

    status = get_watchers_status()
    if action.strip() == "watchers":
        lines = [
            f"Атака активна: {'✅' if status['attack_active'] else '❌'}",
        ]
        if status["attack_active"]:
            lines.append(f"Осталось: {status['attack_remaining']:.0f}с")
        if status["cooldown_remaining"] > 0:
            lines.append(f"Перезарядка: {status['cooldown_remaining']:.0f}с")
        lines.append(f"Шум: {status['noise_level']}%")
        lines.append(f"Грязных логов: {status['dirty_logs']}")
        lines.append(f"Риск: {status['risk_level']}%")
        console.print(Panel("\n".join(lines), title="👁 Watchers", border_style="red"))
    return True, None, None, True
