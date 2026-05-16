"""
Explanation depth state management.
"""

from dataclasses import dataclass


@dataclass
class ExplanationState:
    """Explanation depth configuration."""
    
    explanation_depth: str = "normal"  # beginner, normal, expert

    def set_explanation_depth(self, depth: str) -> str:
        """Set explanation depth: beginner, normal, expert."""
        if depth in ("beginner", "normal", "expert"):
            self.explanation_depth = depth
        return self.explanation_depth

    def get_explanation_depth(self) -> str:
        """Get current explanation depth."""
        return self.explanation_depth