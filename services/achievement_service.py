"""
Achievement checking service.
"""

import json
import logging
import os
from typing import Any, Dict, List
from config import ACHIEVEMENTS_FILE

logger = logging.getLogger(__name__)

# Маппинг типов условий к атрибутам состояния
CONDITION_MAP: Dict[str, str] = {
    "flags_total": "total_flags_collected",
    "assignments_completed": "assignments_completed",
    "total_points": "points",
    "labs_started": "labs_started",
    "quizzes_taken": "quizzes_taken",
    "news_checked": "news_checked",
    "social_success": "social_success",
    "apt_groups_viewed": "apt_groups_viewed",
    "stealth_ops": "stealth_ops",
    "threat_exposures": "threat_exposures",
}


def load_achievements() -> List[Dict[str, Any]]:
    """Загрузить список достижений из JSON-файла."""
    if not os.path.exists(ACHIEVEMENTS_FILE):
        return []
    try:
        with open(ACHIEVEMENTS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("achievements", [])
    except Exception as e:
        logger.error(f"Ошибка загрузки достижений: {e}")
        return []


def check_achievement(
    achievement: Dict[str, Any],
    earned_achievements: List[str],
    state_getter,
) -> bool:
    """Проверить, выполнено ли конкретное достижение."""
    ach_id = achievement.get("id")
    if not ach_id or ach_id in earned_achievements:
        return False

    cond = achievement.get("condition", {})
    cond_type = cond.get("type")
    threshold = cond.get("threshold", 0)

    attr_name = CONDITION_MAP.get(cond_type)
    if attr_name is None:
        return False

    current_value = state_getter(attr_name)
    return current_value >= threshold


def check_achievements(
    earned_achievements: List[str],
    state_getter,
    state_setter,
) -> List[Dict[str, Any]]:
    """Проверить все достижения и вернуть newly earned."""
    achievements_list = load_achievements()
    if not achievements_list:
        return []

    newly_earned = []
    for ach in achievements_list:
        if check_achievement(ach, earned_achievements, state_getter):
            ach_id = ach["id"]
            earned_achievements.append(ach_id)

            xp = ach.get("points", 0)
            if xp > 0:
                current_points = state_getter("points")
                multiplier = state_getter("xp_multiplier")
                state_setter("points", current_points + xp * multiplier)

            newly_earned.append(ach)

    return newly_earned
