"""
Digital Debt system.

Незакрытые лабы, эпизоды, миссии = долги.
>5 → учитель начинает болеть (меньше подсказок).
Списываются при завершении контента.
"""

from typing import List

from state import get_state
from story_mode import CHAPTERS, STORY_EPISODES

DEBT_WARNING = 3
DEBT_CRITICAL = 5
DEBT_HINTS_BLOCKED = 5  # подсказки отключаются при >= этом числа


def get_debts() -> dict:
    state = get_state()
    _recalc_debts(state)
    return {
        "total": state.digital_debts,
        "details": state.debt_details[-10:],
        "status": _get_debt_status(state.digital_debts),
    }


def _get_debt_status(count: int) -> str:
    if count == 0:
        return "clean"
    if count <= DEBT_WARNING:
        return "light"
    if count <= DEBT_CRITICAL:
        return "warning"
    return "critical"


def _recalc_debts(state) -> None:
    """Пересчитать долги на основе незавершённого контента."""
    debts = 0
    details: List[str] = []

    # Uncompleted chapters (only count chapters BEFORE current one — user already moved past)
    ch_completed = getattr(state, "chapter_completed", [])
    story_done = set(getattr(state, "story_completed", []))
    current_ch = getattr(state, "current_chapter", 1)
    for ch in CHAPTERS:
        if ch["id"] not in ch_completed and ch["id"] < current_ch:
            missing_eps = [e for e in ch["episode_ids"] if e not in story_done]
            if missing_eps:
                debts += len(missing_eps)
                details.append(
                    f"Глава {ch['id']}: не пройдено эпизодов: {len(missing_eps)}"
                )

    # Uncompleted missions
    missions_done = getattr(state, "missions_completed", [])
    active = getattr(state, "active_mission", None)
    if active and active not in missions_done:
        debts += 1
        details.append(f"Активная миссия: {active}")

    # Running labs
    running = getattr(state, "running_labs", [])
    if running:
        debts += len(running)
        details.append(f"Запущенные лабы: {len(running)}")

    state.digital_debts = debts
    state.debt_details = details


def add_debt(reason: str, count: int = 1) -> str:
    state = get_state()
    state.digital_debts += count
    details = getattr(state, "debt_details", [])
    details.append(reason)
    state.debt_details = details
    if state.digital_debts >= DEBT_HINTS_BLOCKED:
        return f"\n🚨 ДОЛГОВ: {state.digital_debts}. Подсказки отключены до погашения."
    if state.digital_debts >= DEBT_WARNING:
        return f"\n⚠️ Долгов: {state.digital_debts}. Учитель начинает нервничать."
    return ""


def clear_debt(reason: str, count: int = 1, prefix: str = "") -> str:
    """Списать долги (вызывается при завершении эпизода/миссии).

    Args:
        reason: описание долга
        count: сколько долгов списать
        prefix: префикс для поиска в details (если точное совпадение не подходит)
    """
    state = get_state()
    details = getattr(state, "debt_details", [])
    state.digital_debts = max(0, state.digital_debts - count)
    # Remove matching entries
    remaining = []
    removed = 0
    for d in details:
        if removed < count and (d == reason or (prefix and d.startswith(prefix))):
            removed += 1
        else:
            remaining.append(d)
    state.debt_details = remaining
    return ""
