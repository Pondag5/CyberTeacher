"""Модуль Video/Podcasts Player — встроенный плеер для образовательного контента.

Команды:
    /media                 — Список ресурсов
    /media play <id>       — Воспроизвести (ссылка + конспект)
    /media notes <id>      — Показать конспект
    /media help            — Справка
"""

import random
from typing import Any, Dict, List, Tuple

from rich.panel import Panel
from rich.table import Table

from di import get_context
from ui import console
from handlers.types import HandlerResult


MEDIA_RESOURCES: dict[str, dict[str, Any]] = {
    "yt_sql_injection": {
        "title": "SQL Injection Explained",
        "type": "video",
        "url": "https://www.youtube.com/watch?v=ciNHNC38Ydg",
        "duration": "12:34",
        "topic": "Web Security",
        "summary": "Разбор SQL-инъекций: типы, примеры эксплуатации, методы защиты (подготовленные выражения).",
        "key_points": [
            "Union-based vs Error-based vs Blind SQLi",
            "Использование SQLMap для автоматизации",
            "Защита: параметризованные запросы",
        ],
        "xp": 15,
    },
    "podcast_darknet": {
        "title": "Darknet Diaries: Stuxnet",
        "type": "podcast",
        "url": "https://darknetdiaries.com/episode/1/",
        "duration": "58:20",
        "topic": "Malware",
        "summary": "История создания и применения Stuxnet — первого цифрового оружия.",
        "key_points": [
            "Целевая атака на ядерные объекты Ирана",
            "Использование 4 zero-day уязвимостей",
            "Влияние на кибервойны будущего",
        ],
        "xp": 20,
    },
    "yt_network_basics": {
        "title": "Networking for Hackers",
        "type": "video",
        "url": "https://www.youtube.com/watch?v=Vdq8XnVvMkE",
        "duration": "25:10",
        "topic": "Networking",
        "summary": "Основы сетей: TCP/IP, DNS, HTTP, сокеты — всё, что нужно хакеру.",
        "key_points": [
            "Модель OSI vs TCP/IP",
            "Анализ трафика с Wireshark",
            "DNS-туннелирование",
        ],
        "xp": 15,
    },
    "yt_crypto_101": {
        "title": "Cryptography 101",
        "type": "video",
        "url": "https://www.youtube.com/watch?v=6_CfjGBMB0k",
        "duration": "18:45",
        "topic": "Cryptography",
        "summary": "Введение в криптографию: симметричное/асимметричное шифрование, хэши, цифровые подписи.",
        "key_points": [
            "AES vs RSA",
            "SHA-256 и коллизии",
            "PKI и сертификаты",
        ],
        "xp": 15,
    },
}


def _display_media() -> None:
    """Вывести список ресурсов."""
    table = Table(title="🎬 Видео и подкасты")
    table.add_column("ID", style="cyan")
    table.add_column("Название", style="green")
    table.add_column("Тип", style="yellow")
    table.add_column("Тема", style="magenta")
    table.add_column("Длительность", style="blue")

    for mid, res in MEDIA_RESOURCES.items():
        table.add_row(mid, res["title"], res["type"], res["topic"], res["duration"])

    console.print(table)
    console.print("\n[dim]Используйте /media play <id> для просмотра.[/dim]")


def _play_resource(resource_id: str) -> bool:
    """Воспроизвести ресурс (показать ссылку и конспект)."""
    res = MEDIA_RESOURCES.get(resource_id)
    if not res:
        console.print(f"[red]Ресурс '{resource_id}' не найден.[/red]")
        return False

    console.print(Panel(
        f"[bold]Тип:[/bold] {res['type'].upper()}\n"
        f"[bold]Длительность:[/bold] {res['duration']}\n"
        f"[bold]Ссылка:[/bold] {res['url']}\n\n"
        f"[bold]Конспект:[/bold]\n{res['summary']}\n\n"
        f"[bold]Ключевые моменты:[/bold]\n" + "\n".join(f"  • {p}" for p in res["key_points"]),
        title=res["title"],
        border_style="cyan",
    ))

    ctx = get_context()
    state = ctx.state
    if hasattr(state, "xp"):
        state.xp += res["xp"]
        console.print(f"[green]+{res['xp']} XP за изучение материала![/green]")
    return True


def _show_notes(resource_id: str) -> bool:
    """Показать конспект ресурса."""
    res = MEDIA_RESOURCES.get(resource_id)
    if not res:
        console.print(f"[red]Ресурс '{resource_id}' не найден.[/red]")
        return False

    console.print(Panel(
        f"[bold]Тема:[/bold] {res['topic']}\n"
        f"[bold]Конспект:[/bold]\n{res['summary']}\n\n"
        f"[bold]Ключевые моменты:[/bold]\n" + "\n".join(f"  • {p}" for p in res["key_points"]),
        title=f"Конспект: {res['title']}",
        border_style="green",
    ))
    return True


def handle_media(args: str) -> HandlerResult:
    """Главный обработчик команды /media."""
    parts = args.strip().split(maxsplit=1)
    if not parts or parts[0] == "":
        _display_media()
        return True, None, None, True

    subcommand = parts[0].lower()
    query = parts[1] if len(parts) > 1 else ""

    if subcommand == "play" and query:
        success = _play_resource(query)
        return True, None, None, success
    elif subcommand == "notes" and query:
        success = _show_notes(query)
        return True, None, None, success
    elif subcommand == "help":
        console.print(Panel(
            "[bold]Команды медиа-плеера:[/bold]\n"
            "/media                 — Список ресурсов\n"
            "/media play <id>       — Открыть ресурс + конспект\n"
            "/media notes <id>      — Только конспект",
            border_style="yellow",
        ))
        return True, None, None, True
    else:
        console.print(f"[red]Неизвестная подкоманда: {subcommand}[/red]")
        _display_media()
        return True, None, None, True
