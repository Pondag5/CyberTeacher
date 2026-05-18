"""Telegram бот для CyberTeacher (H-08).

Команды:
    /telegram start    — Запустить бота
    /telegram stop     — Остановить бота
    /telegram status   — Статус бота
    /telegram help     — Справка
"""

import os
import threading
from typing import Tuple

from rich.panel import Panel

from ui import console

# Попытка импорта python-telegram-bot
try:
    from telegram import Update
    from telegram.ext import (
        Application,
        CommandHandler,
        ContextTypes,
        MessageHandler,
        filters,
    )
    TELEGRAM_AVAILABLE = True
except ImportError:
    TELEGRAM_AVAILABLE = False

_bot_app = None
_bot_running = False


def _start_bot(token: str = None) -> bool:
    """Запустить Telegram бота."""
    global _bot_app, _bot_running

    if not TELEGRAM_AVAILABLE:
        console.print("[red]python-telegram-bot не установлен: pip install python-telegram-bot[/red]")
        return False

    token = token or os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        console.print("[red]TOKEN не найден. Установите TELEGRAM_BOT_TOKEN в .env или используйте /telegram start <token>[/red]")
        return False

    async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "🔐 Добро пожаловать в CyberTeacher!\n\n"
            "Команды:\n"
            "/quiz — Начать викторину\n"
            "/stats — Моя статистика\n"
            "/news — Новости кибербезопасности\n"
            "/help — Справка"
        )

    async def quiz_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "🧠 Викторина:\n\n"
            "Что такое XSS?\n"
            "1. Cross-Site Scripting\n"
            "2. XML Style Sheet\n"
            "3. Extra Security System\n\n"
            "Ответьте цифрой (1-3)"
        )

    async def stats_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "📊 Статистика:\n"
            "XP: 127\n"
            "Уровень: 3\n"
            "Викторин пройдено: 5\n"
            "Стрик: 3 дня"
        )

    async def news_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "📰 Последние новости:\n"
            "• Обнаружена новая APT-группа, атакующая финансовый сектор\n"
            "• Критическая уязвимость в Log4j (CVE-2021-44228)\n"
            "• Ransomware LockBit обновил инфраструктуру"
        )

    async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "🔐 CyberTeacher Bot\n\n"
            "Доступные команды:\n"
            "/start — Приветствие\n"
            "/quiz — Викторина\n"
            "/stats — Статистика\n"
            "/news — Новости\n"
            "/help — Справка"
        )

    async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text
        if text in ("1", "2", "3"):
            if text == "1":
                await update.message.reply_text("✅ Верно! +10 XP")
            else:
                await update.message.reply_text("❌ Неверно. Правильный ответ: 1. Cross-Site Scripting")
        else:
            await update.message.reply_text("Используйте /help для списка команд.")

    def _run_bot():
        global _bot_app, _bot_running
        _bot_app = Application.builder().token(token).build()
        _bot_app.add_handler(CommandHandler("start", start_cmd))
        _bot_app.add_handler(CommandHandler("quiz", quiz_cmd))
        _bot_app.add_handler(CommandHandler("stats", stats_cmd))
        _bot_app.add_handler(CommandHandler("news", news_cmd))
        _bot_app.add_handler(CommandHandler("help", help_cmd))
        _bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        _bot_running = True
        _bot_app.run_polling()

    console.print(Panel(
        "[green]🤖 Telegram бот запускается...[/green]\n"
        "Бот будет отвечать на команды в Telegram.",
        border_style="green",
    ))

    thread = threading.Thread(target=_run_bot, daemon=True)
    thread.start()
    return True


def _stop_bot() -> bool:
    """Остановить Telegram бота."""
    global _bot_app, _bot_running
    if _bot_app and _bot_running:
        _bot_app.stop()
        _bot_running = False
        console.print("[yellow]🤖 Telegram бот остановлен.[/yellow]")
        return True
    console.print("[yellow]Бот не запущен.[/yellow]")
    return False


def handle_telegram(args: str) -> tuple[str, bool]:
    """Главный обработчик команды /telegram."""
    parts = args.strip().split(maxsplit=1)
    subcommand = parts[0].lower() if parts else ""
    query = parts[1] if len(parts) > 1 else ""

    if subcommand == "start":
        success = _start_bot(query if query else None)
        return "", success
    elif subcommand == "stop":
        _stop_bot()
        return "", True
    elif subcommand == "status":
        status = "Запущен" if _bot_running else "Остановлен"
        console.print(Panel(
            f"[bold]Telegram бот:[/bold] {status}\n"
            f"[dim]Требуется: pip install python-telegram-bot[/dim]",
            border_style="cyan",
        ))
        return "", True
    elif subcommand == "help":
        console.print(Panel(
            "[bold]Команды Telegram:[/bold]\n"
            "/telegram start [token] — Запустить бота\n"
            "/telegram stop        — Остановить бота\n"
            "/telegram status      — Проверить статус",
            border_style="yellow",
        ))
        return "", True
    else:
        console.print(f"[red]Неизвестная подкоманда: {subcommand}[/red]")
        return "", True
