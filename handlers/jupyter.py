"""Модуль Jupyter Notebook Support — шаблоны ноутбуков для практики.

Команды:
    /jupyter               — Список шаблонов
    /jupyter open <name>   — Открыть шаблон
    /jupyter run <cell>    — Выполнить ячейку
    /jupyter submit        — Отправить на проверку
    /jupyter help          — Справка
"""

import random
from typing import Any, Dict, List, Tuple

from rich.panel import Panel
from rich.table import Table

from state import get_state
from ui import console

NOTEBOOK_TEMPLATES: Dict[str, Dict[str, Any]] = {
    "crypto_basics": {
        "title": "Основы криптографии",
        "description": "Шифрование/дешифрование Caesar, XOR, Base64.",
        "cells": [
            {"id": 1, "code": "def caesar_encrypt(text, shift): ...", "output": "Функция определена"},
            {"id": 2, "code": "caesar_encrypt('HELLO', 3)", "output": "KHOOR"},
            {"id": 3, "code": "import base64; base64.b64encode(b'secret')", "output": "b'c2VjcmV0'"},
        ],
        "xp": 30,
    },
    "web_scraping": {
        "title": "Web Scraping для OSINT",
        "description": "Сбор данных с сайтов с помощью BeautifulSoup.",
        "cells": [
            {"id": 1, "code": "import requests; r = requests.get('http://example.com')", "output": "<Response [200]>"},
            {"id": 2, "code": "from bs4 import BeautifulSoup; soup = BeautifulSoup(r.text)", "output": "HTML parsed"},
            {"id": 3, "code": "soup.find_all('a')", "output": "[<a href='...'>Link</a>]"},
        ],
        "xp": 35,
    },
    "log_analysis": {
        "title": "Анализ логов (Forensics)",
        "description": "Парсинг и анализ syslog, auth.log.",
        "cells": [
            {"id": 1, "code": "with open('auth.log') as f: lines = f.readlines()", "output": "Loaded 1500 lines"},
            {"id": 2, "code": "[l for l in lines if 'Failed password' in l][:5]", "output": "5 failed attempts"},
            {"id": 3, "code": "from collections import Counter; Counter(ips).most_common(3)", "output": "[('192.168.1.10', 42)]"},
        ],
        "xp": 40,
    },
    "network_scan": {
        "title": "Сетевое сканирование",
        "description": "Использование scapy/nmap для анализа сети.",
        "cells": [
            {"id": 1, "code": "from scapy.all import sr1, IP, ICMP", "output": "Scapy loaded"},
            {"id": 2, "code": "pkt = IP(dst='192.168.1.1')/ICMP()", "output": "Packet crafted"},
            {"id": 3, "code": "resp = sr1(pkt, timeout=2)", "output": "Received ICMP reply"},
        ],
        "xp": 45,
    },
}


def _display_notebooks() -> None:
    """Вывести список шаблонов."""
    table = Table(title="📓 Jupyter Notebooks")
    table.add_column("ID", style="cyan")
    table.add_column("Название", style="green")
    table.add_column("Описание", style="yellow")
    table.add_column("XP", style="magenta")

    for nid, nb in NOTEBOOK_TEMPLATES.items():
        table.add_row(nid, nb["title"], nb["description"], str(nb["xp"]))

    console.print(table)
    console.print("\n[dim]Используйте /jupyter open <id> для начала.[/dim]")


def _open_notebook(notebook_id: str) -> bool:
    """Открыть шаблон ноутбука."""
    nb = NOTEBOOK_TEMPLATES.get(notebook_id)
    if not nb:
        console.print(f"[red]Шаблон '{notebook_id}' не найден.[/red]")
        return False

    console.print(Panel(
        f"[bold]Описание:[/bold] {nb['description']}\n"
        f"[bold]Ячеек:[/bold] {len(nb['cells'])}\n\n"
        f"[dim]Используйте /jupyter run <cell_id> для выполнения.[/dim]",
        title=nb["title"],
        border_style="cyan",
    ))

    state = get_state()
    if hasattr(state, "current_notebook"):
        state.current_notebook = notebook_id
        state.completed_cells = []
    return True


def _run_cell(cell_id: int) -> bool:
    """Выполнить ячейку."""
    state = get_state()
    notebook_id = getattr(state, "current_notebook", None)
    if not notebook_id:
        console.print("[yellow]Сначала откройте ноутбук.[/yellow]")
        return False

    nb = NOTEBOOK_TEMPLATES.get(notebook_id)
    cell = next((c for c in nb["cells"] if c["id"] == cell_id), None)
    if not cell:
        console.print(f"[red]Ячейка {cell_id} не найдена.[/red]")
        return False

    console.print(f"[bold]In [{cell_id}]:[/bold] {cell['code']}")
    console.print(f"[green]Out[{cell_id}]:[/green] {cell['output']}")

    if hasattr(state, "completed_cells") and cell_id not in state.completed_cells:
        state.completed_cells.append(cell_id)
        if hasattr(state, "xp"):
            state.xp += 5
            console.print("[green]+5 XP за ячейку![/green]")
    return True


def _submit_notebook() -> bool:
    """Отправить ноутбук на проверку."""
    state = get_state()
    notebook_id = getattr(state, "current_notebook", None)
    if not notebook_id:
        console.print("[yellow]Нет активного ноутбука.[/yellow]")
        return False

    nb = NOTEBOOK_TEMPLATES.get(notebook_id)
    completed = len(getattr(state, "completed_cells", []))
    total = len(nb["cells"])

    if completed == total:
        console.print(Panel(
            f"[green]✅ Ноутбук '{nb['title']}' завершён![/green]\n"
            f"[bold]Бонус:[/bold] +{nb['xp']} XP",
            border_style="green",
        ))
        if hasattr(state, "xp"):
            state.xp += nb["xp"]
        state.current_notebook = None
        return True
    else:
        console.print(Panel(
            f"[yellow]⚠️ Выполнено {completed}/{total} ячеек.[/yellow]\n"
            "Завершите все ячейки для получения бонуса.",
            border_style="yellow",
        ))
        return False


def handle_jupyter(args: str) -> Tuple[str, bool]:
    """Главный обработчик команды /jupyter."""
    parts = args.strip().split(maxsplit=1)
    if not parts or parts[0] == "":
        _display_notebooks()
        return "", True

    subcommand = parts[0].lower()
    query = parts[1] if len(parts) > 1 else ""

    if subcommand == "open" and query:
        success = _open_notebook(query)
        return "", success
    elif subcommand == "run" and query:
        try:
            cell_id = int(query)
            success = _run_cell(cell_id)
            return "", success
        except ValueError:
            console.print("[red]ID ячейки должен быть числом.[/red]")
            return "", False
    elif subcommand == "submit":
        success = _submit_notebook()
        return "", success
    elif subcommand == "help":
        console.print(Panel(
            "[bold]Команды Jupyter:[/bold]\n"
            "/jupyter               — Список шаблонов\n"
            "/jupyter open <id>     — Открыть ноутбук\n"
            "/jupyter run <cell_id> — Выполнить ячейку\n"
            "/jupyter submit        — Отправить на проверку",
            border_style="yellow",
        ))
        return "", True
    else:
        console.print(f"[red]Неизвестная подкоманда: {subcommand}[/red]")
        _display_notebooks()
        return "", True
