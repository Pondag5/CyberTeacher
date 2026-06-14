"""
Persona (mode) management.
"""

from pydantic import BaseModel, Field


class PersonaState(BaseModel):
    """Current persona (mode) of the assistant."""
    
    current_persona: str = Field(default="teacher")
    current_mode: str = Field(default="teacher")

    model_config = {"validate_assignment": True}