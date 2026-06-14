"""Shared types for command handlers."""

from __future__ import annotations
from typing import Any, NamedTuple


class HandlerResult(NamedTuple):
    """Standard return type for all command handlers.

    Attributes:
        success: Whether the command succeeded.
        data: Response data (message, dict, etc.) or None.
        error: Error message or None.
        continue_session: Whether the session should continue.
    """

    success: bool
    data: Any
    error: str | None
    continue_session: bool
