"""Обработчик команды /api — запуск REST API сервера."""

from typing import Any, Tuple

from rich.panel import Panel

from ui import console


def handle_api(action: str) -> tuple[bool, Any | None, Any | None, bool]:
    """Обработчик команды /api."""
    parts = action.strip().split(maxsplit=1)
    # Если только "api" без аргументов — показать help/status
    if len(parts) == 1:
        subcommand = ""
    else:
        subcommand = parts[1].lower().strip()
    query = "" # query пока не используется, можно расширить при необходимости

    if subcommand == "" or subcommand == "help":
        console.print(Panel(
            "[bold]Команды API:[/bold]\n"
            "/api start   — Запустить REST API сервер\n"
            "/api stop    — Остановить сервер\n"
            "/api status  — Проверить статус\n\n"
            "[dim]Требуется: pip install fastapi uvicorn[/dim]",
            border_style="yellow",
        ))
        return True, None, None, True
    elif subcommand == "start":
        try:
            from api_server import is_server_running, start_api_server
            if is_server_running():
                console.print("[yellow]⚠️ Сервер уже запущен.[/yellow]")
                return True, None, None, True
            
            console.print(Panel(
                "[bold]🚀 Запуск REST API сервера...[/bold]\n"
                "URL: http://localhost:8000\n"
                "Docs: http://localhost:8000/docs\n\n"
                "[dim]Сервер запущен в отдельном процессе.[/dim]",
                border_style="green",
            ))
            if start_api_server():
                console.print("[green]✅ Сервер запущен.[/green]")
            else:
                console.print("[red]❌ Ошибка запуска сервера.[/red]")
        except ImportError:
            console.print("[red]FastAPI не установлен: pip install fastapi uvicorn[/red]")
        return True, None, None, True
    elif subcommand == "stop":
        try:
            from api_server import stop_api_server
            if stop_api_server():
                console.print("[green]✅ API сервер остановлен.[/green]")
            else:
                console.print("[yellow]Сервер не был запущен.[/yellow]")
        except Exception as e:
            console.print(f"[red]Ошибка остановки: {e}[/red]")
        return True, None, None, True
    elif subcommand == "status":
        console.print(Panel(
            "[bold]REST API Status:[/bold]\n"
            "Сервер: Остановлен\n"
            "Endpoints: /api/health, /api/progress, /api/stats, /api/achievements, /api/weak-topics\n\n"
            "[dim]Используйте /api start для запуска.[/dim]",
            border_style="yellow",
        ))
        return True, None, None, True
    else:
        console.print(f"[red]Неизвестная подкоманда: {subcommand}[/red]")
        return True, None, None, True
