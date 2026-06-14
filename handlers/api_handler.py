"""Обработчик команды /api — запуск REST API сервера."""

from typing import Any, Tuple

from rich.panel import Panel

from ui import console
from handlers.types import HandlerResult



def handle_api(action: str) -> HandlerResult:
    """Обработчик команды /api."""
    parts = action.strip().split(maxsplit=1)
    # Если только "api" без аргументов — показать help/status
    if len(parts) == 1:
        subcommand = ""
    else:
        subcommand = parts[1].lower().strip()
    query = ""  # query пока не используется, можно расширить при необходимости

    if subcommand == "" or subcommand == "help":
        console.print(
            Panel(
                "[bold]Команды API:[/bold]\n"
                "/api start   — Запустить REST API сервер\n"
                "/api stop    — Остановить сервер\n"
                "/api status  — Проверить статус\n"
                "/api list    — Все доступные endpoints\n\n"
                "[dim]Требуется: pip install fastapi uvicorn[/dim]",
                border_style="yellow",
            )
        )
        return True, None, None, True
    elif subcommand == "start":
        try:
            from api_server import is_server_running, start_api_server

            if is_server_running():
                console.print("[yellow]⚠️ Сервер уже запущен.[/yellow]")
                return True, None, None, True

            console.print(
                Panel(
                    "[bold]🚀 Запуск REST API сервера...[/bold]\n"
                    "URL: http://localhost:8000\n"
                    "Docs: http://localhost:8000/docs\n\n"
                    "[dim]Сервер запущен в отдельном процессе.[/dim]",
                    border_style="green",
                )
            )
            if start_api_server():
                console.print("[green]✅ Сервер запущен.[/green]")
            else:
                console.print("[red]❌ Ошибка запуска сервера.[/red]")
        except ImportError:
            console.print(
                "[red]FastAPI не установлен: pip install fastapi uvicorn[/red]"
            )
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
        console.print(
            Panel(
                "[bold]REST API Status:[/bold]\n"
                "Сервер: Остановлен\n"
                "Endpoints: /api/health, /api/progress, /api/stats, /api/achievements, /api/weak-topics\n\n"
                "[dim]Используйте /api start для запуска.[/dim]",
                border_style="yellow",
            )
        )
        return True, None, None, True
    elif subcommand == "list":
        from rich.table import Table

        table = Table(title="REST API Endpoints (65)", border_style="cyan")
        table.add_column("Method", style="bold", width=6)
        table.add_column("Endpoint", style="green")
        table.add_column("Description")

        for method, endpoint, desc in [
            ("GET", "/health_check", "Health status"),
            ("GET", "/get_progress", "User progress"),
            ("GET", "/get_modes", "Teaching modes"),
            ("GET", "/get_profile", "User profile"),
            ("GET", "/get_courses", "Courses list"),
            ("GET", "/get_labs", "Docker labs"),
            ("GET", "/get_achievements_list", "Achievements (29)"),
            ("GET", "/get_skills", "User skills"),
            ("GET", "/get_shop", "Shop (17 items)"),
            ("GET", "/get_heatmap", "Activity heatmap 28d"),
            ("GET", "/get_history", "Chat history"),
            ("GET", "/get_config", "Configuration"),
            ("GET", "/get_story_episodes", "Story episodes (21)"),
            ("GET", "/get_tracks", "Learning tracks (4)"),
            ("GET", "/get_ctf_status", "CTF status"),
            ("GET", "/get_missions", "Missions"),
            ("GET", "/get_threats", "APT groups (27)"),
            ("GET", "/get_news", "Security news"),
            ("GET", "/get_daily_challenge", "Daily challenge"),
            ("GET", "/get_detailed_stats", "Detailed stats"),
            ("GET", "/get_versus_scenarios", "Versus scenarios (4)"),
            ("GET", "/docker_status", "Docker status"),
            ("GET", "/docker_containers", "Running containers"),
            ("GET", "/get_personality", "Personality drift"),
            ("GET", "/get_context", "Context awareness"),
            ("GET", "/get_world", "Persistent world"),
            ("GET", "/get_episodes", "Episode memory"),
            ("GET", "/get_cyberpsychosis", "Cyberpsychosis status"),
            ("GET", "/verify_auth", "Verify JWT token"),
            ("WS", "/chat_stream", "WebSocket streaming"),
            ("POST", "/chat_with_llm", "Chat with LLM"),
            ("POST", "/generate_quiz", "Generate quiz"),
            ("POST", "/submit_quiz_result", "Submit quiz"),
            ("POST", "/submit_flag", "Submit CTF flag"),
            ("POST", "/submit_daily_challenge", "Submit daily"),
            ("POST", "/set_mode", "Set teaching mode"),
            ("POST", "/select_course", "Select course"),
            ("POST", "/update_profile", "Update profile"),
            ("POST", "/start_lab", "Start Docker lab"),
            ("POST", "/stop_lab", "Stop Docker lab"),
            ("POST", "/start_versus", "Start versus"),
            ("POST", "/versus_move", "Versus move"),
            ("POST", "/scan_code", "Security scan"),
            ("POST", "/purchase_item", "Purchase item"),
            ("POST", "/register", "Register user"),
            ("POST", "/login", "Login user"),
        ]:
            color = (
                "green" if method == "GET" else "cyan" if method == "POST" else "yellow"
            )
            table.add_row(f"[{color}]{method}[/{color}]", endpoint, desc)

        console.print(table)
        return True, None, None, True
    else:
        console.print(f"[red]Неизвестная подкоманда: {subcommand}[/red]")
        return True, None, None, True
