"""
Explanation depth state management.
"""

from pydantic import BaseModel, Field


class ExplanationState(BaseModel):
    """Explanation depth configuration."""

    explanation_depth: str = Field(default="normal")  # beginner, normal, expert

    def set_explanation_depth(self, depth: str) -> str:
        """Set explanation depth: beginner, normal, expert."""
        if depth in ("beginner", "normal", "expert"):
            self.explanation_depth = depth
        return self.explanation_depth

    def get_explanation_depth(self) -> str:
        """Get current explanation depth."""
        return self.explanation_depth

    model_config = {"validate_assignment": True}
