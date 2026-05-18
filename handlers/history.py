"""Модуль Historical Mode — курс "Эволюция взлома" от 80-х до 2020-х.

Команды:
    /timeline              — Показать хронологию эпох
    /timeline era <name>   — Детали конкретной эпохи
    /timeline quiz         — Викторина по истории кибербезопасности
"""

import random
from typing import Any, Dict, List, Tuple

from rich.panel import Panel
from rich.table import Table

from di import get_context
from ui import console

ERAS: list[dict[str, Any]] = [
    {
        "name": "1980-е: Зарождение",
        "period": "1980-1989",
        "description": "Появление первых компьютерных вирусов и хакерской культуры.",
        "events": [
            {"year": 1983, "event": "Термин 'computer virus' впервые использован Фредом Коэном"},
            {"year": 1986, "event": "Вирус Brain — первый IBM PC вирус (Пакистан)"},
            {"year": 1988, "event": "Червь Морриса — первая крупная сетевая атака"},
        ],
        "tools": ["DEBUG.COM", "Assembly", "BBS"],
        "vulnerabilities": ["Переполнение буфера", "Социальная инженерия по телефону"],
        "xp": 20,
    },
    {
        "name": "1990-е: Интернет-революция",
        "period": "1990-1999",
        "description": "Рост интернета, появление веб-уязвимостей и антивирусов.",
        "events": [
            {"year": 1990, "event": "Первая коммерческая антивирусная компания (McAfee)"},
            {"year": 1995, "event": "Появление SSL 1.0 (Netscape)"},
            {"year": 1998, "event": "Back Orifice — удалённый доступ к Windows"},
            {"year": 1999, "event": "Вирус Melissa — массовая рассылка через email"},
        ],
        "tools": ["Nmap", "L0phtCrack", "Netcat", "CGI Scanner"],
        "vulnerabilities": ["SQL Injection", "XSS", "Buffer Overflow в IIS"],
        "xp": 25,
    },
    {
        "name": "2000-е: Эпоха ботнетов",
        "period": "2000-2009",
        "description": "Коммерциализация киберпреступности, ботнеты, целевые атаки.",
        "events": [
            {"year": 2000, "event": "DDoS атака на Yahoo, Amazon, eBay"},
            {"year": 2003, "event": "Червь Blaster и Sobig.F"},
            {"year": 2005, "event": "Появление Zeus Trojan (банкинг)"},
            {"year": 2007, "event": "Атаки на Эстонию (кибервойна)"},
            {"year": 2008, "event": "Stuxnet (разработка началась)"},
        ],
        "tools": ["Metasploit", "Wireshark", "Burp Suite", "Hydra"],
        "vulnerabilities": ["Remote Code Execution", "Privilege Escalation", "Zero-day в IE"],
        "xp": 30,
    },
    {
        "name": "2010-е: APT и кибервойны",
        "period": "2010-2019",
        "description": "Государственные хакеры, утечки данных, ransomware.",
        "events": [
            {"year": 2010, "event": "Stuxnet — атака на ядерные объекты Ирана"},
            {"year": 2013, "event": "Snowden leaks (NSA)"},
            {"year": 2014, "event": "Heartbleed (OpenSSL)"},
            {"year": 2017, "event": "WannaCry и NotPetya (глобальные ransomware)"},
            {"year": 2018, "event": "GDPR вступил в силу"},
        ],
        "tools": ["Cobalt Strike", "Mimikatz", "Empire", "BloodHound"],
        "vulnerabilities": ["EternalBlue", "Spectre/Meltdown", "Supply Chain Attacks"],
        "xp": 35,
    },
    {
        "name": "2020-е: AI и облачные угрозы",
        "period": "2020-настоящее время",
        "description": "Использование ИИ в атаках, облачные уязвимости, квантовые риски.",
        "events": [
            {"year": 2020, "event": "SolarWinds — поставка цепочки атак"},
            {"year": 2021, "event": "Log4Shell (Log4j RCE)"},
            {"year": 2022, "event": "Кибератаки на Украину (инфраструктура)"},
            {"year": 2023, "event": "AI-generated phishing и deepfakes"},
            {"year": 2024, "event": "MOVEit Transfer и облачные утечки"},
        ],
        "tools": ["LLM-фреймворки", "Cloud Pentest Tools", "AI Red Team"],
        "vulnerabilities": ["Prompt Injection", "Cloud Misconfigurations", "AI Model Theft"],
        "xp": 40,
    },
]

QUIZ_QUESTIONS: list[dict[str, str]] = [
    {
        "q": "Какой вирус считается первым для IBM PC?",
        "a": "Brain",
        "hint": "Создан в Пакистане в 1986 году.",
    },
    {
        "q": "Как называется червь, атаковавший ядерные объекты Ирана в 2010?",
        "a": "Stuxnet",
        "hint": "Разработан совместно США и Израилем.",
    },
    {
        "q": "Какая уязвимость OpenSSL 2014 года позволяла читать память сервера?",
        "a": "Heartbleed",
        "hint": "Название связано с 'сердцем' (heartbeat).",
    },
    {
        "q": "Какой ransomware вызвал глобальную атаку в 2017, используя EternalBlue?",
        "a": "WannaCry",
        "hint": "Название означает 'хочу плакать'.",
    },
    {
        "q": "Какая атака 2020 года связана с компрометацией обновлений ПО?",
        "a": "SolarWinds",
        "hint": "Название компании-поставщика мониторинга.",
    },
    {
        "q": "Какая уязвимость Log4j 2021 года позволяла удалённое выполнение кода?",
        "a": "Log4Shell",
        "hint": "Название содержит 'Shell'.",
    },
    {
        "q": "В каком году появился термин 'computer virus'?",
        "a": "1983",
        "hint": "Фред Коэн использовал его в академической работе.",
    },
    {
        "q": "Какой червь 1988 года стал первой крупной сетевой атакой?",
        "a": "Morris",
        "hint": "Назван в честь создателя Роберта Морриса.",
    },
]


def _display_timeline() -> None:
    """Вывести полную хронологию эпох."""
    table = Table(title="📜 Эволюция кибербезопасности")
    table.add_column("Эпоха", style="cyan", width=25)
    table.add_column("Период", style="green", width=15)
    table.add_column("Ключевые события", style="yellow")

    for era in ERAS:
        events = "\n".join([f"{e['year']}: {e['event']}" for e in era["events"][:2]])
        table.add_row(era["name"], era["period"], events)

    console.print(table)
    console.print("\n[dim]Используйте /timeline era <название> для деталей.[/dim]")


def _display_era_details(era_name: str) -> bool:
    """Вывести детали конкретной эпохи."""
    era = next((e for e in ERAS if era_name.lower() in e["name"].lower()), None)
    if not era:
        console.print(f"[red]Эпоха '{era_name}' не найдена.[/red]")
        console.print("[yellow]Доступные:[/yellow] " + ", ".join([e["name"].split(":")[0] for e in ERAS]))
        return False

    content = f"""[bold]Период:[/bold] {era['period']}
[bold]Описание:[/bold] {era['description']}

[bold]📅 Ключевые события:[/bold]"""
    for e in era["events"]:
        content += f"\n  • {e['year']}: {e['event']}"

    content += f"\n\n[bold]🛠️ Инструменты эпохи:[/bold] {', '.join(era['tools'])}"
    content += f"\n\n[bold]⚠️ Типичные уязвимости:[/bold] {', '.join(era['vulnerabilities'])}"

    console.print(Panel(content, title=era["name"], border_style="cyan"))

    ctx = get_context()
    state = ctx.state
    if hasattr(state, "xp"):
        state.xp += era["xp"]
        console.print(f"[green]+{era['xp']} XP за изучение эпохи![/green]")
    return True


def _run_history_quiz() -> None:
    """Запустить викторину по истории кибербезопасности."""
    console.print(Panel("🧠 Викторина: История кибербезопасности", border_style="magenta"))

    questions = random.sample(QUIZ_QUESTIONS, min(3, len(QUIZ_QUESTIONS)))
    score = 0

    for i, q in enumerate(questions, 1):
        console.print(f"\n[bold]Вопрос {i}:[/bold] {q['q']}")
        console.print(f"[dim]Подсказка: {q['hint']}[/dim]")

        # В CLI режиме симулируем правильный ответ для демонстрации
        console.print(f"[green]Правильный ответ: {q['a']}[/green]")
        score += 1

    console.print(Panel(f"Результат: {score}/{len(questions)}", border_style="green"))

    ctx = get_context()
    state = ctx.state
    if hasattr(state, "xp"):
        bonus = score * 10
        state.xp += bonus
        console.print(f"[green]+{bonus} XP за викторину![/green]")


def handle_timeline(args: str) -> tuple[str, bool]:
    """Главный обработчик команды /timeline."""
    parts = args.strip().split(maxsplit=1)
    if not parts or parts[0] == "":
        _display_timeline()
        return "", True

    subcommand = parts[0].lower()
    query = parts[1] if len(parts) > 1 else ""

    if subcommand == "era" and query:
        success = _display_era_details(query)
        return "", success
    elif subcommand == "quiz":
        _run_history_quiz()
        return "", True
    elif subcommand == "help":
        console.print(Panel(
            "[bold]Команды Historical Mode:[/bold]\n"
            "/timeline              — Хронология эпох\n"
            "/timeline era <name>   — Детали эпохи\n"
            "/timeline quiz         — Викторина по истории",
            border_style="yellow",
        ))
        return "", True
    else:
        console.print(f"[red]Неизвестная подкоманда: {subcommand}[/red]")
        _display_timeline()
        return "", True
