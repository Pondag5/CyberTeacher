"""Модуль Mobile Companion App (PWA) — информация о мобильном приложении.

Команды:
    /pwa                   — Информация о PWA и ссылка
    /pwa setup             — Инструкция по установке
    /pwa help              — Справка
"""

from typing import Tuple

from rich.panel import Panel

from ui import console


def handle_pwa(args: str) -> Tuple[str, bool]:
    """Главный обработчик команды /pwa."""
    parts = args.strip().split(maxsplit=1)
    subcommand = parts[0].lower() if parts else ""

    if subcommand == "" or subcommand == "info":
        console.print(Panel(
            "[bold]📱 CyberTeacher Companion App[/bold]\n"
            "PWA-приложение для мобильных устройств.\n\n"
            "[bold]Функции:[/bold]\n"
            "• Быстрые квизы в дороге\n"
            "• Уведомления о повторениях\n"
            "• Синхронизация прогресса\n\n"
            "[bold]URL:[/bold] http://localhost:8501/pwa\n"
            "[dim]Откройте в браузере и добавьте на главный экран.[/dim]",
            border_style="cyan",
        ))
        return "", True
    elif subcommand == "setup":
        console.print(Panel(
            "[bold]📲 Установка PWA:[/bold]\n\n"
            "1. Откройте http://localhost:8501/pwa\n"
            "2. В Chrome: ⋮ → 'Установить приложение'\n"
            "3. В Safari: Поделиться → 'На экран Домой'\n"
            "4. В Firefox: ⋮ → 'Установить'\n\n"
            "[dim]Приложение будет работать офлайн после загрузки.[/dim]",
            border_style="green",
        ))
        return "", True
    elif subcommand == "help":
        console.print(Panel(
            "[bold]Команды PWA:[/bold]\n"
            "/pwa                   — Информация о приложении\n"
            "/pwa setup             — Инструкция по установке",
            border_style="yellow",
        ))
        return "", True
    else:
        console.print(f"[red]Неизвестная подкоманда: {subcommand}[/red]")
        return "", True
