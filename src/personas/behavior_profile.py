"""Hidden behavioral profile — tracks player traits and determines archetype.

Traits (0-100):
  curiosity   — explores new topics, asks questions
  recklessness — takes risks, ignores warnings
  discipline  — follows courses, completes tasks
  creativity  — novel approaches, unusual solutions
  opsec       — covers tracks, uses stealth

Archetypes:
  analyst      — high discipline + opsec
  researcher   — high curiosity + creativity
  script_kiddie — high recklessness, low discipline/opsec
  engineer     — balanced (default)
  ghost        — very high opsec + discipline
  chaotic      — high creativity + low discipline
"""

from typing import Any, Dict, Optional

TRAITS = ["curiosity", "recklessness", "discipline", "creativity", "opsec"]

ARCHETYPES: Dict[str, Dict[str, Any]] = {
    "engineer": {
        "name": "Инженер",
        "emoji": "\u2699\ufe0f",
        "desc": "Прагматичный профессионал. Делает что нужно, без лишнего риска.",
        "prompt": "Ты прагматичен и профессионален. Ученик уравновешен — не рискует без нужды, но и не застревает в теории.",
    },
    "analyst": {
        "name": "Аналитик",
        "emoji": "\ud83d\udd0d",
        "desc": "Методичный и осторожный. Каждый шаг взвешен.",
        "prompt": "Ученик методичен и осторожен. Ценит структуру и теорию. Давай больше технических деталей, объясняй почему, а не только как.",
    },
    "researcher": {
        "name": "Исследователь",
        "emoji": "\ud83d\udcda",
        "desc": "Жаждущий знаний — лезет вглубь каждой темы.",
        "prompt": "Ученик любознателен. Он хочет копать вглубь. Поощряй исследование, предлагай смежные темы и расширяй контекст.",
    },
    "script_kiddie": {
        "name": "Script Kiddie",
        "emoji": "\ud83e\udd22",
        "desc": "Безрассудный новичок. Лезет напролом, не думая о последствиях.",
        "prompt": "Ученик безрассуден — рискует, игнорирует предупреждения, не думает о последствиях. Добавь больше предостережений. Напоминай про OPSEC. Будь строже.",
    },
    "ghost": {
        "name": "Ghost",
        "emoji": "\ud83d\udc7b",
        "desc": "Невидимка. Операционную безопасность возвёл в искусство.",
        "prompt": "Ученик — призрак. Он скрытен, осторожен и методичен. Он уже знает основы OPSEC. Отвечай на том же уровне — глубже, без лишних объяснений основ.",
    },
    "chaotic": {
        "name": "Chaotic Hacker",
        "emoji": "\ud83d\udca5",
        "desc": "Творческий хаос. Результат любой ценой, метод — опционально.",
        "prompt": "Ученик креативен, но хаотичен. Он может найти нестандартное решение, но пропускает базу. Направляй его энергию в продуктивное русло, но не гаси энтузиазм.",
    },
}


def get_profile(state) -> Dict[str, Any]:
    profile = getattr(state, "behavior_profile", None)
    if not profile or not isinstance(profile, dict):
        profile = {
            "curiosity": 25,
            "recklessness": 25,
            "discipline": 25,
            "creativity": 25,
            "opsec": 25,
            "stress": 0,
            "archetype": "engineer",
            "total_actions": 0,
        }
        state.behavior_profile = profile
    return profile


def _clamp(val: int) -> int:
    return max(0, min(100, val))


def _adjust(profile: Dict[str, Any], trait: str, delta: int) -> None:
    if trait in TRAITS or trait == "stress":
        profile[trait] = _clamp(profile.get(trait, 50) + delta)


def record_action(state, action_type: str, **kwargs) -> None:
    """Record a user action and adjust hidden traits."""
    profile = get_profile(state)
    profile["total_actions"] += 1

    if action_type == "quiz_pass":
        _adjust(profile, "discipline", 3)
        _adjust(profile, "stress", -2)

    elif action_type == "quiz_fail":
        _adjust(profile, "stress", 5)
        _adjust(profile, "curiosity", 1)

    elif action_type == "exploit_attempt":
        _adjust(profile, "recklessness", 4)
        _adjust(profile, "creativity", 2)
        _adjust(profile, "opsec", -2)
        _adjust(profile, "discipline", -1)

    elif action_type == "exploit_success":
        _adjust(profile, "creativity", 4)
        _adjust(profile, "recklessness", 2)
        _adjust(profile, "stress", -3)

    elif action_type == "stealth_toggle_on":
        _adjust(profile, "opsec", 3)
        _adjust(profile, "discipline", 1)

    elif action_type == "wipe_logs":
        _adjust(profile, "opsec", 4)
        _adjust(profile, "discipline", 1)

    elif action_type == "mission_start":
        _adjust(profile, "discipline", 2)
        _adjust(profile, "curiosity", 1)

    elif action_type == "mission_complete":
        _adjust(profile, "discipline", 3)
        _adjust(profile, "stress", -3)
        _adjust(profile, "creativity", 1)

    elif action_type == "course_lesson":
        _adjust(profile, "discipline", 2)
        _adjust(profile, "curiosity", 1)
        _adjust(profile, "stress", -1)

    elif action_type == "new_topic":
        _adjust(profile, "curiosity", 3)
        _adjust(profile, "creativity", 1)

    elif action_type == "ctf_flag":
        _adjust(profile, "creativity", 3)
        _adjust(profile, "recklessness", 2)
        _adjust(profile, "opsec", -1)

    elif action_type == "social_attack":
        _adjust(profile, "recklessness", 3)
        _adjust(profile, "creativity", 2)
        _adjust(profile, "opsec", -3)

    elif action_type == "night_session":
        _adjust(profile, "curiosity", 2)
        _adjust(profile, "recklessness", 1)
        _adjust(profile, "stress", 2)

    elif action_type == "long_session":
        _adjust(profile, "stress", 3)
        _adjust(profile, "curiosity", 1)

    _detect_archetype(profile)


def _detect_archetype(profile: Dict[str, Any]) -> str:
    """Determine archetype based on current trait scores."""
    curiosity = profile.get("curiosity", 25)
    recklessness = profile.get("recklessness", 25)
    discipline = profile.get("discipline", 25)
    creativity = profile.get("creativity", 25)
    opsec = profile.get("opsec", 25)

    if profile["total_actions"] < 10:
        profile["archetype"] = "engineer"
        return "engineer"

    scores = {
        "analyst": discipline * 0.6 + opsec * 0.4,
        "researcher": curiosity * 0.5 + creativity * 0.3 + discipline * 0.2,
        "script_kiddie": recklessness * 0.6
        + (100 - discipline) * 0.2
        + (100 - opsec) * 0.2,
        "ghost": opsec * 0.5 + discipline * 0.3 + (100 - recklessness) * 0.2,
        "chaotic": creativity * 0.5 + recklessness * 0.2 + (100 - discipline) * 0.3,
        "engineer": 50,
    }

    best = max(scores, key=scores.get)
    profile["archetype"] = best
    return best


def get_archetype(state) -> str:
    profile = get_profile(state)
    return profile.get("archetype", "engineer")


def get_archetype_prompt_modifier(state) -> Optional[str]:
    """Return a prompt modifier string based on current archetype."""
    profile = get_profile(state)
    archetype_id = profile.get("archetype", "engineer")
    info = ARCHETYPES.get(archetype_id)
    if not info:
        return None

    return (
        f"\n\n---\n"
        f"Поведенческий профиль ученика: {info['emoji']} {info['name']}\n"
        f"{info['prompt']}"
    )


def get_profile_summary(state) -> Dict[str, Any]:
    profile = get_profile(state)
    archetype_id = profile.get("archetype", "engineer")
    archetype_info = ARCHETYPES.get(archetype_id, ARCHETYPES["engineer"])
    return {
        "traits": {k: profile.get(k, 0) for k in TRAITS},
        "stress": profile.get("stress", 0),
        "archetype": {
            "id": archetype_id,
            "name": archetype_info["name"],
            "emoji": archetype_info["emoji"],
            "desc": archetype_info["desc"],
        },
        "total_actions": profile.get("total_actions", 0),
    }
