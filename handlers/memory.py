"""
Teacher memory — персонализированная память учителя.

Учитель запоминает действия ученика и ссылается на них.
"""

from typing import Optional

from state import get_state


def record_memory(action: str, detail: str = "") -> None:
    """Записать воспоминание о действии ученика."""
    state = get_state()
    memories = getattr(state, "student_memories", [])
    entry = f"{action}"
    if detail:
        entry += f": {detail}"
    if entry not in memories:
        memories.append(entry)
        state.student_memories = memories


def get_random_memory() -> Optional[str]:
    """Вернуть случайное воспоминание для вставки в ответ учителя."""
    state = get_state()
    memories = getattr(state, "student_memories", [])
    if not memories:
        return None
    import random

    mem = random.choice(memories)
    prefixes = [
        "Помнишь, как",
        "Кстати, ты когда",
        "А я помню,",
        "Не забуду, как ты",
        "Помню-помню: ты",
    ]
    import random as rnd

    prefix = rnd.choice(prefixes)
    return f"{prefix} {mem}?"
