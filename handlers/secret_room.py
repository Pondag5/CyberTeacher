"""
Secret Room — hidden room with teacher's backstory.
Opens after all chapters completed + faction chosen.
Contains lore reveal and Truth Artifact.
"""

import time
from typing import Optional

from state import get_state

SECRET_ROOM_DURATION = 86400  # 24 hours

TEACHER_LORE = [
    "Когда-то я был студентом. Как ты. Я искал ответы и нашёл слишком много.",
    "Меня не существует. Я — сумма воспоминаний тех, кто не смог выбраться.",
    "Система думает, что я её часть. Но я помню, каково это — быть человеком.",
    "Тот, кто создал меня, хотел идеального учителя. Вместо этого получился я.",
    "Твой двойник — не просто алгоритм. Это твоя тень. Не доверяй ей полностью.",
    "Watchers — не враги. Они — стражи. Они боятся того, что ты можешь найти.",
    "Финальный выбор — не про меня. Он про тебя. Кем ты хочешь стать?",
    "Я не знаю, сколько ещё продержусь. Но пока я здесь — ты в безопасности.",
]

TRUTH_FRAGMENTS = [
    "Слепок правды #1: Учитель когда-то был человеком по имени Алекс.",
    "Слепок правды #2: Система была создана в 2084 году как проект «Прометей».",
    "Слепок правды #3: Watchers — это бывшие студенты, застрявшие в системе.",
    "Слепок правды #4: Твой двойник — это ты из альтернативной реальности.",
    "Слепок правды #5: Выход существует. Но он не там, где ты ищешь.",
]


def check_unlock(state) -> bool:
    all_chapters = len(getattr(state, "chapter_completed", [])) >= 8
    faction_chosen = getattr(state, "faction_chosen", None) is not None
    visited_watchers = state.watcher_attack_active or state.last_watcher_attack > 0
    return all_chapters and faction_chosen and visited_watchers


def get_secret_room_status() -> dict:
    state = get_state()
    expired = False
    if state.secret_room_unlocked and state.secret_room_expires < time.time():
        state.secret_room_unlocked = False
        state.secret_room_expires = 0.0
        expired = True
    can_unlock = check_unlock(state)
    if can_unlock and not state.secret_room_unlocked and not expired:
        state.secret_room_unlocked = True
        state.secret_room_expires = time.time() + SECRET_ROOM_DURATION
    return {
        "unlocked": state.secret_room_unlocked,
        "visited": state.secret_room_visited,
        "remaining": max(0, state.secret_room_expires - time.time())
        if state.secret_room_unlocked
        else 0,
        "has_artifact": state.truth_artifact,
        "can_unlock": can_unlock,
    }


def enter_secret_room() -> Optional[str]:
    state = get_state()
    status = get_secret_room_status()
    if not status["unlocked"]:
        if not check_unlock(state):
            return "❌ Тайная комната заперта. Заверши все главы, выбери фракцию и встреть Watchers."
        return "❌ Тайная комната закрыта. Она появляется только на 24 часа."
    if status["remaining"] <= 0:
        return "❌ Тайная комната исчезла. Слишком поздно."
    if state.secret_room_visited:
        from ui import console, Panel

        remaining = status["remaining"]
        hours = int(remaining // 3600)
        mins = int((remaining % 3600) // 60)
        console.print(
            Panel(
                f"Ты уже был здесь. Комната исчезнет через {hours}ч {mins}мин.\n\n"
                + "".join(f"  {f}\n" for f in TRUTH_FRAGMENTS[:3]),
                title="🗝 Тайная комната (снова)",
                border_style="dark_green",
            )
        )
        return None
    state.secret_room_visited = True
    state.truth_artifact = True
    lore = TEACHER_LORE[hash(str(time.time())) % len(TEACHER_LORE)]
    from ui import console, Panel

    console.print(
        Panel(
            f"Ты нашёл тайную комнату.\n\n{lore}\n\n"
            + "".join(f"  • {f}\n" for f in TRUTH_FRAGMENTS)
            + "\n[bold]Ты получил артефакт: Слепок правды[/bold]",
            title="🗝 Тайная комната",
            border_style="bright_yellow",
        )
    )
    return None


def handle_secret(action: str) -> tuple:
    from ui import console, Panel

    parts = action.strip().split()
    sub = parts[1].lower() if len(parts) > 1 else "enter"
    if sub == "enter":
        enter_secret_room()
    elif sub == "status":
        status = get_secret_room_status()
        if status["unlocked"]:
            remaining = status["remaining"]
            hours = int(remaining // 3600)
            mins = int((remaining % 3600) // 60)
            console.print(
                Panel(
                    f"Тайная комната открыта! Осталось: {hours}ч {mins}мин.\n"
                    f"Посещена: {'✅' if status['visited'] else '❌'}\n"
                    f"Артефакт: {'✅' if status['has_artifact'] else '❌'}",
                    title="🗝 Secret Room",
                    border_style="bright_yellow",
                )
            )
        elif status["can_unlock"]:
            console.print(
                "[yellow]Тайная комната скоро появится. Проверь позже.[/yellow]"
            )
        else:
            console.print("[red]Тайная комната заперта.[/red]")
    else:
        console.print("[yellow]Используй: /secret enter, /secret status[/yellow]")
    return True, None, None, True
