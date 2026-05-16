"""
Shop, themes, and inventory management.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ShopState:
    """Shop, themes, and inventory management."""
    
    # Магазин (C-14)
    owned_themes: List[str] = field(default_factory=list)
    current_theme: str = "default"
    unlocked_topics: List[str] = field(default_factory=list)
    hint_credits: int = 0  # available manual hints

    # XP Boosts (хранятся здесь для удобства, хотя логически относятся к достижениям)
    xp_boost_multiplier: float = 1.0
    xp_boost_expiry: float = 0.0  # timestamp

    # Экипировка (H-02) — выбранные инструменты и их использование
    selected_tools: List[str] = field(default_factory=list)

    # Таймер Trace (H-03) — для лабораторий с ограничением времени
    trace_deadline: Optional[float] = None
    trace_hint: Optional[str] = None

    # Прогресс миссий (H-05)
    missions_completed: List[str] = field(default_factory=list)
    active_mission: Optional[str] = None

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
            import time

            self.xp_boost_multiplier = multiplier
            self.xp_boost_expiry = time.time() + duration_hours * 3600
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
        import time

        now = time.time()
        if self.xp_boost_expiry > 0 and now < self.xp_boost_expiry:
            return self.xp_boost_multiplier
        # Бонус истек или не установлен — сбрасываем
        self.xp_boost_multiplier = 1.0
        self.xp_boost_expiry = 0.0
        return 1.0