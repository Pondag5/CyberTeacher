"""Модуль Time Loop / Alternate Realities — ветвящиеся сюжеты.

Команды:
    /timeloop              — Начать новую петлю
    /timeloop choice <num> — Сделать выбор
    /timeloop reset        — Сбросить петлю
    /timeloop help         — Справка
"""

import random
from typing import Any, Dict, List, Tuple

from rich.panel import Panel
from rich.table import Table

from di import get_context
from ui import console
from handlers.types import HandlerResult


STORY_NODES: dict[str, dict[str, Any]] = {
    "start": {
        "text": (
            "Вы — аналитик SOC. В 3:00 ночи срабатывает警报: подозрительная активность в сети.\n"
            "Сервер базы данных показывает аномальные запросы."
        ),
        "choices": {
            "1": {"text": "Проверить логи сервера", "next": "check_logs"},
            "2": {"text": "Изолировать сервер от сети", "next": "isolate_server"},
            "3": {"text": "Позвонить старшему аналитику", "next": "call_senior"},
        },
    },
    "check_logs": {
        "text": (
            "В логах вы видите множество запросов SELECT * FROM users.\n"
            "IP-адрес источника: 192.168.1.100 (внутренний)."
        ),
        "choices": {
            "1": {"text": "Заблокировать IP через фаервол", "next": "block_ip"},
            "2": {"text": "Проверить, какой пользователь за этим IP", "next": "check_user"},
        },
    },
    "isolate_server": {
        "text": (
            "Вы отключаете сервер от сети. Атака остановлена, но бизнес-процессы нарушены.\n"
            "Начальник требует объяснений."
        ),
        "choices": {
            "1": {"text": "Объяснить, что это была атака", "next": "explain_attack"},
            "2": {"text": "Сказать, что это была профилактика", "next": "fake_maintenance"},
        },
        "endings": ["good", "neutral"],
    },
    "call_senior": {
        "text": (
            "Старший аналитик говорит: 'Я видел такое раньше. Это может быть инсайдер.'\n"
            "Он советует проверить учетные записи с повышенными привилегиями."
        ),
        "choices": {
            "1": {"text": "Проверить AD на предмет изменений", "next": "check_ad"},
            "2": {"text": "Сканировать рабочие станции", "next": "scan_workstations"},
        },
    },
    "block_ip": {
        "text": "IP заблокирован. Но атака продолжается с другого адреса: 192.168.1.101.",
        "choices": {
            "1": {"text": "Заблокировать весь подсеть 192.168.1.0/24", "next": "block_subnet"},
            "2": {"text": "Искать паттерн в запросах", "next": "find_pattern"},
        },
    },
    "check_user": {
        "text": "За IP закреплен пользователь 'Иванов'. Его учетка имеет доступ к БД.",
        "choices": {
            "1": {"text": "Сбросить пароль Иванова", "next": "reset_password"},
            "2": {"text": "Проверить историю действий Иванова", "next": "check_history"},
        },
    },
    "explain_attack": {
        "text": "Начальник понимает ситуацию. Вы получаете благодарность за быструю реакцию.",
        "ending": "good",
        "xp": 50,
    },
    "fake_maintenance": {
        "text": "Начальник верит, но позже правда всплывает. Ваша репутация подорвана.",
        "ending": "bad",
        "xp": 10,
    },
    "check_ad": {
        "text": "Вы находите новую учетку с правами Domain Admin, созданную вчера.",
        "choices": {
            "1": {"text": "Удалить учетку и расследовать", "next": "remove_account"},
            "2": {"text": "Наблюдать за активностью", "next": "monitor_activity"},
        },
    },
    "scan_workstations": {
        "text": "На рабочей станции 12 найден необычный процесс, соединяющийся с внешним IP.",
        "choices": {
            "1": {"text": "Завершить процесс и изолировать станцию", "next": "isolate_workstation"},
            "2": {"text": "Сделать дамп памяти для анализа", "next": "memory_dump"},
        },
    },
    "block_subnet": {
        "text": "Подсеть заблокирована. Офис парализован. Это была слишком агрессивная мера.",
        "ending": "neutral",
        "xp": 20,
    },
    "find_pattern": {
        "text": "Вы обнаруживаете, что запросы идут через SQL-инъекцию в веб-приложении.",
        "choices": {
            "1": {"text": "Исправить код приложения", "next": "fix_app"},
            "2": {"text": "Временно отключить веб-приложение", "next": "disable_app"},
        },
    },
    "reset_password": {
        "text": "Пароль сброшен. Атака прекращена. Иванов утверждает, что его взломали.",
        "ending": "good",
        "xp": 40,
    },
    "check_history": {
        "text": "Иванов скачивал большие объемы данных за последний месяц. Похоже на инсайд.",
        "ending": "good",
        "xp": 45,
    },
    "remove_account": {
        "text": "Учетка удалена. Вы предотвратили эскалацию привилегий.",
        "ending": "good",
        "xp": 50,
    },
    "monitor_activity": {
        "text": "Вы наблюдаете, как учетка пытается получить доступ к финансовым данным.",
        "ending": "good",
        "xp": 55,
    },
    "isolate_workstation": {
        "text": "Станция изолирована. Вы нашли троян, который отправлял данные.",
        "ending": "good",
        "xp": 45,
    },
    "memory_dump": {
        "text": "Дамп сохранен. Позже анализ покажет, что это был RAT.",
        "ending": "good",
        "xp": 50,
    },
    "fix_app": {
        "text": "Вы добавляете параметризованные запросы. Уязвимость устранена.",
        "ending": "good",
        "xp": 60,
    },
    "disable_app": {
        "text": "Приложение отключено. Бизнес теряет деньги, но данные в безопасности.",
        "ending": "neutral",
        "xp": 30,
    },
}


def _display_node(node_id: str) -> None:
    """Отобразить текущий узел сюжета."""
    node = STORY_NODES.get(node_id)
    if not node:
        console.print("[red]Ошибка: узел сюжета не найден.[/red]")
        return

    console.print(Panel(node["text"], title="📖 Событие", border_style="cyan"))

    if "ending" in node:
        console.print(Panel(
            f"[bold]Концовка:[/bold] {node['ending'].upper()}\n"
            f"[bold]XP:[/bold] +{node.get('xp', 0)}",
            border_style="green" if node["ending"] == "good" else "red",
        ))
        state = get_context().state
        if hasattr(state, "xp"):
            state.xp += node.get("xp", 0)
        state.current_node = None
    elif "choices" in node:
        table = Table(title="Выбор")
        table.add_column("№", style="cyan")
        table.add_column("Действие", style="green")
        for num, choice in node["choices"].items():
            table.add_row(num, choice["text"])
        console.print(table)


def _start_timeloop() -> None:
    """Начать новую временную петлю."""
    console.print(Panel(
        "[bold]🔄 Временная петля запущена![/bold]\n"
        "Вы проживаете один и тот же день аналитика SOC.\n"
        "Каждое решение ведёт к разным последствиям.\n"
        "Попробуйте найти все концовки!",
        border_style="magenta",
    ))
    state = get_context().state
    state.current_node = "start"
    state.loop_count = getattr(state, "loop_count", 0) + 1
    _display_node("start")


def _make_choice(choice_num: str) -> None:
    """Сделать выбор в сюжете."""
    state = get_context().state
    current_node = getattr(state, "current_node", None)
    if not current_node:
        console.print("[yellow]Сначала начните петлю: /timeloop[/yellow]")
        return

    node = STORY_NODES.get(current_node)
    if not node or "choices" not in node:
        console.print("[yellow]Нет доступных выборов.[/yellow]")
        return

    choice = node["choices"].get(choice_num)
    if not choice:
        console.print(f"[red]Выбор {choice_num} недоступен.[/red]")
        return

    state.current_node = choice["next"]
    _display_node(choice["next"])


def _reset_timeloop() -> None:
    """Сбросить петлю."""
    state = get_context().state
    state.current_node = None
    console.print(Panel(
        "[bold]🔄 Петля сброшена.[/bold]\n"
        "Используйте /timeloop для начала новой истории.",
        border_style="yellow",
    ))


def handle_timeloop(args: str) -> HandlerResult:
    """Главный обработчик команды /timeloop."""
    parts = args.strip().split(maxsplit=1)
    subcommand = parts[0].lower() if parts else ""
    query = parts[1] if len(parts) > 1 else ""

    if subcommand == "" or subcommand == "start":
        _start_timeloop()
        return True, None, None, True
    elif subcommand == "choice" and query:
        _make_choice(query)
        return True, None, None, True
    elif subcommand == "reset":
        _reset_timeloop()
        return True, None, None, True
    elif subcommand == "help":
        console.print(Panel(
            "[bold]Команды временной петли:[/bold]\n"
            "/timeloop              — Начать новую петлю\n"
            "/timeloop choice <num> — Сделать выбор\n"
            "/timeloop reset        — Сбросить петлю",
            border_style="yellow",
        ))
        return True, None, None, True
    else:
        console.print(f"[red]Неизвестная подкоманда: {subcommand}[/red]")
        return True, None, None, True
