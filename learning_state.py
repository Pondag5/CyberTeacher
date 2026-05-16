"""
Learning progress and course management.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class LearningState(BaseModel):
    """Learning progress and course data."""

    # Курс
    current_course: Optional[str] = None
    current_topic: int = Field(default=0, ge=0)

    # Для курсов
    course_progress: Dict[str, int] = Field(default_factory=dict)

    # Контекст обучения
    learning_context: Dict[str, Any] = Field(
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

    model_config = {"validate_assignment": True}
