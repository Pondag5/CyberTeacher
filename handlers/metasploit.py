"""
💀 Metasploit интеграция (L-09)

Команды:
- /msf search <keyword> — поиск эксплойтов/модулей
- /msf info <module> — информация о модуле
- /msf options <module> — опции модуля
- /msf run <module> <options> — запуск модуля
- /msf sessions — активные сессии
- /msf help — справка

Примечание: Требует запущенный Metasploit RPC сервер (msfrpcd).
"""

import json
import logging
import os
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()
logger = logging.getLogger(__name__)

# Попытка импорта pymetasploit3
try:
    from pymetasploit3.msfrpc import MsfRpcClient
    HAS_METASPLOIT = True
except ImportError:
    HAS_METASPLOIT = False

# Настройки подключения
MSF_HOST = os.getenv("MSF_HOST", "127.0.0.1")
MSF_PORT = int(os.getenv("MSF_PORT", "55553"))
MSF_PASSWORD = os.getenv("MSF_PASSWORD", "abc123")
MSF_URI = os.getenv("MSF_URI", "/api")


def get_msf_client() -> Any | None:
    """Получить клиент Metasploit RPC."""
    if not HAS_METASPLOIT:
        console.print("[yellow]⚠️ pymetasploit3 не установлен. Установите: pip install pymetasploit3[/yellow]")
        return None

    try:
        client = MsfRpcClient(MSF_PASSWORD, server=MSF_HOST, port=MSF_PORT, uri=MSF_URI, ssl=True)
        return client
    except Exception as e:
        logger.error(f"Metasploit connection failed: {e}")
        console.print(f"[red]❌ Не удалось подключиться к Metasploit: {e}[/red]")
        return None


def handle_msf_search(keyword: str) -> tuple[bool, Any | None, Any | None, bool]:
    """Поиск модулей Metasploit."""
    client = get_msf_client()
    if not client:
        return True, None, None, True

    try:
        # Поиск по всем типам модулей
        results = {
            "exploits": [],
            "auxiliary": [],
            "post": [],
            "encoders": [],
            "nops": [],
            "payloads": [],
        }

        # Поиск через RPC
        for module_type in ["exploit", "auxiliary", "post", "encoder", "nop", "payload"]:
            modules = client.modules.modules[module_type]
            for name, info in modules.items():
                if keyword.lower() in name.lower() or keyword.lower() in info.get("name", "").lower():
                    results[f"{module_type}s"].append({
                        "name": name,
                        "description": info.get("name", ""),
                        "rank": info.get("rank", ""),
                        "disclosure_date": info.get("disclosure_date", ""),
                    })

        # Отображение результатов
        total = sum(len(v) for v in results.values())
        if total == 0:
            console.print(f"[yellow]Модули по запросу '{keyword}' не найдены[/yellow]")
            return True, None, None, True

        console.print(f"[bold]Найдено {total} модулей по запросу '{keyword}'[/bold]")

        for module_type, modules in results.items():
            if modules:
                table = Table(title=f"{module_type.capitalize()} ({len(modules)})")
                table.add_column("Name", style="cyan")
                table.add_column("Description")
                table.add_column("Rank", style="yellow")

                for m in modules[:20]:
                    table.add_row(
                        m["name"][:50],
                        m["description"][:60],
                        m["rank"],
                    )

                console.print(table)
                if len(modules) > 20:
                    console.print(f"  [dim]...и ещё {len(modules) - 20}[/dim]")

        return True, None, None, True

    except Exception as e:
        console.print(f"[red]Ошибка поиска: {e}[/red]")
        return True, None, None, True


def handle_msf_info(module_name: str) -> tuple[bool, Any | None, Any | None, bool]:
    """Информация о модуле."""
    client = get_msf_client()
    if not client:
        return True, None, None, True

    try:
        # Определяем тип модуля
        module_type = module_name.split("/", maxsplit=1)[0] if "/" in module_name else "exploit"

        # Получаем информацию
        info = client.modules.info(module_type, module_name)

        if not info:
            console.print(f"[red]Модуль {module_name} не найден[/red]")
            return True, None, None, True

        # Отображение
        details = (
            f"[bold]Name:[/bold] {info.get('name', '')}\n"
            f"[bold]Description:[/bold] {info.get('description', '')[:500]}\n"
            f"[bold]Rank:[/bold] {info.get('rank', '')}\n"
            f"[bold]Disclosure Date:[/bold] {info.get('disclosure_date', '')}\n"
            f"[bold]Author:[/bold] {', '.join(info.get('author', [])[:5])}\n"
            f"[bold]License:[/bold] {info.get('license', '')}\n"
            f"[bold]Platform:[/bold] {', '.join(info.get('platform', []))}\n"
            f"[bold]Arch:[/bold] {', '.join(info.get('arch', []))}\n"
            f"[bold]Targets:[/bold] {', '.join(info.get('targets', [])[:5])}"
        )

        console.print(Panel(details, title=f"Module: {module_name}", border_style="cyan"))

        return True, None, None, True

    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
        return True, None, None, True


def handle_msf_options(module_name: str) -> tuple[bool, Any | None, Any | None, bool]:
    """Опции модуля."""
    client = get_msf_client()
    if not client:
        return True, None, None, True

    try:
        module_type = module_name.split("/", maxsplit=1)[0] if "/" in module_name else "exploit"
        info = client.modules.info(module_type, module_name)

        if not info:
            console.print(f"[red]Модуль {module_name} не найден[/red]")
            return True, None, None, True

        options = info.get("options", {})
        if not options:
            console.print("[yellow]Нет опций[/yellow]")
            return True, None, None, True

        table = Table(title=f"Options: {module_name}")
        table.add_column("Name", style="cyan")
        table.add_column("Required")
        table.add_column("Default")
        table.add_column("Description")

        for name, opt in options.items():
            table.add_row(
                name,
                "Yes" if opt.get("required", False) else "No",
                str(opt.get("default", "")),
                opt.get("desc", "")[:50],
            )

        console.print(table)
        return True, None, None, True

    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
        return True, None, None, True


def handle_msf_sessions() -> tuple[bool, Any | None, Any | None, bool]:
    """Активные сессии."""
    client = get_msf_client()
    if not client:
        return True, None, None, True

    try:
        sessions = client.sessions.list

        if not sessions:
            console.print("[yellow]Нет активных сессий[/yellow]")
            return True, None, None, True

        table = Table(title="Active Sessions")
        table.add_column("ID", style="cyan")
        table.add_column("Type")
        table.add_column("Info")
        table.add_column("Tunnel")
        table.add_column("UUID")

        for sid, session in sessions.items():
            table.add_row(
                str(sid),
                session.get("type", ""),
                session.get("session_host", ""),
                session.get("tunnel_local", ""),
                session.get("uuid", "")[:8],
            )

        console.print(table)
        return True, None, None, True

    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
        return True, None, None, True


def handle_msf_action(action: str) -> tuple[bool, Any | None, Any | None, bool]:
    """Обработка /msf <subcommand>."""
    parts = action.split()

    if len(parts) < 2:
        console.print("[cyan]Использование:[/cyan]")
        console.print("  /msf search <keyword>     — поиск модулей")
        console.print("  /msf info <module>        — информация о модуле")
        console.print("  /msf options <module>     — опции модуля")
        console.print("  /msf sessions             — активные сессии")
        console.print("\n[dim]Требуется: msfrpcd запущен, pymetasploit3 установлен[/dim]")
        console.print("[dim]Настройка: MSF_HOST, MSF_PORT, MSF_PASSWORD в .env[/dim]")
        return True, None, None, True

    subcmd = parts[1]

    if subcmd == "search" and len(parts) >= 3:
        return handle_msf_search(" ".join(parts[2:]))
    elif subcmd == "info" and len(parts) >= 3:
        return handle_msf_info(parts[2])
    elif subcmd == "options" and len(parts) >= 3:
        return handle_msf_options(parts[2])
    elif subcmd == "sessions":
        return handle_msf_sessions()
    else:
        console.print(f"[red]Неизвестная подкоманда: {subcmd}[/red]")
        return True, None, None, True
