"""
🔊 Voice Assistant (M-34)

Provides text-to-speech (TTS) and speech-to-text (STT) capabilities.
Currently supports TTS using pyttsx3 (cross-platform, offline).
"""

import logging
import random
from typing import Any

from rich.console import Console
from rich.panel import Panel

from di import get_context

logger = logging.getLogger(__name__)
console = Console()

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


def handle_voice(action: str, args: str = "") -> tuple[bool, str, Any]:
    """Handle voice commands: /voice on/off/test."""
    ctx = get_context()
    state = ctx.state

    if action == "voice on":
        state.voice_enabled = True
        return True, "🔊 Voice output enabled. Responses will be read aloud.", None

    elif action == "voice off":
        state.voice_enabled = False
        return True, "🔇 Voice output disabled.", None

    elif action == "voice test":
        if not _speak("Это тест голосового помощника CyberTeacher."):
            return (
                False,
                "❌ TTS engine not available. Check pyttsx3 installation.",
                None,
            )
        return True, "✅ TTS test complete. You should have heard a message.", None

    elif action == "voice status":
        status = "enabled" if state.voice_enabled else "disabled"
        stt_status = "✅ STT доступен" if STT_AVAILABLE else "⚠️ STT симуляция"
        return (
            True,
            f"🔊 Voice status: {status}. Engine: {state.voice_engine}, Rate: {state.voice_rate} wpm\n{stt_status}",
            None,
        )

    elif action == "voice listen":
        return _handle_voice_listen()

    else:
        return False, "Usage: /voice on, /voice off, /voice test, /voice status", None


# Initialize pyttsx3 engine lazily
_engine = None


def _get_tts_engine():
    """Get or initialize the TTS engine."""
    global _engine
    if _engine is not None:
        return _engine

    try:
        import pyttsx3

        engine = pyttsx3.init()
        engine.setProperty("rate", get_context().state.voice_rate)
        # Optionally set voice based on language
        voices = engine.getProperty("voices")
        # Try to find a Russian voice if available
        for voice in voices:
            if "russian" in voice.languages[0].lower() if voice.languages else False:
                engine.setProperty("voice", voice.id)
                break
        _engine = engine
        return _engine
    except Exception as e:
        logger.error(f"Failed to initialize TTS engine: {e}")
        return None


def _speak(text: str) -> bool:
    """Speak the given text using TTS.

    Args:
        text: Text to speak.

    Returns:
        True if spoken successfully, False otherwise.
    """
    ctx = get_context()
    state = ctx.state
    if not state.voice_enabled:
        return False

    engine = _get_tts_engine()
    if engine is None:
        return False

    try:
        # Interrupt any ongoing speech
        engine.stop()
        engine.say(text)
        engine.runAndWait()
        return True
    except RuntimeError:
        # Workaround: if runAndWait called recursively, ignore
        logger.debug("TTS busy, skipping speech")
        return False
    except Exception as e:
        logger.error(f"TTS error: {e}")
        return False


def speak_if_enabled(text: str):
    """Speak text if voice output is enabled. Non-blocking convenience wrapper."""
    if not get_context().state.voice_enabled:
        return
    _speak(text)


def _handle_voice_listen() -> tuple[bool, str, Any]:
    """Listen for voice input using STT or simulate."""
    if STT_AVAILABLE:
        try:
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                console.print("[bold cyan]🎤 Говорите... (5 сек)[/bold cyan]")
                audio = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio, language="ru-RU")
                console.print(Panel(f"[bold]Распознано:[/bold] {text}", border_style="green"))
                return True, text, None
        except Exception as e:
            logger.warning(f"STT error: {e}")

    # Симуляция
    text = random.choice(SIMULATED_PHRASES)
    console.print(Panel(f"[bold]Симуляция STT:[/bold] {text}", border_style="yellow"))
    console.print("[dim]Для реального STT: pip install SpeechRecognition pyaudio[/dim]")
    return True, text, None
