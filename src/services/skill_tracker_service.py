"""
Skill tracking service.
"""

import time
from typing import Any


def track_skill(
    skill_tracker: dict[str, Any],
    skill: str,
    success: bool,
    xp: int = 10,
) -> None:
    """Отследить использование навыка."""
    if skill not in skill_tracker:
        skill_tracker[skill] = {
            "level": 0,
            "xp": 0,
            "last_practice": time.time(),
            "attempts": 0,
            "successes": 0,
        }
    s = skill_tracker[skill]
    s["xp"] += xp
    s["attempts"] += 1
    s["last_practice"] = time.time()
    if success:
        s["successes"] += 1
    new_level = min(5, s["xp"] // 50)
    s["level"] = max(s["level"], new_level)


def get_skill_level(skill_tracker: dict[str, Any], skill: str) -> int:
    """Получить уровень навыка (0-5)."""
    if skill in skill_tracker:
        return int(skill_tracker[skill]["level"])
    return 0


def get_all_skills(skill_tracker: dict[str, Any]) -> list[dict[str, Any]]:
    """Получить все навыки с прогрессом."""
    result = []
    for name, data in skill_tracker.items():
        result.append(
            {
                "name": name,
                "level": data["level"],
                "xp": data["xp"],
                "attempts": data["attempts"],
                "successes": data["successes"],
                "success_rate": round(data["successes"] / data["attempts"] * 100, 1)
                if data["attempts"] > 0
                else 0,
                "last_practice": data.get("last_practice", 0),
            }
        )
    return sorted(result, key=lambda x: x["level"], reverse=True)


def apply_skill_decay(
    skill_tracker: dict[str, Any],
    decay_days: int = 7,
    decay_rate: float = 0.10,
) -> list[str]:
    """Применить decay к навыкам, которые не практиковались decay_days дней.

    Возвращает список навыков, которые были уменьшены.
    """
    now = time.time()
    decay_seconds = decay_days * 86400
    decayed = []

    for name, data in skill_tracker.items():
        last_practice = data.get("last_practice", 0)
        if last_practice > 0 and (now - last_practice) > decay_seconds:
            old_xp = data["xp"]
            data["xp"] = max(0, int(old_xp * (1 - decay_rate)))
            data["level"] = min(5, data["xp"] // 50)
            if data["xp"] < old_xp:
                decayed.append(name)

    return decayed
