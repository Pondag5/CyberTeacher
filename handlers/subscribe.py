"""Модуль подписки на уведомления об угрозах (L-13).

Команды:
    /subscribe add <type>   — Подписаться на тип угроз
    /subscribe remove <type>— Отписаться
    /subscribe list         — Список подписок
    /subscribe notify       — Проверить уведомления
    /subscribe help         — Справка
"""

import json
import os
import random
from datetime import datetime
from typing import Any, Dict, List, Tuple

from rich.panel import Panel
from rich.table import Table

from state import get_state
from ui import console

SUBSCRIPTIONS_FILE = os.path.join(os.path.dirname(__file__), "memory", "subscriptions.json")

THREAT_TYPES: Dict[str, str] = {
    "apt": "APT-группы и целевые атаки",
    "ransomware": "Ransomware и шифровальщики",
    "ddos": "DDoS-атаки",
    "vulnerability": "Критические уязвимости (CVE)",
    "malware": "Новые семейства вредоносов",
    "phishing": "Фишинговые кампании",
    "iot": "Угрозы для IoT устройств",
    "cloud": "Облачные инциденты",
}

RECENT_THREATS: Dict[str, List[Dict[str, str]]] = {
    "apt": [
        {"name": "APT41", "detail": "Новая кампания против телекома в Юго-Восточной Азии", "severity": "High"},
        {"name": "Lazarus", "detail": "Атака на криптовалютные биржи через supply chain", "severity": "Critical"},
    ],
    "ransomware": [
        {"name": "BlackCat", "detail": "Обновлённый шифратор, обход EDR", "severity": "Critical"},
        {"name": "LockBit 4.0", "detail": "Новая версия с улучшенным распространением", "severity": "High"},
    ],
    "vulnerability": [
        {"name": "CVE-2024-21762", "detail": "FortiOS out-of-bounds write, RCE", "severity": "Critical"},
        {"name": "CVE-2024-1709", "detail": "ConnectWise ScreenConnect Auth Bypass", "severity": "High"},
    ],
    "malware": [
        {"name": "Lumma Stealer", "detail": "Новый стилер данных через фишинг", "severity": "Medium"},
        {"name": "Rhysida", "detail": "Новый ransomware с двойным шантажом", "severity": "High"},
    ],
}


def _load_subscriptions() -> Dict[str, Any]:
    """Загрузить подписки."""
    if os.path.exists(SUBSCRIPTIONS_FILE):
        with open(SUBSCRIPTIONS_FILE, "r") as f:
            return json.load(f)
    return {"types": [], "notifications": [], "last_check": None}


def _save_subscriptions(data: Dict[str, Any]) -> None:
    """Сохранить подписки."""
    os.makedirs(os.path.dirname(SUBSCRIPTIONS_FILE), exist_ok=True)
    with open(SUBSCRIPTIONS_FILE, "w") as f:
        json.dump(data, f, indent=2)


def _add_subscription(threat_type: str) -> bool:
    """Подписаться на тип угроз."""
    if threat_type not in THREAT_TYPES:
        console.print(f"[red]Тип '{threat_type}' не найден.[/red]")
        console.print(f"[yellow]Доступные: {', '.join(THREAT_TYPES.keys())}[/yellow]")
        return False

    data = _load_subscriptions()
    if threat_type in data["types"]:
        console.print(f"[yellow]Вы уже подписаны на '{threat_type}'.[/yellow]")
        return True

    data["types"].append(threat_type)
    _save_subscriptions(data)
    console.print(f"[green]✅ Подписка на '{threat_type}' добавлена.[/green]")
    return True


def _remove_subscription(threat_type: str) -> bool:
    """Отписаться от типа угроз."""
    data = _load_subscriptions()
    if threat_type not in data["types"]:
        console.print(f"[yellow]Подписка на '{threat_type}' не найдена.[/yellow]")
        return False

    data["types"].remove(threat_type)
    _save_subscriptions(data)
    console.print(f"[green]✅ Подписка на '{threat_type}' удалена.[/green]")
    return True


def _list_subscriptions() -> None:
    """Список подписок."""
    data = _load_subscriptions()
    if not data["types"]:
        console.print("[yellow]Нет активных подписок.[/yellow]")
        return

    table = Table(title="🔔 Подписки на угрозы")
    table.add_column("Тип", style="cyan")
    table.add_column("Описание", style="green")
    for t in data["types"]:
        table.add_row(t, THREAT_TYPES.get(t, ""))
    console.print(table)


def _check_notifications() -> None:
    """Проверить новые уведомления."""
    data = _load_subscriptions()
    if not data["types"]:
        console.print("[yellow]Нет подписок. Используйте /subscribe add <type>.[/yellow]")
        return

    console.print("[bold cyan]🔔 Новые уведомления:[/bold cyan]")

    for threat_type in data["types"]:
        threats = RECENT_THREATS.get(threat_type, [])
        if threats:
            console.print(f"\n[bold]{threat_type.upper()}:[/bold]")
            for t in threats:
                severity_color = "red" if t["severity"] == "Critical" else "yellow"
                console.print(f"  [{severity_color}]⚠️ {t['name']}[/][dim] — {t['detail']}[/dim]")

    data["last_check"] = datetime.now().isoformat()
    _save_subscriptions(data)


def handle_subscribe(args: str) -> Tuple[str, bool]:
    """Главный обработчик команды /subscribe."""
    parts = args.strip().split(maxsplit=1)
    subcommand = parts[0].lower() if parts else ""
    query = parts[1] if len(parts) > 1 else ""

    if subcommand == "add" and query:
        success = _add_subscription(query)
        return "", success
    elif subcommand == "remove" and query:
        success = _remove_subscription(query)
        return "", success
    elif subcommand == "list":
        _list_subscriptions()
        return "", True
    elif subcommand == "notify":
        _check_notifications()
        return "", True
    elif subcommand == "help":
        types_list = "\n".join(f"  • {k} — {v}" for k, v in THREAT_TYPES.items())
        console.print(Panel(
            f"[bold]Подписки на угрозы:[/bold]\n"
            "/subscribe add <type>   — Подписаться\n"
            "/subscribe remove <type>— Отписаться\n"
            "/subscribe list         — Список подписок\n"
            "/subscribe notify       — Проверить уведомления\n\n"
            f"[bold]Доступные типы:[/bold]\n{types_list}",
            border_style="yellow",
        ))
        return "", True
    else:
        console.print(f"[red]Неизвестная подкоманда: {subcommand}[/red]")
        return "", True
