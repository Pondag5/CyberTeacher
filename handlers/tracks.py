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

console = Console()
logger = logging.getLogger(__name__)


def handle_tracks(action: str, args: str = "") -> tuple[bool, str, Any]:
    """Main entry point for track commands"""
    parts = action.split(maxsplit=1)
    cmd = parts[0]
    subcmd = parts[1] if len(parts) > 1 else ""
    # args is reserved for future use (currently unused)

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
            return True, help_text, None


def cmd_tracks_list() -> tuple[bool, str, None]:
    """Показать список всех доступных треков"""
    engine = get_track_engine()
    tracks = engine.list_tracks()
    completed_tracks = (
        get_context().state.tracks_enrolled
    )  # используем tracks_enrolled как completed

    if not tracks:
        return True, "❌ Треки не найдены. Проверьте директорию ./tracks", None

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
        # Привести completed_tracks к списку строк если это не список
        if isinstance(completed_tracks, list):
            status = "✅ Пройден" if track.id in completed_tracks else "⏳ Доступен"
        else:
            status = "⏳ Доступен"
        table.add_row(
            track.id,
            f"{track.name}",
            f"{emoji} {track.level}",
            str(track.estimated_hours),
            "🔄" if track.adaptive else "-",
            str(len(track.topics)),
            status,
        )

    output = "[bold]📚 ДОСТУПНЫЕ ТРЕКИ:[/bold]\n"
    completed_count = len([t for t in tracks if t.id in completed_tracks])
    output += f"Всего: {len(tracks)} | Пройдено: {completed_count}\n\n"
    return True, Panel(table, border_style="cyan"), None


def cmd_track_start(track_id: str) -> tuple[bool, str, None]:
    """Начать трек"""
    if not track_id:
        return False, "❌ Укажи ID трека. Использование: `/tracks start <id>`", None

    engine = get_track_engine()
    track = engine.get_track(track_id)
    if not track:
        return (
            False,
            f"❌ Трек '{track_id}' не найден. Используй `/tracks list` для списка.",
            None,
        )

    state = get_context().state

    # Проверить prerequisites
    if track.prerequisites:
        missing = [
            pid for pid in track.prerequisites if pid not in state.tracks_enrolled
        ]
        if missing:
            prereq_names = ", ".join(missing)
            return (
                False,
                "❌ Не выполнены prereq: "
                + prereq_names
                + ". Пройди сначала: "
                + prereq_names,
                None,
            )

    # Если уже enrolled, показать прогресс
    if track_id in state.tracks_enrolled:
        prog = state.track_progress.get(track_id, {})
        curr_idx = prog.get("current_topic_idx", 0)
        return (
            True,
            f"⚠️ Трек '{track.name}' уже начат. "
            f"Текущая тема: {curr_idx + 1}. "
            "Используй `/tracks progress`",
            None,
        )

    # Записаться на трек
    state.tracks_enrolled.append(track_id)
    state.track_progress[track_id] = {
        "current_topic_idx": 0,
        "completed_topics": [],
        "started_at": time.time(),
        "completed_at": None,
    }
    state.save_to_file()

    # Показать первую тему
    first_topic = track.get_next_topic([], 0)
    if not first_topic:
        return True, f"✅ Трек '{track.name}' начат, но тем нет.", None

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
    return True, output, None


def cmd_track_progress(track_id: str = "") -> tuple[bool, str, None]:
    """Показать прогресс по треку (или по всем трекам)"""
    state = get_context().state
    if not state.tracks_enrolled:
        return (
            False,
            "❌ Ты ещё не начал ни одного трека. "
            "Используй `/tracks list` и `/tracks start <id>`",
            None,
        )

    if track_id:
        # Прогресс по конкретному треку
        engine = get_track_engine()
        track = engine.get_track(track_id)
        if not track:
            return False, f"❌ Трек '{track_id}' не найден.", None

        prog = state.track_progress.get(track_id, {})
        return _render_track_progress(track, prog)
    else:
        # Обзор всех треков
        output = "📊 **ПРОГРЕСС ПО ТРЕКАМ:**\n\n"
        engine = get_track_engine()
        for tid in state.tracks_enrolled:
            track = engine.get_track(tid)
            if track:
                prog = state.track_progress.get(tid, {})
                completed, total = track.progress(prog.get("completed_topics", []))
                pct = (completed / total * 100) if total > 0 else 0
                status = (
                    "✅ Завершён"
                    if track.is_completed(prog.get("completed_topics", []))
                    else f"{completed}/{total} ({pct:.0f}%)"
                )
                output += f"• **{track.name}** [{track.level}]: {status}\n"
            else:
                output += f"• Неизвестный трек: {tid}\n"

        output += "\n💡 Подробно: `/tracks progress <id>`"
        return True, output, None


def _render_track_progress(track: Track, prog: dict) -> tuple[bool, str, None]:
    """Отобразить прогресс по одному треку"""
    completed_topics = prog.get("completed_topics", [])
    current_idx = prog.get("current_topic_idx", 0)
    started_at = prog.get("started_at")
    completed_at = prog.get("completed_at")

    completed_count, total_required = track.progress(completed_topics)
    is_completed = track.is_completed(completed_topics)

    # Статус
    status_lines = []
    if is_completed:
        status_lines.append("✅ ТРЕК ЗАВЕРШЁН!")
    else:
        status_lines.append(f"⏳ В прогрессе: {completed_count}/{total_required} тем")

    # Временные метки
    if started_at:
        start_dt = time.strftime("%Y-%m-%d %H:%M", time.localtime(started_at))
        status_lines.append(f"📅 Начат: {start_dt}")
    if completed_at:
        complete_dt = time.strftime("%Y-%m-%d %H:%M", time.localtime(completed_at))
        status_lines.append(f"🎉 Завершён: {complete_dt}")

    # Таблица тем
    table = Table(show_header=True, header_style="bold yellow")
    table.add_column("#", justify="right", style="dim", width=3)
    table.add_column("Тема", style="white")
    table.add_column("Статус", justify="center", width=10)
    table.add_column("Лаба", style="cyan", width=15)
    table.add_column("Квиз", style="magenta", width=12)

    for i, topic in enumerate(track.topics, 1):
        status = "✅" if topic.topic_id in completed_topics else "⏳"
        if (
            not is_completed
            and i == current_idx + 1
            and topic.topic_id not in completed_topics
        ):
            status = "🟡"  # текущая
        lab = topic.lab_id or "-"
        quiz = topic.quiz_topic or "-"
        table.add_row(str(i), topic.title, status, lab, quiz)

    return (
        True,
        Panel(table, border_style="yellow", title=f"Темы ({total_required} всего)"),
        None,
    )


def cmd_track_next() -> tuple[bool, str, None]:
    """Получить следующую тему текущего трека или указанного трека"""
    state = get_context().state
    if not state.tracks_enrolled:
        return (
            False,
            "❌ Нет активных треков. Начни с `/tracks list` и `/tracks start <id>`",
            None,
        )

    # Если есть активный трек в контексте, используем его, иначе последний начатый
    current_track_id = state.learning_context.get("current_track")
    if not current_track_id or current_track_id not in state.tracks_enrolled:
        current_track_id = state.tracks_enrolled[-1]  # последний записанный

    engine = get_track_engine()
    track = engine.get_track(current_track_id)
    if not track:
        return False, f"❌ Трек '{current_track_id}' не найден.", None

    prog = state.track_progress.get(current_track_id, {})
    current_idx = prog.get("current_topic_idx", 0)
    completed = prog.get("completed_topics", [])

    next_topic = track.get_next_topic(completed, current_idx)

    if not next_topic:
        # Все темы пройдены?
        if track.is_completed(completed):
            # Помечаем как завершённый
            prog["completed_at"] = time.time()
            state.track_progress[current_track_id] = prog
            state.save_to_file()
            return (
                True,
                f"🎉 Трек '{track.name}' завершён! Все обязательные темы пройдены.",
                None,
            )
        else:
            return (
                True,
                "⚠️ Все темы обработаны, но не все обязательные пройдены. "
                f"Проверь прогресс: `/tracks progress {track.id}`",
                None,
            )

    # Обновляем текущий индекс
    prog["current_topic_idx"] = next_topic.order - 1  # order начинается с 1
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
4. Когда theme готова, отметь: `/tracks complete {next_topic.topic_id}`
"""
    # Установить текущий трек в контексте
    state.set_learning_context(action="track_next", course=current_track_id)
    return True, output, None


def cmd_track_complete_topic(topic_id: str) -> tuple[bool, str, None]:
    """Отметить тему как пройденную (вручную, после квиза или проверки)"""
    if not topic_id:
        return (
            False,
            "❌ Укажи ID темы. Использование: `/tracks complete <topic_id>`",
            None,
        )

    state = get_context().state
    if not state.tracks_enrolled:
        return False, "❌ Нет активных треков.", None

    # Найти, к какому треку принадлежит эта тема
    engine = get_track_engine()
    current_track_id = (
        state.learning_context.get("current_track") or state.tracks_enrolled[-1]
    )
    track = engine.get_track(current_track_id)
    if not track:
        return False, f"❌ Трек '{current_track_id}' не найден.", None

    topic = track.get_topic_by_id(topic_id)
    if not topic:
        return False, f"❌ Тема '{topic_id}' не найдена в треке '{track.name}'.", None

    prog = state.track_progress.get(
        current_track_id,
        {
            "current_topic_idx": 0,
            "completed_topics": [],
            "started_at": time.time(),
            "completed_at": None,
        },
    )

    if topic_id in prog["completed_topics"]:
        return True, f"✅ Тема '{topic.title}' уже отмечена как пройденная.", None

    # Добавляем тему в завершённые
    prog["completed_topics"].append(topic_id)

    # Проверить, не завершён ли трек
    if track.is_completed(prog["completed_topics"]):
        prog["completed_at"] = time.time()
        # Добавляем трек в completed если ещё не там
        if current_track_id not in state.tracks_enrolled:
            state.tracks_enrolled.append(current_track_id)
        # Начисляем бонусные очки за завершение трека
        bonus = 50 * track.estimated_hours
        state.points += bonus
        msg = f"🎉 Трек '{track.name}' завершён! +{bonus} очков."
    else:
        msg = f"✅ Тема '{topic.title}' отмечена как пройденная."

    state.track_progress[current_track_id] = prog
    state.save_to_file()

    return True, msg, None


def cmd_track_recommend() -> tuple[bool, str, None]:
    """Получить персональные рекомендации по трекам"""
    state = get_context().state
    engine = get_track_engine()

    weak_topics = state.get_weak_topics(threshold=70.0)
    completed_tracks = [t for t in state.tracks_enrolled if engine.get_track(t)]

    recommendations = engine.recommend_tracks(weak_topics, completed_tracks)

    if not recommendations:
        return (
            False,
            "❌ Нет доступных треков для рекомендаций. Возможно, все пройдены "
            "или prerequisites не выполнены.",
            None,
        )

    output = "🎯 **РЕКОМЕНДАЦИИ НА ОСНОВЕ ТВОИХ СЛАБЫХ ТЕМ:**\n\n"
    if weak_topics:
        output += "🔴 Слабые темы:\n"
        for wt in weak_topics[:5]:
            output += f"  • {wt['topic']} (успешность: {wt['success_rate']:.0f}%)\n"
        output += "\n"

    output += "📚 **Рекомендуемые треки:**\n\n"
    for i, (track, score) in enumerate(recommendations[:5], 1):
        marker = "🔥" if i == 1 else f"{i}."
        output += (
            f"{marker} **{track.name}** [{track.level}] - {track.description[:60]}...\n"
        )
        adapt = "✅" if track.adaptive else "❌"
        output += f"   Тем: {len(track.topics)} | Адаптивность: {adapt}\n"
        output += f"   Начать: `/tracks start {track.id}`\n\n"

    return True, output, None


def cmd_track_reset(track_id: str = "") -> tuple[bool, str, None]:
    """Сбросить прогресс трека (или всех треков)"""
    state = get_context().state
    if not track_id:
        # Сбросить все треки
        confirm = (
            "⚠️ Сбросить ВСЕ треки? Это удалит весь прогресс. "
            "Используй `/tracks reset <id>` для конкретного трека."
        )
        return False, confirm, None

    engine = get_track_engine()
    track = engine.get_track(track_id)
    if not track:
        return False, f"❌ Трек '{track_id}' не найден.", None

    if track_id in state.tracks_enrolled:
        state.tracks_enrolled.remove(track_id)
    if track_id in state.track_progress:
        del state.track_progress[track_id]
    state.save_to_file()
    return True, f"✅ Прогресс трека '{track.name}' сброшен.", None


def cmd_track_status() -> tuple[bool, str, None]:
    """Показать текущий активный трек"""
    state = get_context().state
    current = state.learning_context.get("current_track")

    if not current:
        if state.tracks_enrolled:
            current = state.tracks_enrolled[-1]
        else:
            return False, "❌ Нет активного трека. Начни с `/tracks start <id>`", None

    engine = get_track_engine()
    track = engine.get_track(current)
    if not track:
        return False, f"❌ Трек '{current}' не найден.", None

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
    return True, output, None
