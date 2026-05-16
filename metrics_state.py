"""
Performance metrics and statistics.
"""

import time
from typing import Dict, Any, List
from pydantic import BaseModel, Field, validator


class MetricsState(BaseModel):
    """Performance metrics and statistics."""

    # Метрики (Q-04)
    llm_call_count: int = Field(default=0, ge=0)
    llm_total_time: float = Field(default=0.0, ge=0.0)
    llm_total_tokens: int = Field(default=0, ge=0)
    cache_hits: int = Field(default=0, ge=0)
    cache_misses: int = Field(default=0, ge=0)
    start_time: float = Field(default_factory=time.time)

    # Rate limiting timestamps (Q-05) - переместим сюда из user_state для логической группировки с метриками
    request_timestamps: List[float] = Field(default_factory=list)

    # Статистика использования команд (M-31)
    command_usage: Dict[str, int] = Field(default_factory=dict)

    def can_make_request(
        self, window_seconds: int = 60, max_requests: int = 10
    ) -> bool:
        """Check if a new request is allowed within the rate limit."""
        now = time.time()
        self.request_timestamps = [
            ts for ts in self.request_timestamps if now - ts < window_seconds
        ]
        return len(self.request_timestamps) < max_requests

    def record_request(self) -> None:
        """Record that a request was made."""
        self.request_timestamps.append(time.time())

    def track_command_usage(self, command: str) -> None:
        """Отслеживать использование команды (M-31)."""
        self.command_usage[command] = self.command_usage.get(command, 0) + 1

    model_config = {"validate_assignment": True}
