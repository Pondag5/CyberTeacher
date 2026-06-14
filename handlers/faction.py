"""
Faction reputation system.

Rick vs Ghost — выбор личности учителя влияет на стиль подсказок.
"""

from typing import Optional

from state import get_state


FACTIONS = {
    "rick": "Rick — циник и гений",
    "ghost": "Ghost — параноик и шептун",
    "archive": "Archive — хранитель знаний",
}


def get_factions() -> dict:
    state = get_state()
    rep = getattr(state, "faction_reputation", {"rick": 0, "ghost": 0, "archive": 0})
    chosen = getattr(state, "faction_chosen", None)
    return {
        "rick": rep.get("rick", 0),
        "ghost": rep.get("ghost", 0),
        "archive": rep.get("archive", 0),
        "chosen": chosen,
        "dominant": _get_dominant(rep),
    }


def _get_dominant(rep: dict) -> Optional[str]:
    best = max(rep, key=rep.get) if rep else None
    return best if rep.get(best, 0) > 0 else None


def choose_faction(faction: str) -> str:
    state = get_state()
    if faction not in FACTIONS:
        return "❌ Выбери: rick, ghost или archive."
    state.faction_chosen = faction
    rep = getattr(state, "faction_reputation", {"rick": 0, "ghost": 0, "archive": 0})
    rep[faction] = max(rep.get(faction, 0), 10)
    state.faction_reputation = rep
    return f"✅ Ты выбрал {FACTIONS[faction]}. Это повлияет на стиль подсказок и доступные лабы."


def add_faction_rep(faction: str, amount: int = 5) -> str:
    state = get_state()
    rep = getattr(state, "faction_reputation", {"rick": 0, "ghost": 0, "archive": 0})
    if faction in rep:
        rep[faction] += amount
        state.faction_reputation = rep
    return ""
