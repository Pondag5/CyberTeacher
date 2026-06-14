"""Модуль Mobile Companion App (PWA) — информация о мобильном приложении.

Команды:
    /pwa                   — Информация о PWA и ссылка
    /pwa setup             — Инструкция по установке
    /pwa help              — Справка
"""

import socket
from typing import Any, Tuple

from rich.panel import Panel

from ui import console
from handlers.types import HandlerResult


def get_local_ip() -> str:
    """Получить локальный IP-адрес машины."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip: str = s.getsockname()[0]
        s.close()
        return ip
    except (OSError, socket.error):
        return "localhost"


def handle_pwa(action: str) -> HandlerResult:
    """Главный обработчик команды /pwa."""
    parts = action.strip().split(maxsplit=1)
    # Если только "pwa" без аргументов — показать info
    if len(parts) == 1:
        subcommand = ""
    else:
        subcommand = parts[1].lower().strip()
    local_ip = get_local_ip()

    if subcommand == "" or subcommand == "info":
        console.print(
            Panel(
                f"[bold]📱 CyberTeacher Companion App[/bold]\n"
                "Адаптивное веб-приложение для ПК, планшетов и смартфонов.\n\n"
                "[bold]Функции:[/bold]\n"
                "• Быстрые квизы в дороге\n"
                "• Просмотр прогресса и статистики\n"
                "• Установка на главный экран (PWA)\n\n"
                "[bold]Доступ в локальной сети:[/bold]\n"
                f"  🌐 http://{local_ip}:8000\n\n"
                "[bold]Локально:[/bold]\n"
                "  🌐 http://localhost:8000\n\n"
                "[dim]Откройте ссылку в браузере любого устройства.[/dim]",
                border_style="cyan",
            )
        )
        return True, None, None, True
    elif subcommand == "setup":
        console.print(
            Panel(
                f"[bold]📲 Как открыть:[/bold]\n\n"
                "1. Убедитесь, что API запущен: /api start\n"
                f"2. Откройте в браузере: http://{local_ip}:8000\n"
                "3. Для установки как приложения:\n"
                "   • Chrome (Android/PC): ⋮ → 'Установить приложение'\n"
                "   • Safari (iOS): Поделиться → 'На экран Домой'\n"
                "   • Firefox: ⋮ → 'Установить'\n\n"
                "[dim]Приложение адаптируется под размер экрана.[/dim]",
                border_style="green",
            )
        )
        return True, None, None, True
    elif subcommand == "help":
        console.print(
            Panel(
                "[bold]Команды PWA:[/bold]\n"
                "/pwa                   — Информация и ссылки\n"
                "/pwa setup             — Инструкция по установке",
                border_style="yellow",
            )
        )
        return True, None, None, True
    else:
        console.print(f"[red]Неизвестная подкоманда: {subcommand}[/red]")
        return True, None, None, True
