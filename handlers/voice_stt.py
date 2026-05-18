"""Модуль Voice STT — распознавание речи для голосового учителя.

Команды:
    /voice listen          — Распознать речь (STT)
    /voice status          — Статус голосовых функций
    /voice help            — Справка
"""

import random
from typing import Tuple

from rich.panel import Panel

from di import get_context
from ui import console

# Попытка импорта speech_recognition
try:
    import speech_recognition as sr
    STT_AVAILABLE = True
except ImportError:
    STT_AVAILABLE = False

SIMULATED_PHRASES: list[str] = [
    "Расскажи про SQL-инъекции",
    "Как защитить сервер от DDoS?",
    "Что такое XSS?",
    "Покажи последние новости",
    "Запусти викторину по сетям",
    "Объясни разницу между симметричным и асимметричным шифрованием",
    "Как работает фаервол?",
    "Что такое MITRE ATT&CK?",
]


def _listen_for_voice() -> str:
    """Слушать микрофон и распознать речь."""
    if STT_AVAILABLE:
        try:
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                console.print("[bold cyan]🎤 Говорите... (нажмите Ctrl+C для остановки)[/bold cyan]")
                audio = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio, language="ru-RU")
                return text
        except Exception as e:
            console.print(f"[yellow]Ошибка STT: {e}. Использую симуляцию.[/yellow]")

    # Симуляция
    return random.choice(SIMULATED_PHRASES)


def _display_voice_status() -> None:
    """Показать статус голосовых функций."""
    state = get_context().state
    tts_status = "✅ Доступен" if hasattr(state, "tts_enabled") else "❌ Не настроен"
    stt_status = "✅ Доступен (speech_recognition)" if STT_AVAILABLE else "⚠️ Симуляция (установите speech_recognition)"

    console.print(Panel(
        f"[bold]Голосовые функции:[/bold]\n"
        f"TTS (Синтез): {tts_status}\n"
        f"STT (Распознавание): {stt_status}\n\n"
        f"[dim]Для реального STT: pip install SpeechRecognition pyaudio[/dim]",
        border_style="cyan",
    ))


def handle_voice_stt(args: str) -> tuple[str, bool]:
    """Обработчик голосовых команд STT."""
    parts = args.strip().split(maxsplit=1)
    subcommand = parts[0].lower() if parts else ""

    if subcommand == "listen":
        text = _listen_for_voice()
        console.print(Panel(f"[bold]Распознано:[/bold] {text}", border_style="green"))
        # Автоматически передаём в основной обработчик
        console.print(f"[dim]Передаю в учителя: '{text}'[/dim]")
        return text, True
    elif subcommand == "status":
        _display_voice_status()
        return "", True
    elif subcommand == "help":
        console.print(Panel(
            "[bold]Голосовое управление (STT):[/bold]\n"
            "/voice listen  — Распознать речь и передать учителю\n"
            "/voice status  — Проверить статус микрофона и STT\n\n"
            "[dim]Требуется микрофон и SpeechRecognition для реальной работы.[/dim]",
            border_style="yellow",
        ))
        return "", True
    else:
        console.print(f"[red]Неизвестная подкоманда: {subcommand}[/red]")
        return "", True
