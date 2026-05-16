"""
Voice assistant state management.
"""

from dataclasses import dataclass


@dataclass
class VoiceState:
    """Voice assistant configuration."""
    
    voice_enabled: bool = False  # TTS for responses
    voice_engine: str = "pyttsx3"  # TTS engine
    voice_rate: int = 200  # words per minute (for pyttsx3)