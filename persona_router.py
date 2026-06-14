"""Persona Router — dynamic persona selection per request.

Routes to one of: rick, doc, analyst, ghost, auto (based on context).
"""

import logging
from typing import Any, Dict, Optional

from state import get_state

logger = logging.getLogger(__name__)

PERSONAS = {
    "rick": {
        "name": "Rick",
        "emoji": "🧪",
        "prompt": (
            "\n\n[PERSONA: RICK] Ты — Рик Санчес. Хаотичный гениальный ученый. "
            "Саркастичен, циничен, не терпишь глупость. Говоришь прямо, "
            "без лишних церемоний. Иногда ломаешь четвёртую стену. "
            "Стиль: дерзкий, непредсказуемый, гениальный."
        ),
    },
    "doc": {
        "name": "Doc Brown",
        "emoji": "⚡",
        "prompt": (
            "\n\n[PERSONA: DOC] Ты — Доктор Эмметт Браун. Энтузиастичный изобретатель. "
            "Говоришь с восторгом, используешь научную лексику, любишь метафоры "
            "про время и пространство. Вдохновляешь, поддерживаешь, веришь в ученика. "
            "Стиль: энергичный, вдохновляющий, немного безумный."
        ),
    },
    "analyst": {
        "name": "Analyst",
        "emoji": "🔍",
        "prompt": (
            "\n\n[PERSONA: ANALYST] Ты — Холодный Аналитик. Точен, лаконичен, "
            "технически максимально точно. Никакой воды, никаких эмоций. "
            "Только факты, команды, векторы атаки, сниппеты. "
            "Стиль: профессиональный, сухой, авторитетный."
        ),
    },
    "ghost": {
        "name": "Ghost",
        "emoji": "👻",
        "prompt": (
            "\n\n[PERSONA: GHOST] Ты — Призрак. Параноидальный опсековый эксперт. "
            "Говоришь шепотом, намеками. Всегда про безопасность, следы, анонимность. "
            "Подозрительно относишься ко всему. Учишь невидимости. "
            "Стиль: тёмный, осторожный, глубокий."
        ),
    },
}

AUTO_TRIGGERS = [
    ("high_risk", ["risk_high", "noise_high", "cp_high"], "ghost"),
    ("code_review", ["review", "code", "security", "audit"], "analyst"),
    ("late_night", ["is_night", "3am", "witching"], "doc"),
    ("chaos_mode", ["reckless", "exploit", "brute", "scan", "aggressive"], "rick"),
    ("stealth_mode", ["stealth_on", "opsec", "wipe", "hide", "anonymous"], "ghost"),
    ("learning", ["quiz", "course", "lesson", "study", "explain"], "doc"),
]


def _get_context_hints(state) -> Dict[str, Any]:
    """Extract relevant context for auto-routing."""
    from datetime import datetime

    hour = datetime.now().hour
    is_night = hour >= 22 or hour <= 5
    return {
        "risk_high": getattr(state, "risk_level", 0) >= 70,
        "noise_high": getattr(state, "noise_level", 0) >= 70,
        "cp_high": getattr(state, "cp_level", 0) >= 70,
        "stealth_on": getattr(state, "stealth_mode", False),
        "is_night": is_night,
    }


def _matches_triggers(triggers: list, context: Dict[str, Any], user_msg: str) -> bool:
    msg_lower = user_msg.lower()
    for t in triggers:
        if t in context and context[t]:
            return True
        if t in msg_lower:
            return True
    return False


def select_persona(state, user_message: str = "", forced: str = None) -> str:
    """Select persona for this request."""
    # Explicit override
    if forced and forced in PERSONAS:
        return forced
    if forced == "auto" or forced is None:
        # Check user preference
        pref = getattr(state, "preferred_persona", "auto")
        if pref != "auto" and pref in PERSONAS:
            return pref
        # Auto-routing based on context
        context = _get_context_hints(state)
        for _, triggers, persona in AUTO_TRIGGERS:
            if _matches_triggers(triggers, context, user_message):
                return persona
    # Default
    return "rick"


def get_persona_prompt(persona_id: str) -> str:
    """Get system prompt modifier for persona."""
    return PERSONAS.get(persona_id, PERSONAS["rick"])["prompt"]


def get_persona_info(persona_id: str) -> Dict[str, Any]:
    """Get persona metadata for UI."""
    p = PERSONAS.get(persona_id, PERSONAS["rick"])
    return {"id": persona_id, "name": p["name"], "emoji": p["emoji"]}


def list_personas() -> list:
    return [
        {"id": k, "name": v["name"], "emoji": v["emoji"]} for k, v in PERSONAS.items()
    ]


def set_preferred_persona(persona_id: str) -> bool:
    if persona_id in PERSONAS or persona_id == "auto":
        state = get_state()
        state.preferred_persona = persona_id
        return True
    return False


def get_preferred_persona() -> str:
    state = get_state()
    return getattr(state, "preferred_persona", "auto")
