"""
Learning progress and course management.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class LearningState:
    """Learning progress and course data."""
    
    # Курс
    current_course: Optional[str] = None
    current_topic: int = 0

    # Для курсов
    course_progress: Dict[str, int] = field(default_factory=dict)

    # Контекст обучения
    learning_context: Dict[str, Any] = field(
        default_factory=lambda: {
            "current_course": None,
            "current_topic": None,
            "current_lab": None,
            "last_action": None,
        }
    )

    def set_learning_context(self, course=None, topic=None, lab=None, action=None):
        """Установить контекст обучения"""
        if course:
            self.learning_context["current_course"] = course
        if topic:
            self.learning_context["current_topic"] = topic
        if lab:
            self.learning_context["current_lab"] = lab
        if action:
            self.learning_context["last_action"] = action

    def get_learning_context(self) -> Dict[str, Any]:
        """Получить контекст обучения"""
        return self.learning_context

    def reset_course(self):
        """Сбросить прогресс курса"""
        self.current_course = None
        self.current_topic = 0

    def set_course(self, course_id: str):
        """Установить текущий курс"""
        self.current_course = course_id
        self.current_topic = 0

    def next_topic(self):
        """Следующая тема"""
        self.current_topic += 1