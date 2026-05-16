"""
Shared types and enums to eliminate circular imports
"""

from enum import Enum


class Mode(Enum):
    """Application modes for different interaction styles"""

    TEACHER = "Учитель"
    EXPERT = "Эксперт"
    CTF = "CTF"
    CODE_REVIEW = "Анализ кода"
    QUIZ = "Викторина"
