"""
Performance metrics and statistics.
"""

import time
from typing import Any

from pydantic import BaseModel, Field


class MetricsState(BaseModel):
    """Performance metrics and statistics."""

    # LLM metrics
    llm_call_count: int = Field(default=0, ge=0)
    llm_total_time: float = Field(default=0.0, ge=0.0)
    llm_total_tokens: int = Field(default=0, ge=0)

    # Cache metrics
    cache_hits: int = Field(default=0, ge=0)
    cache_misses: int = Field(default=0, ge=0)

    # Session
    start_time: float = Field(default_factory=time.time)

    # Rate limiting
    request_timestamps: list[float] = Field(default_factory=list)

    # Command usage
    command_usage: dict[str, int] = Field(default_factory=dict)

    def can_make_request(self, window_seconds: int = 60, max_requests: int = 10) -> bool:
        now = time.time()
        self.request_timestamps = [ts for ts in self.request_timestamps if now - ts < window_seconds]
        return len(self.request_timestamps) < max_requests

    def record_request(self) -> None:
        self.request_timestamps.append(time.time())

    def track_command_usage(self, command: str) -> None:
        self.command_usage[command] = self.command_usage.get(command, 0) + 1

    model_config = {"validate_assignment": True}