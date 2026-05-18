"""
Shop, themes, and inventory management.
"""

import time
from typing import List, Optional

from pydantic import BaseModel, Field


class ShopState(BaseModel):
    """Shop, themes, and inventory management."""
    
    # Магазин (C-14)
    owned_themes: list[str] = Field(default_factory=list)
    current_theme: str = Field(default="default")
    unlocked_topics: list[str] = Field(default_factory=list)
    hint_credits: int = Field(default=0, ge=0)  # available manual hints

    # XP Boosts (хранятся здесь для удобства, хотя логически относятся к достижениям)
    xp_boost_multiplier: float = Field(default=1.0, ge=0.0)
    xp_boost_expiry: float = Field(default=0.0, ge=0.0)  # timestamp

    # Экипировка (H-02) — выбранные инструменты и их использование
    selected_tools: list[str] = Field(default_factory=list)

    # Таймер Trace (H-03) — для лабораторий с ограничением времени
    trace_deadline: float | None = None
    trace_hint: str | None = None

    # Прогресс миссий (H-05)
    missions_completed: list[str] = Field(default_factory=list)
    active_mission: str | None = None

    def apply_item_effect(self, item: dict) -> str:
        """Применить эффект купленного предмета к состоянию.
        
        Returns:
            str: The type of effect applied, or None if not handled.
                Possible values: "theme", "unlock_topic", "xp_boost", "hint_credit"
        """
        item_type = item.get("type")
        if item_type == "theme":
            theme_id = item.get("value")
            if theme_id and theme_id not in self.owned_themes:
                self.owned_themes.append(theme_id)
                return "theme"
        elif item_type == "unlock_topic":
            topic = item.get("value")
            if topic and topic not in self.unlocked_topics:
                self.unlocked_topics.append(topic)
                return "unlock_topic"
        elif item_type == "xp_boost":
            multiplier = item.get("multiplier", 2.0)
            duration_hours = item.get("duration_hours", 1)
            self.xp_boost_multiplier = max(0.0, multiplier)
            self.xp_boost_expiry = time.time() + max(0.0, duration_hours) * 3600
            return "xp_boost"
        elif item_type == "consumable":
            effect = item.get("effect")
            qty = item.get("quantity", 1)
            if effect == "hint_credit":
                self.hint_credits += qty
                return "hint_credit"
        return None

    def get_xp_multiplier(self) -> float:
        """Возвращает текущий множитель XP с учетом активного буста."""
        now = time.time()
        if self.xp_boost_expiry > 0 and now < self.xp_boost_expiry:
            return self.xp_boost_multiplier
        # Бонус истек или не установлен — сбрасываем
        self.xp_boost_multiplier = 1.0
        self.xp_boost_expiry = 0.0
        return 1.0

    model_config = {
        "validate_assignment": True
    }
