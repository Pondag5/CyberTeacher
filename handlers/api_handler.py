"""Обработчик команды /api — запуск REST API сервера."""

import threading
from typing import Tuple

from rich.panel import Panel

from ui import console


def handle_api(args: str) -> Tuple[str, bool]:
    """Обработчик команды /api."""
    parts = args.strip().split(maxsplit=1)
    subcommand = parts[0].lower() if parts else ""
    query = parts[1] if len(parts) > 1 else ""

    if subcommand == "start":
        console.print(Panel(
            "[bold]🚀 Запуск REST API сервера...[/bold]\n"
            "URL: http://localhost:8000\n"
            "Docs: http://localhost:8000/docs\n\n"
            "[dim]Сервер запущен в фоновом потоке.[/dim]",
            border_style="green",
        ))
        # Запуск в фоновом потоке
        def _start():
            try:
                from api_server import start_api_server
                start_api_server()
            except ImportError:
                console.print("[red]FastAPI не установлен: pip install fastapi uvicorn[/red]")

        thread = threading.Thread(target=_start, daemon=True)
        thread.start()
        return "", True
    elif subcommand == "stop":
        console.print("[yellow]API сервер останавливается...[/yellow]")
        return "", True
    elif subcommand == "status":
        console.print(Panel(
            "[bold]REST API Status:[/bold]\n"
            "Сервер: Остановлен\n"
            "Endpoints: /api/health, /api/progress, /api/stats, /api/achievements, /api/weak-topics\n\n"
            "[dim]Используйте /api start для запуска.[/dim]",
            border_style="yellow",
        ))
        return "", True
    elif subcommand == "help":
        console.print(Panel(
            "[bold]Команды API:[/bold]\n"
            "/api start   — Запустить REST API сервер\n"
            "/api stop    — Остановить сервер\n"
            "/api status  — Проверить статус\n\n"
            "[dim]Требуется: pip install fastapi uvicorn[/dim]",
            border_style="yellow",
        ))
        return "", True
    else:
        console.print(f"[red]Неизвестная подкоманда: {subcommand}[/red]")
        return "", True
