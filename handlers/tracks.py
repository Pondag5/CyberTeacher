"""
🎯 Handlers for path-based learning tracks (M-29)
"""
# isort: skip_file

import logging
import time
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from di import get_context
from track_engine import get_track_engine, Track
from handlers.types import HandlerResult


console = Console()
logger = logging.getLogger(__name__)


def handle_tracks(action: str, args: str = "") -> HandlerResult:
    """Main entry point for track commands"""
    parts = action.split(maxsplit=1)
    cmd = parts[0]
    subcmd = parts[1] if len(parts) > 1 else ""

    match cmd:
        case "list":
            return cmd_tracks_list()
        case "start":
            return cmd_track_start(subcmd)
        case "progress":
            return cmd_track_progress(subcmd)
        case "next":
            return cmd_track_next()
        case "complete":
            return cmd_track_complete_topic(subcmd)
        case "recommend":
            return cmd_track_recommend()
        case "reset":
            return cmd_track_reset(subcmd)
        case "status":
            return cmd_track_status()
        case _:
            help_text = """
🎯 **Track Commands:**

• `/tracks list` - показать все доступные треки
• `/tracks recommend` - получить персональные рекомендации
• `/tracks start <id>` - начать новый трек
• `/tracks progress [id]` - показать прогресс по треку
• `/tracks status` - текущий активный трек
• `/tracks next` - получить следующую тему
• `/tracks complete <topic_id>` - отметить тему пройденной
• `/tracks reset [id]` - сбросить прогресс трека (без аргумента - все)

**Примеры:**
• `/tracks start web-fundamentals`
• `/tracks next`
• `/tracks complete sql-injection`
"""
            return True, None, help_text, True


def cmd_tracks_list() -> HandlerResult:
    """Показать список всех доступных треков"""
    engine = get_track_engine()
    tracks = engine.list_tracks()
    completed_tracks = get_context().state.tracks_enrolled

    if not tracks:
        return True, None, "❌ Треки не найдены. Проверьте директорию ./tracks", True

    table = Table(
        title="📚 Доступные треки", show_header=True, header_style="bold cyan"
    )
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Название", style="white")
    table.add_column("Уровень", justify="center")
    table.add_column("Часов", justify="center")
    table.add_column("Адапт.", justify="center")
    table.add_column("Тем", justify="center")
    table.add_column("Статус", justify="center")

    level_emoji = {"beginner": "🌱", "intermediate": "🌿", "advanced": "🌳"}

    for track in sorted(tracks, key=lambda t: t.level):
        emoji = level_emoji.get(track.level, "📖")
        status = "✅ Пройден" if track.id in completed_tracks else "⏳ Доступен"
        table.add_row(
            track.id,
            f"{track.name}",
            f"{emoji} {track.level}",
            str(track.estimated_hours),
            "🔄" if track.adaptive else "-",
            str(len(track.topics)),
            status,
        )

    output = f"[bold]📚 ДОСТУПНЫЕ ТРЕКИ:[/bold]\nВсего: {len(tracks)} | Пройдено: {len([t for t in tracks if t.id in completed_tracks])}\n"
    console.print(Panel(table, border_style="cyan"))
    return True, None, output, True


def cmd_track_start(track_id: str) -> HandlerResult:
    """Начать трек"""
    if not track_id:
        return False, None, "❌ Укажи ID трека. Использование: `/tracks start <id>`", True

    engine = get_track_engine()
    track = engine.get_track(track_id)
    if not track:
        return False, None, f"❌ Трек '{track_id}' не найден. Используй `/tracks list` для списка.", True

    state = get_context().state

    if track.prerequisites:
        missing = [pid for pid in track.prerequisites if pid not in state.tracks_enrolled]
        if missing:
            prereq_names = ", ".join(missing)
            return False, None, f"❌ Не выполнены prereq: {prereq_names}. Пройди сначала: {prereq_names}", True

    if track_id in state.tracks_enrolled:
        prog = state.track_progress.get(track_id, {})
        curr_idx = prog.get("current_topic_idx", 0)
        return True, None, f"⚠️ Трек '{track.name}' уже начат. Текущая тема: {curr_idx + 1}. Используй `/tracks progress`", True
    state.tracks_enrolled.append(track_id)
    state.track_progress[track_id] = {
        "current_topic_idx": 0,
        "completed_topics": [],
        "started_at": time.time(),
        "completed_at": None,
    }
    state.save_to_file()

    first_topic = track.get_next_topic([], 0)
    if not first_topic:
        return True, None, f"✅ Трек '{track.name}' начат, но тем нет.", True
    output = f"""
╔══════════════════════════════════════════════════════╗
║  🎯 ТРЕК НАЧАТ: {track.name[:30]:<30} ║
╠══════════════════════════════════════════════════════╣
║  Уровень: {track.level}                                    ║
║  Тем: {len(track.topics)}                                     ║
║  Адаптивный: {"✅" if track.adaptive else "❌"}                    ║
╚══════════════════════════════════════════════════════╝

📌 **ТЕМА 1: {first_topic.title}**
   {first_topic.description}

🔧 **Лаборатория:** {first_topic.lab_id or "Не указана"}
📝 **Квиз:** /quiz {first_topic.quiz_topic or "N/A"}

💡 Следующие шаги:
   • Запусти лабу: `/lab start {first_topic.lab_id or "N/A"}`
   • Когда будешь готов, напиши `/tracks next` для следующей темы
   • Отметь тему как пройденную: `/tracks complete {first_topic.topic_id}`
"""
    return True, None, output, True


def cmd_track_progress(track_id: str = "") -> HandlerResult:
    """Показать прогресс по треку (или по всем трекам)"""
    state = get_context().state
    if not state.tracks_enrolled:
        return False, None, "❌ Ты ещё не начал ни одного трека. Используй `/tracks list` и `/tracks start <id>`", True

    if track_id:
        engine = get_track_engine()
        track = engine.get_track(track_id)
        if not track:
            return False, None, f"❌ Трек '{track_id}' не найден.", True
        prog = state.track_progress.get(track_id, {})
        return _render_track_progress(track, prog)
    else:
        output = "📊 **ПРОГРЕСС ПО ТРЕКАМ:**\n\n"
        engine = get_track_engine()
        for tid in state.tracks_enrolled:
            track = engine.get_track(tid)
            if track:
                prog = state.track_progress.get(tid, {})
                completed, total = track.progress(prog.get("completed_topics", []))
                pct = (completed / total * 100) if total > 0 else 0
                status = "✅ Завершён" if track.is_completed(prog.get("completed_topics", [])) else f"{completed}/{total} ({pct:.0f}%)"
                output += f"• **{track.name}** [{track.level}]: {status}\n"
            else:
                output += f"• Неизвестный трек: {tid}\n"
        output += "\n💡 Подробно: `/tracks progress <id>`"
        return True, None, output, True


def _render_track_progress(track: Track, prog: dict) -> HandlerResult:
    """Отобразить прогресс по одному треку"""
    completed_topics = prog.get("completed_topics", [])
    current_idx = prog.get("current_topic_idx", 0)
    started_at = prog.get("started_at")
    completed_at = prog.get("completed_at")

    completed_count, total_required = track.progress(completed_topics)
    is_completed = track.is_completed(completed_topics)

    status_lines = []
    if is_completed:
        status_lines.append("✅ ТРЕК ЗАВЕРШЁН!")
    else:
        status_lines.append(f"⏳ В прогрессе: {completed_count}/{total_required} тем")

    if started_at:
        start_dt = time.strftime("%Y-%m-%d %H:%M", time.localtime(started_at))
        status_lines.append(f"📅 Начат: {start_dt}")
    if completed_at:
        complete_dt = time.strftime("%Y-%m-%d %H:%M", time.localtime(completed_at))
        status_lines.append(f"🎉 Завершён: {complete_dt}")

    table = Table(show_header=True, header_style="bold yellow")
    table.add_column("#", justify="right", style="dim", width=3)
    table.add_column("Тема", style="white")
    table.add_column("Статус", justify="center", width=10)
    table.add_column("Лаба", style="cyan", width=15)
    table.add_column("Квиз", style="magenta", width=12)

    for i, topic in enumerate(track.topics, 1):
        status = "✅" if topic.topic_id in completed_topics else "⏳"
        if not is_completed and i == current_idx + 1 and topic.topic_id not in completed_topics:
            status = "🟡"
        lab = topic.lab_id or "-"
        quiz = topic.quiz_topic or "-"
        table.add_row(str(i), topic.title, status, lab, quiz)

    console.print(Panel(table, border_style="yellow", title=f"Темы ({total_required} всего)"))
    return True, None, "\n".join(status_lines), True
def cmd_track_next() -> HandlerResult:
    """Получить следующую тему текущего трека или указанного трека"""
    state = get_context().state
    if not state.tracks_enrolled:
        return False, None, "❌ Нет активных треков. Начни с `/tracks list` и `/tracks start <id>`", True

    current_track_id = state.learning_context.get("current_track")
    if not current_track_id or current_track_id not in state.tracks_enrolled:
        current_track_id = state.tracks_enrolled[-1]

    engine = get_track_engine()
    track = engine.get_track(current_track_id)
    if not track:
        return False, None, f"❌ Трек '{current_track_id}' не найден.", True

    prog = state.track_progress.get(current_track_id, {})
    current_idx = prog.get("current_topic_idx", 0)
    completed = prog.get("completed_topics", [])

    next_topic = track.get_next_topic(completed, current_idx)

    if not next_topic:
        if track.is_completed(completed):
            prog["completed_at"] = time.time()
            state.track_progress[current_track_id] = prog
            state.save_to_file()
            return True, None, f"🎉 Трек '{track.name}' завершён! Все обязательные темы пройдены.", True
        else:
            return True, None, f"⚠️ Все темы обработаны, но не все обязательные пройдены. Проверь прогресс: `/tracks progress {track.id}`", True
    prog["current_topic_idx"] = next_topic.order - 1
    state.track_progress[current_track_id] = prog
    state.save_to_file()

    output = f"""
╔══════════════════════════════════════════════════════╗
║  📌 ТЕМА {next_topic.order}: {next_topic.title[:28]:<28} ║
╚══════════════════════════════════════════════════════╝

{next_topic.description}

🔧 **Лаборатория:** {next_topic.lab_id or "Не указана"}
📝 **Квиз для проверки:** {next_topic.quiz_topic or "N/A"}
🎯 **Минимальный балл:** {next_topic.min_score}%

💡 **Что делать:**
1. Запусти лабу: `/lab start {next_topic.lab_id or "N/A"}`
2. Практикуйся, изучай материал
3. Пройди квиз: `/quiz {next_topic.quiz_topic or "N/A"}`
4. Когда тема готова, отметь: `/tracks complete {next_topic.topic_id}`
"""
    state.set_learning_context(action="track_next", course=current_track_id)
    return True, None, output, True


def cmd_track_complete_topic(topic_id: str) -> HandlerResult:
    """Отметить тему как пройденную"""
    if not topic_id:
        return False, None, "❌ Укажи ID темы. Использование: `/tracks complete <topic_id>`", True

    state = get_context().state
    if not state.tracks_enrolled:
        return False, None, "❌ Нет активных треков.", True

    engine = get_track_engine()
    current_track_id = state.learning_context.get("current_track") or state.tracks_enrolled[-1]
    track = engine.get_track(current_track_id)
    if not track:
        return False, None, f"❌ Трек '{current_track_id}' не найден.", True

    topic = track.get_topic_by_id(topic_id)
    if not topic:
        return False, None, f"❌ Тема '{topic_id}' не найдена в треке '{track.name}'.", True

    prog = state.track_progress.get(current_track_id, {"current_topic_idx": 0, "completed_topics": [], "started_at": time.time(), "completed_at": None})

    if topic_id in prog["completed_topics"]:
        return True, None, f"✅ Тема '{topic.title}' уже отмечена как пройденная.", True
    prog["completed_topics"].append(topic_id)

    if track.is_completed(prog["completed_topics"]):
        prog["completed_at"] = time.time()
        if current_track_id not in state.tracks_enrolled:
            state.tracks_enrolled.append(current_track_id)
        bonus = 50 * track.estimated_hours
        state.points += bonus
        msg = f"🎉 Трек '{track.name}' завершён! +{bonus} очков."
    else:
        msg = f"✅ Тема '{topic.title}' отмечена как пройденная."

    state.track_progress[current_track_id] = prog
    state.save_to_file()
    return True, None, msg, True


def cmd_track_recommend() -> HandlerResult:
    """Получить персональные рекомендации по трекам"""
    state = get_context().state
    engine = get_track_engine()

    weak_topics = state.get_weak_topics(threshold=70.0)
    completed_tracks = [t for t in state.tracks_enrolled if engine.get_track(t)]

    recommendations = engine.recommend_tracks(weak_topics, completed_tracks)

    if not recommendations:
        return False, None, "❌ Нет доступных треков для рекомендаций. Возможно, все пройдены или prerequisites не выполнены.", True

    output = "🎯 **РЕКОМЕНДАЦИИ НА ОСНОВЕ ТВОИХ СЛАБЫХ ТЕМ:**\n\n"
    if weak_topics:
        output += "🔴 Слабые темы:\n"
        for wt in weak_topics[:5]:
            output += f"  • {wt['topic']} (успешность: {wt['success_rate']:.0f}%)\n"
        output += "\n"

    output += "📚 **Рекомендуемые треки:**\n\n"
    for i, (track, score) in enumerate(recommendations[:5], 1):
        marker = "🔥" if i == 1 else f"{i}."
        output += f"{marker} **{track.name}** [{track.level}] - {track.description[:60]}...\n"
        adapt = "✅" if track.adaptive else "❌"
        output += f"   Тем: {len(track.topics)} | Адаптивность: {adapt}\n"
        output += f"   Начать: `/tracks start {track.id}`\n\n"

    return True, None, output, True


def cmd_track_reset(track_id: str = "") -> HandlerResult:
    """Сбросить прогресс трека (или всех треков)"""
    state = get_context().state
    if not track_id:
        return False, None, "⚠️ Сбросить ВСЕ треки? Это удалит весь прогресс. Используй `/tracks reset <id>` для конкретного трека.", True

    engine = get_track_engine()
    track = engine.get_track(track_id)
    if not track:
        return False, None, f"❌ Трек '{track_id}' не найден.", True

    if track_id in state.tracks_enrolled:
        state.tracks_enrolled.remove(track_id)
    if track_id in state.track_progress:
        del state.track_progress[track_id]
    state.save_to_file()
    return True, None, f"✅ Прогресс трека '{track.name}' сброшен.", True
def cmd_track_status() -> HandlerResult:
    """Показать текущий активный трек"""
    state = get_context().state
    current = state.learning_context.get("current_track")

    if not current and state.tracks_enrolled:
        current = state.tracks_enrolled[-1]

    if not current:
        return False, None, "❌ Нет активного трека. Начни с `/tracks start <id>`", True

    engine = get_track_engine()
    track = engine.get_track(current)
    if not track:
        return False, None, f"❌ Трек '{current}' не найден.", True

    prog = state.track_progress.get(current, {})
    completed, total = track.progress(prog.get("completed_topics", []))
    pct = (completed / total * 100) if total > 0 else 0

    output = f"""
🎯 **АКТИВНЫЙ ТРЕК:** {track.name}
📊 Прогресс: {completed}/{total} ({pct:.0f}%)
Уровень: {track.level}
Адаптивный: {"✅" if track.adaptive else "❌"}

💡 Команды:
   /tracks next - следующая тема
   /tracks progress - подробный прогресс
   /tracks complete <topic_id> - отметить тему
"""
    return True, None, output, True