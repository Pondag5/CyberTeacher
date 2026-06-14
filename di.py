"""
Dependency Injection container for CyberTeacher.

Replaces global get_state() calls with explicit dependency injection.
Provides AppContext with state, settings, and services.
"""

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, Optional

from settings import Settings, get_settings
from state import AppState, get_state


@dataclass
class AppContext:
    """Central dependency container.

    Holds all application dependencies that handlers need.
    Passed explicitly to handlers instead of using global singletons.
    """

    # Core state
    state: AppState = field(default_factory=get_state)

    # Configuration
    settings: Settings = field(default_factory=get_settings)

    # Database connection (set by main.py)
    db_conn: Any = None

    # LLM instance (lazy-loaded)
    _llm: Any = None

    # Knowledge base (lazy-loaded)
    _knowledge_base: Any = None

    # Context Budget Manager (set by main.py)
    budget_manager: Any = None

    def get_llm(self) -> Any:
        """Get or create LLM instance."""
        if self._llm is None:
            from config import LazyLoader

            self._llm = LazyLoader.get_llm()
        return self._llm

    def get_knowledge_base(self) -> Any:
        """Get or create knowledge base instance."""
        if self._knowledge_base is None:
            try:
                from knowledge import KnowledgeBase  # type: ignore[attr-defined]

                self._knowledge_base = KnowledgeBase()
            except (ImportError, AttributeError):
                self._knowledge_base = None
        return self._knowledge_base

    def save_state(self, force: bool = False) -> None:
        """Save state to file using configured path.
        Also persists ContextBudgetManager stats into state before saving.
        """
        if self.budget_manager is not None:
            try:
                self.state.context_budget = self.budget_manager.to_dict()
            except (AttributeError, ValueError, RuntimeError):
                pass
        self.state.save_to_file(str(self.settings.state_file), force=force)


# Global context instance (for backward compatibility)
_context: AppContext | None = None


def get_context() -> AppContext:
    """Get the global application context.

    During transition, this provides backward compatibility.
    Eventually, context will be passed explicitly to all handlers.
    """
    global _context
    if _context is None:
        _context = AppContext()
    return _context


def set_context(ctx: AppContext) -> None:
    """Set the global application context."""
    global _context
    _context = ctx


def reset_context() -> None:
    """Reset the global context (for testing)."""
    global _context
    _context = None


# ── Decorator for handler injection ─────────────────────────────


def inject(
    handler_func: Callable[..., tuple[bool, Any, Any, bool]],
) -> Callable[..., tuple[bool, Any, Any, bool]]:
    """Decorator that injects AppContext into handlers.

    Usage:
        @inject
        def handle_mycommand(ctx: AppContext, action: str):
            ctx.state.points += 10
            ctx.save_state()

    The decorator wraps the handler to automatically pass the context.
    """

    def wrapper(action: str, *args: Any, **kwargs: Any) -> tuple[bool, Any, Any, bool]:
        ctx = get_context()
        return handler_func(ctx, action, *args, **kwargs)

    # Preserve original function metadata
    wrapper.__name__ = handler_func.__name__
    wrapper.__doc__ = handler_func.__doc__
    return wrapper
