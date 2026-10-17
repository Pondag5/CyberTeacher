# context_budget.py — Context Budget Manager v2
# Token-aware context trimming for LLM calls.
# Uses character-ratio estimation (~4 chars per token) to stay dependency-free.
from typing import Any, Dict, List, Optional, Tuple

CHARS_PER_TOKEN = 4
DEFAULT_MAX_TOKENS = 8000
DEFAULT_SYSTEM_PROMPT_TOKENS = 1500
DEFAULT_RAG_CONTEXT_TOKENS = 2000
DEFAULT_RESPONSE_RESERVE = 1024
DEFAULT_MAX_HISTORY_MESSAGES = 30


class ContextBudgetManager:
    """Manages context budget for LLM calls.

    Budget allocation:
        total_window = system_prompt + rag_context + history + user_input + response_reserve
        history_budget = total_window - system_prompt - rag_context - user_input - response_reserve

    Persistence: use to_dict() / from_dict() to save/restore across sessions.
    """

    def __init__(
        self,
        max_tokens: int = DEFAULT_MAX_TOKENS,
        system_prompt_tokens: int = DEFAULT_SYSTEM_PROMPT_TOKENS,
        rag_context_tokens: int = DEFAULT_RAG_CONTEXT_TOKENS,
        response_reserve: int = DEFAULT_RESPONSE_RESERVE,
    ):
        self.max_tokens = max_tokens
        self.system_prompt_tokens = system_prompt_tokens
        self.rag_context_tokens = rag_context_tokens
        self.response_reserve = response_reserve
        self._total_chars_sent = 0
        self._call_count = 0
        self._trim_count = 0
        self._peak_used_tokens: int = 0
        self._overflow_count: int = 0

    def _estimate_tokens(self, text: str) -> int:
        """Estimate token count from text using character-ratio."""
        return max(1, len(text) // CHARS_PER_TOKEN)

    def _estimate_message_tokens(self, message: Dict[str, str]) -> int:
        """Estimate tokens for a single message including role prefix."""
        role_overhead = 4  # "user: " or "assistant: "
        return role_overhead + self._estimate_tokens(message.get("content", ""))

    def _estimate_total_tokens(self, messages: List[Dict[str, str]]) -> int:
        """Estimate total tokens for a list of messages."""
        return sum(self._estimate_message_tokens(m) for m in messages)

    def get_history_budget(
        self,
        rag_context_tokens: Optional[int] = None,
        user_input: str = "",
    ) -> int:
        """Calculate how many tokens are available for chat history.

        Returns: maximum tokens available for history messages.
        """
        user_input_tokens = self._estimate_tokens(user_input)
        rag = (
            rag_context_tokens
            if rag_context_tokens is not None
            else self.rag_context_tokens
        )
        budget = (
            self.max_tokens
            - self.system_prompt_tokens
            - rag
            - user_input_tokens
            - self.response_reserve
        )
        return max(512, budget)  # minimum 512 tokens for history

    def prepare_context(
        self,
        messages: List[Dict[str, str]],
        max_messages: int = DEFAULT_MAX_HISTORY_MESSAGES,
        user_input: str = "",
        rag_context_tokens: Optional[int] = None,
    ) -> Tuple[List[Dict[str, str]], str]:
        """Trim messages to fit within the context budget.

        Returns:
            (trimmed_messages, warning_message)
        """
        self._call_count += 1
        if not messages:
            return messages, ""

        history_budget = self.get_history_budget(
            rag_context_tokens=rag_context_tokens,
            user_input=user_input,
        )
        total_tokens = self._estimate_total_tokens(messages)

        # If fits within budget and message count, return as-is
        if total_tokens <= history_budget and len(messages) <= max_messages:
            return messages, ""

        # Strategy: keep the most recent messages that fit within budget
        # Always include the last message for continuity
        kept: List[Dict[str, str]] = []
        used_tokens = 0

        # Walk from the end (newest) backwards
        for msg in reversed(messages):
            msg_tokens = self._estimate_message_tokens(msg)
            if used_tokens + msg_tokens > history_budget:
                break
            kept.insert(0, msg)
            used_tokens += msg_tokens

            # Also respect message count limit
            if len(kept) >= max_messages:
                break

        # Ensure at least 2 messages (one user + one assistant)
        if len(kept) < 2 and len(messages) >= 2:
            kept = messages[-2:]

        # Track peak usage and overflow
        if used_tokens > self._peak_used_tokens:
            self._peak_used_tokens = used_tokens
        trimmed_count = len(messages) - len(kept)
        if trimmed_count > 0:
            self._trim_count += 1
            self._overflow_count += 1
            budget_used_pct = int(used_tokens / history_budget * 100)
            warning = (
                f"[yellow]✂️ Контекст: {trimmed_count} сообщений обрезано "
                f"({used_tokens}/{history_budget} токенов, ~{budget_used_pct}% бюджета)[/yellow]"
            )
            return kept, warning

        return messages, ""

    def get_stats(self) -> Dict[str, Any]:
        """Return budget manager statistics."""
        return {
            "max_tokens": self.max_tokens,
            "system_prompt_tokens": self.system_prompt_tokens,
            "rag_context_tokens": self.rag_context_tokens,
            "response_reserve": self.response_reserve,
            "history_budget": self.get_history_budget(),
            "total_calls": self._call_count,
            "total_trims": self._trim_count,
            "total_chars_sent": self._total_chars_sent,
            "peak_used_tokens": self._peak_used_tokens,
            "overflow_count": self._overflow_count,
        }

    def to_dict(self) -> Dict[str, Any]:
        """Serialize budget state for persistence."""
        return {
            "max_tokens": self.max_tokens,
            "system_prompt_tokens": self.system_prompt_tokens,
            "rag_context_tokens": self.rag_context_tokens,
            "response_reserve": self.response_reserve,
            "total_chars_sent": self._total_chars_sent,
            "call_count": self._call_count,
            "trim_count": self._trim_count,
            "peak_used_tokens": self._peak_used_tokens,
            "overflow_count": self._overflow_count,
        }

    @classmethod
    def from_dict(cls, data: Optional[Dict[str, Any]]) -> "ContextBudgetManager":
        """Restore budget state from a dict (returned by to_dict())."""
        mgr = cls()
        if not data:
            return mgr
        mgr.max_tokens = data.get("max_tokens", DEFAULT_MAX_TOKENS)
        mgr.system_prompt_tokens = data.get(
            "system_prompt_tokens", DEFAULT_SYSTEM_PROMPT_TOKENS
        )
        mgr.rag_context_tokens = data.get(
            "rag_context_tokens", DEFAULT_RAG_CONTEXT_TOKENS
        )
        mgr.response_reserve = data.get("response_reserve", DEFAULT_RESPONSE_RESERVE)
        mgr._total_chars_sent = data.get("total_chars_sent", 0)
        mgr._call_count = data.get("call_count", 0)
        mgr._trim_count = data.get("trim_count", 0)
        mgr._peak_used_tokens = data.get("peak_used_tokens", 0)
        mgr._overflow_count = data.get("overflow_count", 0)
        return mgr

    def extract_summary(self, messages: List[Dict[str, str]]) -> Optional[str]:
        """Extract the most recent [SUMMARY] message from history."""
        for msg in reversed(messages):
            content = msg.get("content", "")
            if content.startswith("[SUMMARY]"):
                return content.replace("[SUMMARY]", "").strip()
        return None

    def record_usage(self, chars: int) -> None:
        """Record characters sent to LLM for stats tracking."""
        self._total_chars_sent += chars
        self._call_count += 1
