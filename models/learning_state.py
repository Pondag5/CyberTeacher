"""
Learning progress and course management.
"""

from typing import Any

from pydantic import BaseModel, Field


class LearningState(BaseModel):
    """Learning progress and course data."""

    current_course: str | None = None
    current_topic: int = Field(default=0, ge=0)
    course_progress: dict[str, int] = Field(default_factory=dict)
    learning_context: dict[str, Any] = Field(
        default_factory=lambda: {
            "current_course": None,
            "current_topic": None,
            "current_lab": None,
            "last_action": None,
        }
    )

    def set_learning_context(
        self,
        course: Any = None,
        topic: Any = None,
        lab: Any = None,
        action: Any = None
    ) -> None:
        if course is not None:
            self.learning_context["current_course"] = course
        if topic is not None:
            self.learning_context["current_topic"] = topic
        if lab is not None:
            self.learning_context["current_lab"] = lab
        if action is not None:
            self.learning_context["last_action"] = action

    def get_learning_context(self) -> dict[str, Any]:
        return self.learning_context

    def reset_course(self) -> None:
        self.current_course = None
        self.current_topic = 0

    def set_course(self, course_id: str) -> None:
        self.current_course = course_id
        self.current_topic = 0

    def next_topic(self) -> None:
        self.current_topic += 1

    model_config = {"validate_assignment": True}