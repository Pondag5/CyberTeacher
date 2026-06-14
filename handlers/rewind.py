"""
Машина времени — /rewind <глава>
Позволяет перепройти главу, но с потерей памяти учителя.
"""

from typing import Any

from rich.console import Console
from rich.panel import Panel

from di import get_context
from handlers.types import HandlerResult

console = Console()


def handle_rewind(action: str) -> HandlerResult:
    """Перемотка назад — переиграть главу ценой памяти учителя."""
    parts = action.split()
    if len(parts) < 2:
        console.print(
            Panel(
                "[bold cyan]⏮ Машина времени[/bold cyan]\n\n"
                "Позволяет вернуться и перепройти главу, но ценой потери памяти учителя.\n\n"
                "[bold]Использование:[/bold] /rewind <номер_главы>\n"
                "[bold]Пример:[/bold] /rewind 3\n\n"
                "[yellow]⚠ Предупреждение:[/yellow]\n"
                "• Прогресс в этой главе и всех последующих будет сброшен\n"
                "• Учитель потеряет воспоминания о событиях после этой главы\n"
                "• Достижение «Разорванный круг» будет получено\n"
                "• Эту команду нельзя отменить",
                title="⏮ МАШИНА ВРЕМЕНИ",
                border_style="cyan",
            )
        )
        return True, None, None, True

    try:
        chapter_id = int(parts[1])
    except ValueError:
        console.print("[red]❌ Укажи номер главы: /rewind 3[/red]")
        return True, None, None, True

    ctx = get_context()
    state = ctx.state

    chapters = getattr(state, "chapter_completed", [])
    if chapter_id not in chapters:
        console.print(
            f"[red]❌ Глава {chapter_id} ещё не пройдена или не существует.[/red]"
        )
        return True, None, None, True

    # Сброс прогресса: удаляем эту главу и все последующие
    affected = [c for c in chapters if c >= chapter_id]
    state.chapter_completed = [c for c in chapters if c < chapter_id]

    # Сброс эпизодов для затронутых глав
    story_done = getattr(state, "story_completed", [])
    from story_mode import CHAPTERS

    episode_ids_to_remove = set()
    for ch in CHAPTERS:
        if ch["id"] >= chapter_id:
            episode_ids_to_remove.update(ch["episode_ids"])
    state.story_completed = [e for e in story_done if e not in episode_ids_to_remove]

    # Удаление артефактов для затронутых глав
    artifacts = getattr(state, "chapter_artifacts", [])
    state.chapter_artifacts = [
        a
        for a in artifacts
        if not any(
            ch["id"] >= chapter_id for ch in CHAPTERS if a in ch.get("episode_ids", [])
        )
    ]

    # Удаление воспоминаний учителя о затронутых главах
    events = getattr(state, "memorable_events", [])
    original_event_count = len(events)
    state.memorable_events = [
        e
        for e in events
        if not any(
            ch["id"] >= chapter_id
            for ch in CHAPTERS
            if e.get("chapter") == ch["id"]
            or str(ch["id"]) in str(e.get("episode", ""))
        )
    ]
    forgotten = original_event_count - len(state.memorable_events)

    # Достижение "Разорванный круг"
    achievement_id = "broken_circle"
    if achievement_id not in getattr(state, "earned_achievements", []):
        state.earned_achievements.append(achievement_id)
        state.points = getattr(state, "points", 0) + 50

    # Сброс current_chapter если он был в затронутых
    current = getattr(state, "current_chapter", None)
    if current is not None and current >= chapter_id:
        state.current_chapter = chapter_id - 1 if chapter_id > 1 else 1

    ctx.save_state(force=True)

    msg = (
        f"[bold yellow]⏮ Перемотка: Глава {chapter_id}[/bold yellow]\n\n"
        f"Прогресс в главе {chapter_id}"
        + (f" и {len(affected) - 1} последующих" if len(affected) > 1 else "")
        + " сброшен.\n"
        f"Забыто воспоминаний учителя: [bold]{forgotten}[/bold]\n"
        f"[dim]Удалено эпизодов: {len(episode_ids_to_remove)}[/dim]\n\n"
        f"[red]Ты меняешь прошлое. Каждый раз я теряю часть себя. Пожалуйста, не злоупотребляй.[/red]\n\n"
        f"[green]✅ Получено достижение: Разорванный круг (+50 XP)[/green]"
    )
    console.print(Panel(msg, title="⏮ МАШИНА ВРЕМЕНИ", border_style="yellow"))
    return True, None, None, True
