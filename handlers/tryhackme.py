"""
🎯 TryHackMe API интеграция (G-01)

Команды:
- /thm login <api_key> — авторизация
- /thm rooms [type] — список комнат
- /thm room <id> — детали комнаты
- /thm submit <room_id> <task> <answer> — отправка ответа
- /thm status — статус пользователя
- /thm sync — синхронизация прогресса
"""

import json
import os
import re
from typing import Any

import requests
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from di import get_context
from state import get_state
from handlers.types import HandlerResult


console = Console()

THM_API_BASE = "https://tryhackme.com/api"
THM_KEY_FILE = os.path.join(
    os.path.dirname(__file__), "..", "memory", "thm_api_key.json"
)


def _load_thm_key() -> str | None:
    """Загрузить API ключ TryHackMe."""
    if os.path.exists(THM_KEY_FILE):
        with open(THM_KEY_FILE, "r", encoding="utf-8") as f:
            data: dict[str, Any] = json.load(f)
            return data.get("api_key")
    return None


def _save_thm_key(api_key: str) -> None:
    """Сохранить API ключ."""
    os.makedirs(os.path.dirname(THM_KEY_FILE), exist_ok=True)
    with open(THM_KEY_FILE, "w", encoding="utf-8") as f:
        json.dump({"api_key": api_key}, f)


def _thm_request(endpoint: str, params: dict | None = None) -> dict[str, Any] | None:
    """Выполнить запрос к TryHackMe API."""
    api_key = _load_thm_key()
    if not api_key:
        return None

    try:
        headers = {"Accept": "application/json"}
        url = f"{THM_API_BASE}{endpoint}"
        if params:
            # THM API использует ключ в query params
            params["api_key"] = api_key

        response = requests.get(url, headers=headers, params=params, timeout=30)
        if response.status_code == 200:
            data: dict[str, Any] = response.json()
            return data
    except Exception:
        pass

    return None


def handle_thm_login(api_key: str) -> HandlerResult:
    """Авторизация в TryHackMe."""
    _save_thm_key(api_key)

    # Проверяем ключ
    data = _thm_request("/v2/user/info")
    if data and data.get("success"):
        user = data.get("data", {})
        username = user.get("username", "Unknown")
        console.print(
            Panel(
                f"✅ Авторизация успешна!\n\n"
                f"👤 Username: {username}\n"
                f"🏆 Rank: {user.get('publicProfile', {}).get('rank', 'N/A')}\n"
                f"⭐ Level: {user.get('publicProfile', {}).get('level', 'N/A')}\n"
                f"🔥 Streak: {user.get('publicProfile', {}).get('streak', 0)} дней",
                title="TryHackMe Login",
                border_style="green",
            )
        )
    else:
        console.print(
            "[yellow]⚠️ Ключ сохранён, но не удалось проверить. Проверьте API ключ.[/yellow]"
        )

    return True, None, None, True


def handle_thm_rooms(
    room_type: str = "all",
) -> HandlerResult:
    """Получить список комнат."""
    state = get_state()

    # Используем кэш если есть
    cache = getattr(state, "thm_rooms_cache", {})
    if cache.get("rooms") and cache.get("timestamp", 0) > 0:
        import time

        if time.time() - cache["timestamp"] < 3600:  # 1 час
            _display_rooms(cache["rooms"], room_type)
            return True, None, None, True

    # Запрос к API
    data = _thm_request("/v2/rooms")
    if not data or not data.get("success"):
        console.print(
            "[red]Не удалось получить список комнат. Проверьте API ключ.[/red]"
        )
        return True, None, None, True

    rooms = data.get("data", [])

    # Кэшируем
    import time

    state.thm_rooms_cache = {"rooms": rooms, "timestamp": time.time()}

    _display_rooms(rooms, room_type)
    return True, None, None, True


def _display_rooms(rooms: list[dict[str, Any]], room_type: str = "all") -> None:
    """Отобразить список комнат."""
    if not rooms:
        console.print("[yellow]Комнаты не найдены.[/yellow]")
        return

    # Фильтрация
    if room_type != "all":
        rooms = [r for r in rooms if r.get("type", "").lower() == room_type.lower()]

    table = Table(title=f"TryHackMe Rooms ({len(rooms)})")
    table.add_column("ID", style="cyan")
    table.add_column("Name")
    table.add_column("Type")
    table.add_column("Difficulty", justify="center")
    table.add_column("Users", justify="right")

    for room in rooms[:50]:
        diff = room.get("difficulty", "N/A")
        diff_style = {
            "Easy": "green",
            "Medium": "yellow",
            "Hard": "red",
        }.get(str(diff), "white")

        table.add_row(
            str(room.get("id", "")),
            room.get("title", "")[:40],
            room.get("type", ""),
            f"[{diff_style}]{diff}[/{diff_style}]",
            str(room.get("user_count", "")),
        )

    console.print(table)

    if len(rooms) > 50:
        console.print(
            f"[dim]...и ещё {len(rooms) - 50} комнат. Используйте /thm room <id> для деталей.[/dim]"
        )


def handle_thm_room(room_id: str) -> HandlerResult:
    """Получить детали комнаты."""
    data = _thm_request(f"/v2/rooms/{room_id}")
    if not data or not data.get("success"):
        console.print(f"[red]Комната {room_id} не найдена.[/red]")
        return True, None, None, True

    room = data.get("data", {})

    console.print(
        Panel(
            f"[bold]{room.get('title', '')}[/bold]\n\n"
            f"📝 Type: {room.get('type', 'N/A')}\n"
            f"📊 Difficulty: {room.get('difficulty', 'N/A')}\n"
            f"👥 Users: {room.get('user_count', 'N/A')}\n"
            f"⭐ Rating: {room.get('rating', 'N/A')}/5\n\n"
            f"[bold]Description:[/bold]\n{room.get('description', 'N/A')[:500]}",
            title=f"Room #{room_id}",
            border_style="cyan",
        )
    )

    # Задачи
    tasks = room.get("tasks", [])
    if tasks:
        console.print(f"[bold]Tasks ({len(tasks)}):[/bold]")
        for i, task in enumerate(tasks[:10], 1):
            console.print(f"  {i}. {task.get('title', 'Untitled')}")
        if len(tasks) > 10:
            console.print(f"  [dim]...и ещё {len(tasks) - 10} задач[/dim]")

    return True, None, None, True


def handle_thm_submit(room_id: str, task_id: str, answer: str) -> HandlerResult:
    """Отправить ответ на задачу."""
    api_key = _load_thm_key()
    if not api_key:
        console.print("[red]Сначала авторизуйтесь: /thm login <api_key>[/red]")
        return True, None, None, True

    try:
        url = f"{THM_API_BASE}/v2/rooms/{room_id}/tasks/{task_id}/check"
        response = requests.post(
            url,
            headers={"Accept": "application/json"},
            json={"answer": answer, "api_key": api_key},
            timeout=30,
        )

        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                console.print("[green]✅ Правильно! +XP[/green]")
                # Сохраняем прогресс
                state = get_state()
                if not hasattr(state, "thm_completed"):
                    state.thm_completed = []
                state.thm_completed.append({"room": room_id, "task": task_id})
            else:
                console.print("[red]❌ Неправильно. Попробуйте ещё раз.[/red]")
        else:
            console.print(f"[red]Ошибка API: {response.status_code}[/red]")
    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")

    return True, None, None, True


def handle_thm_status() -> HandlerResult:
    """Показать статус пользователя."""
    data = _thm_request("/v2/user/info")
    if not data or not data.get("success"):
        console.print("[red]Не удалось получить статус. Проверьте API ключ.[/red]")
        return True, None, None, True

    user = data.get("data", {})
    profile = user.get("publicProfile", {})

    console.print(
        Panel(
            f"👤 Username: {user.get('username', 'N/A')}\n"
            f"🏆 Rank: {profile.get('rank', 'N/A')}\n"
            f"⭐ Level: {profile.get('level', 'N/A')}\n"
            f"🔥 Streak: {profile.get('streak', 0)} дней\n"
            f"📊 Points: {profile.get('points', 0)}\n"
            f"🏅 Badges: {len(profile.get('badges', []))}\n"
            f"📚 Rooms Completed: {profile.get('completedRooms', 0)}",
            title="TryHackMe Status",
            border_style="green",
        )
    )

    return True, None, None, True


def handle_thm_sync() -> HandlerResult:
    """Синхронизировать прогресс с TryHackMe."""
    state = get_state()
    data = _thm_request("/v2/user/info")

    if not data or not data.get("success"):
        console.print("[red]Не удалось синхронизировать.[/red]")
        return True, None, None, True

    user = data.get("data", {})
    profile = user.get("publicProfile", {})

    # Сохраняем прогресс
    state.thm_username = user.get("username")
    state.thm_points = profile.get("points", 0)
    state.thm_level = profile.get("level", 0)
    state.thm_rank = profile.get("rank", "")
    state.save_to_file()

    console.print("[green]✅ Прогресс синхронизирован![/green]")
    console.print(f"  Points: {state.thm_points}")
    console.print(f"  Level: {state.thm_level}")
    console.print(f"  Rank: {state.thm_rank}")

    return True, None, None, True


def handle_thm_action(action: str) -> HandlerResult:
    """Обработка /thm <subcommand>."""
    parts = action.split()

    if len(parts) < 2:
        console.print("[cyan]Использование:[/cyan]")
        console.print("  /thm login <api_key>              — авторизация")
        console.print("  /thm rooms [all|free|pro]         — список комнат")
        console.print("  /thm room <id>                    — детали комнаты")
        console.print("  /thm submit <room> <task> <answer> — отправка ответа")
        console.print("  /thm status                       — статус пользователя")
        console.print("  /thm sync                         — синхронизация")
        console.print("\n[dim]Получите API ключ: https://tryhackme.com/settings[/dim]")
        return True, None, None, True

    subcmd = parts[1]

    if subcmd == "login" and len(parts) >= 3:
        return handle_thm_login(parts[2])
    elif subcmd == "rooms":
        room_type = parts[2] if len(parts) > 2 else "all"
        return handle_thm_rooms(room_type)
    elif subcmd == "room" and len(parts) >= 3:
        return handle_thm_room(parts[2])
    elif subcmd == "submit" and len(parts) >= 5:
        return handle_thm_submit(parts[2], parts[3], parts[4])
    elif subcmd == "status":
        return handle_thm_status()
    elif subcmd == "sync":
        return handle_thm_sync()
    else:
        console.print(f"[red]Неизвестная подкоманда: {subcmd}[/red]")
        return True, None, None, True
