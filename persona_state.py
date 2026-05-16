"""
Persona (mode) management.
"""

from dataclasses import dataclass


@dataclass
class PersonaState:
    """Current persona (mode) of the assistant."""
    
    current_persona: str = "teacher"  # teacher, expert, ctf, review
    current_mode: str = "teacher"  # режим для совместимости