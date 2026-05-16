"""Модуль Interactive Investigations — интерактивные расследования.

Команды:
    /investigation           — Список кейсов
    /investigation start <id>— Начать расследование
    /investigation examine <item> — Изучить улику
    /investigation conclude <suspect> — Обвинить подозреваемого
    /investigation help      — Справка
"""

import random
from typing import Any, Dict, List, Tuple

from rich.panel import Panel
from rich.table import Table

from state import get_state
from ui import console

CASES: Dict[str, Dict[str, Any]] = {
    "corp_espionage": {
        "title": "Корпоративный шпионаж",
        "description": "В компании TechCorp произошла утечка чертежей нового продукта. Найдите шпиона.",
        "suspects": ["Иванов (Бухгалтер)", "Петрова (Инженер)", "Сидоров (Менеджер)", "Козлов (IT-админ)"],
        "culprit": "Петрова (Инженер)",
        "evidence": {
            "email_logs": "Обнаружены письма на внешний до competitor.com от p.petrova@techcorp.local",
            "usb_logs": "Подключено USB-устройство 'Kingston 64GB' к workstation-12 (Петрова)",
            "access_logs": "Доступ к папке 'R&D/Blueprints' в 23:45 (нерабочее время)",
            "browser_history": "Поисковые запросы: 'как обойти DLP', 'шифрование архивов'",
        },
        "red_herrings": [
            "Иванов скачивал зарплатные ведомости (но это его работа)",
            "Козлов тестировал эксплойты (но в лаборатории)",
        ],
        "xp": 60,
    },
    "data_leak": {
        "title": "Утечка данных клиентов",
        "description": "База данных клиентов попала в даркнет. Определите вектор утечки.",
        "suspects": ["Внешний хакер", "Инсайдер (Маркетинг)", "Ошибка конфигурации S3", "Фишинг"],
        "culprit": "Ошибка конфигурации S3",
        "evidence": {
            "server_logs": "Нет следов взлома, аутентификация не нарушена",
            "cloud_config": "S3 bucket 'client-data-prod' имеет ACL: public-read",
            "shodan_scan": "Bucket проиндексирован и доступен без авторизации",
            "darknet_post": "Файл найден на форуме, источник: 'open source intel'",
        },
        "red_herrings": [
            "Фишинговая рассылка была, но никто не кликнул",
            "Маркетинг выгружал отчёты, но только агрегированные",
        ],
        "xp": 50,
    },
    "insider_threat": {
        "title": "Инсайдерская угроза",
        "description": "Сотрудник перед увольнением удалил критические данные. Найдите доказательства.",
        "suspects": ["Алексеев (DevOps)", "Борисова (HR)", "Волков (Sales)"],
        "culprit": "Алексеев (DevOps)",
        "evidence": {
            "git_history": "Коммит 'cleanup' удалил 15 репозиториев за 2 часа до увольнения",
            "terminal_log": "Выполнено: rm -rf /var/backups/* && shred -n 3 /etc/passwd",
            "badge_access": "Пропуск использован в 03:00 (офис пуст)",
            "exit_interview": "Алексеев выразил недовольство на встрече с HR",
        },
        "red_herrings": [
            "Волков экспортировал CRM (но для портфолио, без чувствительных данных)",
            "Борисова удаляла старые резюме (по политике хранения)",
        ],
        "xp": 55,
    },
}


def _display_cases() -> None:
    """Вывести список кейсов."""
    table = Table(title="🔍 Интерактивные расследования")
    table.add_column("ID", style="cyan")
    table.add_column("Название", style="green")
    table.add_column("Описание", style="yellow")

    for cid, case in CASES.items():
        table.add_row(cid, case["title"], case["description"][:50] + "...")

    console.print(table)
    console.print("\n[dim]Используйте /investigation start <id> для начала.[/dim]")


def _start_case(case_id: str) -> bool:
    """Начать расследование."""
    case = CASES.get(case_id)
    if not case:
        console.print(f"[red]Кейс '{case_id}' не найден.[/red]")
        return False

    console.print(Panel(
        f"[bold]Описание:[/bold] {case['description']}\n"
        f"[bold]Подозреваемые:[/bold] {', '.join(case['suspects'])}\n\n"
        f"[dim]Изучайте улики: email_logs, usb_logs, access_logs, browser_history, server_logs и др.[/dim]",
        title=case["title"],
        border_style="cyan",
    ))

    state = get_state()
    if hasattr(state, "current_case"):
        state.current_case = case_id
        state.found_evidence = []
    return True


def _examine_evidence(item: str) -> bool:
    """Изучить улику."""
    state = get_state()
    case_id = getattr(state, "current_case", None)
    if not case_id:
        console.print("[yellow]Сначала начните расследование.[/yellow]")
        return False

    case = CASES.get(case_id)
    evidence = case["evidence"].get(item)
    if evidence:
        console.print(Panel(f"[bold]{item}:[/bold]\n{evidence}", border_style="green"))
        if hasattr(state, "found_evidence") and item not in state.found_evidence:
            state.found_evidence.append(item)
            if hasattr(state, "xp"):
                state.xp += 10
                console.print("[green]+10 XP за найденную улику![/green]")
        return True
    else:
        console.print(f"[yellow]Улика '{item}' не найдена в этом кейсе.[/yellow]")
        return False


def _conclude(suspect: str) -> bool:
    """Обвинить подозреваемого."""
    state = get_state()
    case_id = getattr(state, "current_case", None)
    if not case_id:
        console.print("[yellow]Сначала начните расследование.[/yellow]")
        return False

    case = CASES.get(case_id)
    if suspect.lower() == case["culprit"].lower():
        evidence_count = len(getattr(state, "found_evidence", []))
        bonus = evidence_count * 5
        total_xp = case["xp"] + bonus
        console.print(Panel(
            f"[green]✅ Верно! {case['culprit']} — виновник.[/green]\n"
            f"[bold]Найдено улик:[/bold] {evidence_count}\n"
            f"[bold]Бонус за улики:[/bold] +{bonus} XP\n"
            f"[bold]Итого:[/bold] +{total_xp} XP",
            border_style="green",
        ))
        if hasattr(state, "xp"):
            state.xp += total_xp
        state.current_case = None
        return True
    else:
        console.print(Panel(
            f"[red]❌ Неверно. {suspect} не является виновником.[/red]\n"
            f"[dim]Попробуйте изучить больше улик.[/dim]",
            border_style="red",
        ))
        return False


def handle_investigation(args: str) -> Tuple[str, bool]:
    """Главный обработчик команды /investigation."""
    parts = args.strip().split(maxsplit=1)
    if not parts or parts[0] == "":
        _display_cases()
        return "", True

    subcommand = parts[0].lower()
    query = parts[1] if len(parts) > 1 else ""

    if subcommand == "start" and query:
        success = _start_case(query)
        return "", success
    elif subcommand == "examine" and query:
        success = _examine_evidence(query)
        return "", success
    elif subcommand == "conclude" and query:
        success = _conclude(query)
        return "", success
    elif subcommand == "help":
        console.print(Panel(
            "[bold]Команды расследования:[/bold]\n"
            "/investigation              — Список кейсов\n"
            "/investigation start <id>   — Начать расследование\n"
            "/investigation examine <item>— Изучить улику\n"
            "/investigation conclude <name> — Обвинить подозреваемого",
            border_style="yellow",
        ))
        return "", True
    else:
        console.print(f"[red]Неизвестная подкоманда: {subcommand}[/red]")
        _display_cases()
        return "", True
