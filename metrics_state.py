"""
Performance metrics and statistics.
"""

import time
from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class MetricsState:
    """Performance metrics and statistics."""
    
    # Метрики (Q-04)
    llm_call_count: int = 0
    llm_total_time: float = 0.0
    llm_total_tokens: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    start_time: float = field(default_factory=time.time)
    
    # Rate limiting timestamps (Q-05) - переместим сюда из user_state для логической группировки с метриками
    request_timestamps: list[float] = field(default_factory=list)
    
    # Статистика использования команд (M-31)
    command_usage: dict[str, int] = field(default_factory=dict)
    
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