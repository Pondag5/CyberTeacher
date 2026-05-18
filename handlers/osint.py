"""Модуль OSINT (Open Source Intelligence) — симуляция разведки по открытым источникам.

Команды:
    /osint search <username> — Поиск профиля по никнейму
    /osint email <email>     — Проверка email на утечки
    /osint phone <phone>     — Поиск по номеру телефона
    /osint metadata <file>   — Анализ метаданных файла
    /osint help              — Справка по командам OSINT
"""

import random
import re
from typing import Any, Dict, List, Optional, Tuple

from rich.panel import Panel
from rich.table import Table

from di import get_context
from ui import console


def _simulate_social_media(username: str) -> list[dict[str, str]]:
    """Симуляция поиска аккаунтов в социальных сетях."""
    platforms = [
        {"name": "GitHub", "url": f"https://github.com/{username}", "found": random.choice([True, True, False])},
        {"name": "Twitter/X", "url": f"https://twitter.com/{username}", "found": random.choice([True, False])},
        {"name": "Instagram", "url": f"https://instagram.com/{username}", "found": random.choice([True, False])},
        {"name": "LinkedIn", "url": f"https://linkedin.com/in/{username}", "found": random.choice([True, False])},
        {"name": "Reddit", "url": f"https://reddit.com/user/{username}", "found": random.choice([True, False])},
        {"name": "Telegram", "url": f"https://t.me/{username}", "found": random.choice([True, True, False])},
    ]
    return [p for p in platforms if p["found"]]


def _simulate_breaches(email: str) -> list[dict[str, str]]:
    """Симуляция проверки email по базам утечек."""
    breaches = [
        {"name": "Adobe (2013)", "data": "Email, Password (MD5), Hint"},
        {"name": "LinkedIn (2012)", "data": "Email, Password (SHA1)"},
        {"name": "Dropbox (2012)", "data": "Email, Password (bcrypt)"},
        {"name": "Collection #1 (2019)", "data": "Email, Password (Plaintext)"},
        {"name": "Canva (2019)", "data": "Email, Username, City"},
        {"name": "Verification.io (2019)", "data": "Email, Name, Phone, Gender"},
    ]
    # Случайное количество утечек (0-4)
    count = random.randint(0, 4)
    return random.sample(breaches, count)


def _simulate_phone_info(phone: str) -> dict[str, Any]:
    """Симуляция поиска информации по номеру телефона."""
    carriers = ["MTS", "Beeline", "Megafon", "Tele2", "Yota"]
    regions = ["Москва", "Санкт-Петербург", "Новосибирск", "Екатеринбург", "Казань"]
    return {
        "carrier": random.choice(carriers),
        "region": random.choice(regions),
        "timezone": f"UTC+{random.randint(2, 7)}",
        "valid": True,
        "type": "Mobile",
    }


def _simulate_metadata(filepath: str) -> dict[str, str]:
    """Симуляция извлечения метаданных из файла."""
    cameras = ["Canon EOS 5D Mark IV", "iPhone 13 Pro", "Samsung Galaxy S21", "Sony A7 III"]
    software = ["Adobe Photoshop 2024", "GIMP 2.10", "Microsoft Office 365", "Preview (macOS)"]
    return {
        "file_name": filepath,
        "file_size": f"{random.randint(100, 5000)} KB",
        "mime_type": random.choice(["image/jpeg", "application/pdf", "application/docx"]),
        "created": f"2024-{random.randint(1,12):02d}-{random.randint(1,28):02d} {random.randint(0,23):02d}:{random.randint(0,59):02d}:{random.randint(0,59):02d}",
        "modified": f"2025-{random.randint(1,12):02d}-{random.randint(1,28):02d} {random.randint(0,23):02d}:{random.randint(0,59):02d}:{random.randint(0,59):02d}",
        "camera": random.choice(cameras),
        "gps_lat": f"{random.uniform(40.0, 60.0):.6f}",
        "gps_lon": f"{random.uniform(30.0, 50.0):.6f}",
        "software": random.choice(software),
        "author": random.choice(["User", "Admin", "John Doe", ""]),
    }


def _display_osint_help() -> None:
    """Вывести справку по командам OSINT."""
    help_text = """[bold]Доступные команды OSINT:[/bold]

[green]/osint search <username>[/green]  — Поиск аккаунтов по никнейму
[green]/osint email <email>[/green]      — Проверка email на утечки
[green]/osint phone <phone>[/green]      — Информация по номеру телефона
[green]/osint metadata <file>[/green]    — Анализ метаданных файла

[bold]Примечание:[/bold] Это учебная симуляция. В реальном OSINT используются:
- Maltego, theHarvester, Sherlock
- HaveIBeenPwned API, Dehashed
- ExifTool, Metagoofil
- Google Dorks, Shodan, Censys"""

    console.print(Panel(help_text, title="OSINT HELP", border_style="yellow"))


def handle_osint_search(username: str) -> tuple[str, bool]:
    """Обработать команду поиска по никнейму."""
    if not username or len(username) < 3:
        console.print("[red]Ошибка:[/red] Никнейм должен содержать минимум 3 символа.")
        return "", True

    accounts = _simulate_social_media(username)

    table = Table(title=f"Результаты поиска: {username}")
    table.add_column("Платформа", style="cyan")
    table.add_column("URL", style="green")
    table.add_column("Статус", style="bold")

    for acc in accounts:
        table.add_row(acc["name"], acc["url"], "[green]Найден[/green]")

    if not accounts:
        table.add_row("—", "—", "[yellow]Ничего не найдено[/yellow]")

    console.print(table)

    # Образовательный блок
    console.print(Panel(
        "[bold]Совет по OSINT:[/bold] Используйте инструменты like [cyan]Sherlock[/cyan] или [cyan]Maigret[/cyan] "
        "для реального поиска по никнеймам. Они проверяют сотни сайтов одновременно.",
        border_style="blue",
    ))

    # Обновляем XP за OSINT активность
    state = get_context().state
    if hasattr(state, "xp"):
        state.xp += 10
    return "", True


def handle_osint_email(email: str) -> tuple[str, bool]:
    """Обработать команду проверки email."""
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        console.print("[red]Ошибка:[/red] Неверный формат email.")
        return "", True

    breaches = _simulate_breaches(email)

    table = Table(title=f"Утечки для: {email}")
    table.add_column("Название утечки", style="cyan")
    table.add_column("Скомпрометированные данные", style="yellow")

    if breaches:
        for b in breaches:
            table.add_row(b["name"], b["data"])
    else:
        table.add_row("—", "[green]Утечек не обнаружено[/green]")

    console.print(table)

    console.print(Panel(
        "[bold]Рекомендация:[/bold] Проверьте свой email на [cyan]haveibeenpwned.com[/cyan]. "
        "Используйте уникальные пароли для каждого сервиса и включите 2FA.",
        border_style="blue",
    ))

    state = get_context().state
    if hasattr(state, "xp"):
        state.xp += 15
    return "", True


def handle_osint_phone(phone: str) -> tuple[str, bool]:
    """Обработать команду поиска по телефону."""
    clean_phone = re.sub(r"[^\d+]", "", phone)
    if len(clean_phone) < 10:
        console.print("[red]Ошибка:[/red] Номер телефона слишком короткий.")
        return "", True

    info = _simulate_phone_info(clean_phone)

    panel_content = f"""[bold]Оператор:[/bold] {info['carrier']}
[bold]Регион:[/bold] {info['region']}
[bold]Часовой пояс:[/bold] {info['timezone']}
[bold]Тип:[/bold] {info['type']}
[bold]Валиден:[/bold] {'Да' if info['valid'] else 'Нет'}"""

    console.print(Panel(panel_content, title=f"Телефон: {clean_phone}", border_style="cyan"))

    console.print(Panel(
        "[bold]Для реального поиска:[/bold] Используйте [cyan]PhoneInfoga[/cyan] или API операторов. "
        "В некоторых странах доступны публичные реестры номеров.",
        border_style="blue",
    ))

    state = get_context().state
    if hasattr(state, "xp"):
        state.xp += 10
    return "", True


def handle_osint_metadata(filepath: str) -> tuple[str, bool]:
    """Обработать команду анализа метаданных."""
    if not filepath:
        console.print("[red]Ошибка:[/red] Укажите путь к файлу.")
        return "", True

    meta = _simulate_metadata(filepath)

    table = Table(title=f"Метаданные: {filepath}")
    table.add_column("Параметр", style="cyan")
    table.add_column("Значение", style="green")

    for key, value in meta.items():
        if value:
            table.add_row(key.replace("_", " ").title(), str(value))

    console.print(table)

    console.print(Panel(
        "[bold]Важно:[/bold] Метаданные могут раскрыть местоположение, устройство и автора. "
        "Используйте [cyan]ExifTool[/cyan] для просмотра и очистки метаданных перед публикацией файлов.",
        border_style="blue",
    ))

    state = get_context().state
    if hasattr(state, "xp"):
        state.xp += 15
    return "", True


def handle_osint(args: str) -> tuple[str, bool]:
    """Главный обработчик команды /osint."""
    parts = args.strip().split(maxsplit=1)
    if not parts:
        _display_osint_help()
        return "", True

    subcommand = parts[0].lower()
    query = parts[1] if len(parts) > 1 else ""

    if subcommand == "search":
        return handle_osint_search(query)
    elif subcommand == "email":
        return handle_osint_email(query)
    elif subcommand == "phone":
        return handle_osint_phone(query)
    elif subcommand == "metadata":
        return handle_osint_metadata(query)
    elif subcommand == "help":
        _display_osint_help()
        return "", True
    else:
        console.print(f"[red]Неизвестная подкоманда OSINT:[/red] {subcommand}")
        _display_osint_help()
        return "", True
