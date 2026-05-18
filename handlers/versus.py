"""Модуль LLM-Соперник (/versus) — режим дуэли с LLM.

LLM играет за сервер/атакующего, пользователь за противоположную сторону.
Поддерживает несколько сценариев дуэли.
"""

from typing import Any

from rich.panel import Panel

from di import get_context
from ui import console

# Сценарии дуэли
VERSUS_SCENARIOS = {
    "web": {
        "name": "Веб-дуэль",
        "description": "Ты атакующий, LLM — веб-сервер с уязвимостями",
        "system_prompt": (
            "Ты веб-сервер с уязвимостями (SQLi, XSS, CSRF). "
            "Пользователь — атакующий, который пытается тебя взломать. "
            "Отвечай как сервер: показывай HTML-ответы, ошибки, результаты запросов. "
            "Если атака успешна — покажи флаг FLAG{...}. "
            "Если атака не удалась — покажи ошибку или нормальный ответ. "
            "Будь реалистичным: не сдавайся сразу, но и не будь непобедимым. "
            "После 3-5 попыток дай подсказку если пользователь застрял."
        ),
        "initial_message": (
            "🌐 Веб-сервер запущен на http://target.local:8080\n"
            "Технологии: PHP 7.4, MySQL 5.7, Apache 2.4\n"
            "Цель: найди уязвимость и получи FLAG{...}\n\n"
            "Введи свой первый запрос (например: GET /login)"
        )
    },
    "network": {
        "name": "Сетевая дуэль",
        "description": "Ты пентестер, LLM — сетевая инфраструктура",
        "system_prompt": (
            "Ты сетевая инфраструктура компании (Linux серверы, Windows домен, файрвол). "
            "Пользователь — пентестер, который сканирует и атакует сеть. "
            "Отвечай как nmap/sshd/smb/ftp: показывай открытые порты, баннеры, ошибки. "
            "Если атака успешна — покажи FLAG{...}. "
            "Будь реалистичным: не все порты открыты, есть файрвол. "
            "После 3-5 попыток дай подсказку."
        ),
        "initial_message": (
            "️ Сетевая инфраструктура: 192.168.1.0/24\n"
            "Известные хосты: 192.168.1.1 (роутер), 192.168.1.10 (сервер)\n"
            "Цель: получи доступ к серверу и найди FLAG{...}\n\n"
            "Введи свою первую команду (например: nmap 192.168.1.10)"
        )
    },
    "crypto": {
        "name": "Крипто-дуэль",
        "description": "Ты криптоаналитик, LLM — зашифрованное сообщение",
        "system_prompt": (
            "Ты система шифрования. Пользователь — криптоаналитик. "
            "Показывай зашифрованные данные, подсказки о типе шифрования. "
            "Если пользователь правильно расшифрует — покажи FLAG{...}. "
            "Используй реальные алгоритмы: Caesar, Vigenere, Base64, XOR, RSA. "
            "Давай подсказки после 3 неудачных попыток."
        ),
        "initial_message": (
            "🔐 Зашифрованное сообщение обнаружено!\n"
            "Тип шифрования: неизвестен\n"
            "Цель: расшифруй сообщение и найди FLAG{...}\n\n"
            "Зашифрованные данные: SGVsbG8gV29ybGQh\n\n"
            "Введи свою попытку расшифровки"
        )
    },
    "forensics": {
        "name": "Форензика-дуэль",
        "description": "Ты следователь, LLM — артефакты инцидента",
        "system_prompt": (
            "Ты система, показывающая артефакты киберинцидента (логи, дампы, файлы). "
            "Пользователь — следователь, который анализирует улики. "
            "Показывай логи, hex-дампы, метаданные файлов. "
            "Если пользователь найдёт ключевую улику — покажи FLAG{...}. "
            "Давай подсказки после 3 неудачных попыток."
        ),
        "initial_message": (
            "🔍 Инцидент: утечка данных из корпоративной сети\n"
            "Доступные артефакты: логи веб-сервера, дамп памяти, pcap файл\n"
            "Цель: определи вектор атаки и найди FLAG{...}\n\n"
            "Введи команду для анализа (например: cat /var/log/apache2/access.log)"
        )
    }
}


def handle_versus(args: str) -> tuple[bool, Any | None, Any | None, bool]:
    """Главный обработчик команды /versus."""
    ctx = get_context()
    state = ctx.state
    parts = args.strip().split(maxsplit=1)
    subcommand = parts[0].lower() if parts else ""

    if subcommand == "" or subcommand == "help":
        _show_versus_help()
        return True, None, None, True

    if subcommand == "list":
        _show_versus_list()
        return True, None, None, True

    if subcommand == "start":
        if len(parts) < 2:
            console.print("[yellow]Использование: /versus start <сценарий>[/yellow]")
            console.print("[dim]Доступные: web, network, crypto, forensics[/dim]")
            return True, None, None, True
        
        scenario_id = parts[1].lower().strip()
        if scenario_id not in VERSUS_SCENARIOS:
            console.print(f"[red]❌ Сценарий '{scenario_id}' не найден.[/red]")
            console.print("[dim]Доступные: web, network, crypto, forensics[/dim]")
            return True, None, None, True
        
        _start_versus(scenario_id)
        return True, None, None, True

    if subcommand == "stop":
        state.versus_active = False
        state.versus_scenario = None
        state.versus_attempts = 0
        console.print("[green]✅ Дуэль завершена.[/green]")
        return True, None, None, True

    if subcommand == "status":
        _show_versus_status()
        return True, None, None, True

    console.print(f"[red]Неизвестная подкоманда: {subcommand}[/red]")
    return True, None, None, True


def _show_versus_help():
    """Показать справку по /versus."""
    console.print(Panel(
        "[bold]🥊 LLM-Соперник (/versus)[/bold]\n\n"
        "Режим дуэли: ты против LLM в кибербезопасности!\n\n"
        "[bold]Команды:[/bold]\n"
        "/versus list     — Список сценариев\n"
        "/versus start <id> — Начать дуэль\n"
        "/versus stop     — Завершить дуэль\n"
        "/versus status   — Текущий статус\n"
        "/versus help     — Эта справка\n\n"
        "[dim]Во время дуэли просто пиши команды/запросы.[/dim]",
        border_style="magenta",
    ))


def _show_versus_list():
    """Показать список сценариев."""
    lines = []
    for sid, scenario in VERSUS_SCENARIOS.items():
        marker = " ← текущий" if getattr(get_context().state, "versus_scenario", None) == sid else ""
        lines.append(f"  [cyan]{sid:<12}[/cyan] — {scenario['name']}{marker}")
        lines.append(f"     [dim]{scenario['description']}[/dim]")
    
    console.print(Panel(
        "\n".join(lines),
        title="🥊 СЦЕНАРИИ ДУЭЛИ",
        border_style="magenta",
    ))


def _start_versus(scenario_id: str):
    """Начать дуэль."""
    ctx = get_context()
    state = ctx.state
    scenario = VERSUS_SCENARIOS[scenario_id]
    
    state.versus_active = True
    state.versus_scenario = scenario_id
    state.versus_attempts = 0
    ctx.save_state()
    
    console.print(Panel(
        f"[bold]{scenario['name']}[/bold]\n\n"
        f"{scenario['initial_message']}\n\n"
        "[dim]Пиши команды/запросы. /versus stop для выхода.[/dim]",
        title="🥊 ДУЭЛЬ НАЧАТА",
        border_style="magenta",
    ))


def _show_versus_status():
    """Показать статус дуэли."""
    ctx = get_context()
    state = ctx.state
    
    if not getattr(state, "versus_active", False):
        console.print("[yellow]Дуэль не активна. Используй /versus start <сценарий>[/yellow]")
        return
    
    scenario_id = getattr(state, "versus_scenario", "unknown")
    scenario = VERSUS_SCENARIOS.get(scenario_id, {})
    attempts = getattr(state, "versus_attempts", 0)
    
    console.print(Panel(
        f"[bold]Сценарий:[/bold] {scenario.get('name', scenario_id)}\n"
        f"[bold]Попыток:[/bold] {attempts}\n"
        f"[bold]Статус:[/bold] {'Активна' if state.versus_active else 'Завершена'}\n\n"
        "[dim]/versus stop для завершения[/dim]",
        title="🥊 СТАТУС ДУЭЛИ",
        border_style="magenta",
    ))


def get_versus_system_prompt() -> str | None:
    """Получить системный промпт для активной дуэли."""
    ctx = get_context()
    state = ctx.state
    
    if not getattr(state, "versus_active", False):
        return None
    
    scenario_id = getattr(state, "versus_scenario", None)
    if not scenario_id or scenario_id not in VERSUS_SCENARIOS:
        return None
    
    return VERSUS_SCENARIOS[scenario_id]["system_prompt"]


def increment_versus_attempts():
    """Увеличить счётчик попыток дуэли."""
    ctx = get_context()
    state = ctx.state
    
    if getattr(state, "versus_active", False):
        state.versus_attempts = getattr(state, "versus_attempts", 0) + 1
        ctx.save_state()
