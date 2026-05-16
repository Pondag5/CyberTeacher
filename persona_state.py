"""
Persona (mode) management.
"""

from pydantic import BaseModel, Field


class PersonaState(BaseModel):
    """Current persona (mode) of the assistant."""
    
    current_persona: str = Field(default="teacher")  # teacher, expert, ctf, review
    current_mode: str = Field(default="teacher")  # режим для совместимости

    model_config = {
        "validate_assignment": True
    }