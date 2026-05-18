"""
Voice assistant state management.
"""

from pydantic import BaseModel, Field


class VoiceState(BaseModel):
    """Voice assistant configuration."""
    
    voice_enabled: bool = Field(default=False)  # TTS for responses
    voice_engine: str = Field(default="pyttsx3")  # TTS engine
    voice_rate: int = Field(default=200, gt=0)  # words per minute (for pyttsx3)

    model_config = {
        "validate_assignment": True
    }
