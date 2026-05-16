"""Модуль Cross-platform Sync — синхронизация прогресса между устройствами.

Команды:
    /sync export [file]  — Экспорт прогресса в JSON
    /sync import <file>  — Импорт прогресса из JSON
    /sync id             — Показать ID пользователя
    /sync help           — Справка
"""

import json
import os
import uuid
from datetime import datetime
from typing import Any, Dict, Tuple

from rich.panel import Panel

from state import get_state
from ui import console


def _generate_user_id() -> str:
    """Генерация уникального ID пользователя."""
    state = get_state()
    if not hasattr(state, "sync_id"):
        state.sync_id = str(uuid.uuid4())[:8]
    return state.sync_id


def _export_progress(filepath: str = None) -> bool:
    """Экспорт прогресса в JSON файл."""
    state = get_state()
    if not filepath:
        filepath = f"cyberteacher_sync_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    sync_data = {
        "sync_id": _generate_user_id(),
        "exported_at": datetime.now().isoformat(),
        "version": "1.0",
        "progress": {
            "xp": getattr(state, "xp", 0),
            "level": getattr(state, "level", 1),
            "completed_quizzes": getattr(state, "completed_quizzes", []),
            "completed_tasks": getattr(state, "completed_tasks", []),
            "weak_topics": getattr(state, "weak_topics", []),
            "achievements": getattr(state, "achievements", []),
            "skills": getattr(state, "skills", {}),
            "reputation": getattr(state, "reputation", 0),
        },
    }

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(sync_data, f, indent=2, ensure_ascii=False)
        console.print(Panel(
            f"[green]✅ Прогресс экспортирован в:[/green] {filepath}\n"
            f"[bold]Sync ID:[/bold] {sync_data['sync_id']}\n"
            f"[dim]Перенесите файл на другое устройство и используйте /sync import.[/dim]",
            border_style="green",
        ))
        return True
    except Exception as e:
        console.print(f"[red]Ошибка экспорта: {e}[/red]")
        return False


def _import_progress(filepath: str) -> bool:
    """Импорт прогресса из JSON файла."""
    if not os.path.exists(filepath):
        console.print(f"[red]Файл '{filepath}' не найден.[/red]")
        return False

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            sync_data = json.load(f)

        if "progress" not in sync_data:
            console.print("[red]Неверный формат файла синхронизации.[/red]")
            return False

        state = get_state()
        progress = sync_data["progress"]

        # Восстановление данных
        state.xp = progress.get("xp", 0)
        state.level = progress.get("level", 1)
        state.completed_quizzes = progress.get("completed_quizzes", [])
        state.completed_tasks = progress.get("completed_tasks", [])
        state.weak_topics = progress.get("weak_topics", [])
        state.achievements = progress.get("achievements", [])
        state.skills = progress.get("skills", {})
        state.reputation = progress.get("reputation", 0)

        console.print(Panel(
            f"[green]✅ Прогресс импортирован![/green]\n"
            f"[bold]XP:[/bold] {state.xp} | [bold]Уровень:[/bold] {state.level}\n"
            f"[bold]Достижений:[/bold] {len(state.achievements)} | [bold]Репутация:[/bold] {state.reputation}",
            border_style="green",
        ))
        return True
    except Exception as e:
        console.print(f"[red]Ошибка импорта: {e}[/red]")
        return False


def handle_sync(args: str) -> Tuple[str, bool]:
    """Главный обработчик команды /sync."""
    parts = args.strip().split(maxsplit=1)
    subcommand = parts[0].lower() if parts else ""
    query = parts[1] if len(parts) > 1 else ""

    if subcommand == "export":
        success = _export_progress(query if query else None)
        return "", success
    elif subcommand == "import" and query:
        success = _import_progress(query)
        return "", success
    elif subcommand == "id":
        user_id = _generate_user_id()
        console.print(Panel(
            f"[bold]Ваш Sync ID:[/bold] {user_id}\n"
            f"[dim]Используйте этот ID для идентификации при синхронизации.[/dim]",
            border_style="cyan",
        ))
        return "", True
    elif subcommand == "help":
        console.print(Panel(
            "[bold]Команды синхронизации:[/bold]\n"
            "/sync export [file]  — Экспорт прогресса в JSON\n"
            "/sync import <file>  — Импорт прогресса из JSON\n"
            "/sync id             — Показать ID пользователя\n\n"
            "[dim]Для синхронизации между устройствами перенесите файл\n"
            "через облако (Google Drive, Dropbox) или USB.[/dim]",
            border_style="yellow",
        ))
        return "", True
    else:
        console.print(f"[red]Неизвестная подкоманда: {subcommand}[/red]")
        return "", True
