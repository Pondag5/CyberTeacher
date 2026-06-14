"""ResilientLLM — Provider Fallback Chain with retry and circuit breaker.

Usage:
    from resilient_llm import ResilientLLM
    llm = ResilientLLM(primary=ollama_llm, fallbacks=[groq_llm, openrouter_llm])
    response = llm.invoke("Hello")
"""

import logging
import time
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

DEFAULT_MAX_RETRIES = 2
DEFAULT_CIRCUIT_BREAKER_THRESHOLD = 3
DEFAULT_CIRCUIT_BREAKER_COOLDOWN = 60  # seconds
DEFAULT_TIMEOUT = 30  # seconds


class CircuitState:
    """Tracks circuit breaker state per provider."""

    CLOSED = "closed"  # Normal — requests pass through
    OPEN = "open"  # Failing — skip this provider
    HALF_OPEN = "half_open"  # Testing — allow one request

    def __init__(self):
        self.state = self.CLOSED
        self.failure_count = 0
        self.last_failure_time = 0.0
        self.last_error: Optional[str] = None

    def record_failure(
        self, threshold: int = DEFAULT_CIRCUIT_BREAKER_THRESHOLD, error: Optional[str] = None
    ) -> None:
        self.failure_count += 1
        self.last_failure_time = time.time()
        self.last_error = error
        if self.failure_count >= threshold:
            self.state = self.OPEN
            logger.warning(f"Circuit breaker OPEN after {self.failure_count} failures: {error}")

    def record_success(self) -> None:
        self.state = self.CLOSED
        self.failure_count = 0
        self.last_error = None

    def should_skip(self, cooldown: float = DEFAULT_CIRCUIT_BREAKER_COOLDOWN) -> bool:
        if self.state == self.CLOSED:
            return False
        if self.state == self.OPEN:
            if time.time() - self.last_failure_time > cooldown:
                self.state = self.HALF_OPEN
                return False
            return True
        return False


class ResilientLLM:
    """LLM wrapper with retry logic, circuit breaker, and provider fallback.

    Wraps a primary LLM and optional fallback LLMs. If the primary fails,
    tries fallbacks in order. Each provider has its own circuit breaker.
    """

    def __init__(
        self,
        primary: Any,
        fallbacks: Optional[List[Any]] = None,
        max_retries: int = DEFAULT_MAX_RETRIES,
        circuit_breaker_threshold: int = DEFAULT_CIRCUIT_BREAKER_THRESHOLD,
        circuit_breaker_cooldown: float = DEFAULT_CIRCUIT_BREAKER_COOLDOWN,
        timeout: float = DEFAULT_TIMEOUT,
        provider_names: Optional[Dict[int, str]] = None,
    ):
        self.llm = primary
        self._primary = primary
        self._fallbacks = fallbacks or []
        self._max_retries = max_retries
        self._cb_threshold = circuit_breaker_threshold
        self._cb_cooldown = circuit_breaker_cooldown
        self._timeout = timeout
        self._circuits: Dict[int, CircuitState] = {}
        self._provider_names: Dict[int, str] = provider_names or {}
        self._current_provider = primary
        self._provider_type: Dict[int, str] = {}  # e.g. "ollama", "groq"
        self._provider_model: Dict[int, str] = {}  # actual model name

        for i, llm in enumerate([primary] + self._fallbacks):
            self._circuits[id(llm)] = CircuitState()
            if id(llm) not in self._provider_names:
                name = getattr(llm, "model", f"provider_{i}")
                self._provider_names[id(llm)] = str(name)
            self._provider_type[id(llm)] = getattr(llm, "model", f"provider_{i}").split("/")[0] if "/" in str(getattr(llm, "model", "")) else str(getattr(llm, "model", f"provider_{i}"))
            self._provider_model[id(llm)] = str(getattr(llm, "model", "unknown"))

    def _try_invoke(self, llm: Any, prompt: str) -> Any:
        """Try to invoke an LLM, raising on failure."""
        import signal
        from functools import partial

        class TimeoutError(Exception):
            pass

        def _timeout_handler(signum, frame):
            raise TimeoutError(f"Provider timed out after {self._timeout}s")

        # Set timeout using signal (Unix) or fallback
        if hasattr(signal, "SIGALRM"):
            old_handler = signal.signal(signal.SIGALRM, _timeout_handler)
            signal.alarm(int(self._timeout))
            try:
                result = llm.invoke(prompt)
                return result
            finally:
                signal.alarm(0)
                signal.signal(signal.SIGALRM, old_handler)
        else:
            # Windows fallback: use a threading timer
            import threading

            result_container = []
            error_container = []

            def _invoke_target():
                try:
                    result = llm.invoke(prompt)
                    result_container.append(result)
                except Exception as e:
                    error_container.append(e)

            thread = threading.Thread(target=_invoke_target, daemon=True)
            thread.start()
            thread.join(timeout=self._timeout)
            if thread.is_alive():
                raise TimeoutError(f"Provider timed out after {self._timeout}s")
            if error_container:
                raise error_container[0]
            if result_container:
                return result_container[0]
            raise RuntimeError("No result from provider")

    def _try_stream(self, llm: Any, prompt: str):
        """Try to stream from an LLM, raising on failure."""
        if hasattr(llm, "stream"):
            gen = llm.stream(prompt)
            first = True
            for chunk in gen:
                if first:
                    first = False
                    yield chunk
                else:
                    yield chunk
        else:
            result = llm.invoke(prompt)
            if hasattr(result, "content"):
                yield result.content
            else:
                yield str(result)

    def _get_provider_chain(self) -> List[Any]:
        """Return ordered list of providers, skipping circuits that are open."""
        chain = []
        for llm in [self._primary] + self._fallbacks:
            circuit = self._circuits.get(id(llm))
            if circuit and not circuit.should_skip(self._cb_cooldown):
                chain.append(llm)
        return chain

    def invoke(self, prompt: str) -> Any:
        """Invoke with fallback chain. Tries primary first, then fallbacks."""
        chain = self._get_provider_chain()
        last_error = None

        for llm in chain:
            circuit = self._circuits[id(llm)]
            name = self._provider_names.get(id(llm), "unknown")

            for attempt in range(self._max_retries + 1):
                try:
                    result = self._try_invoke(llm, prompt)
                    circuit.record_success()
                    if llm is not self._primary:
                        logger.info(f"Fallback to {name} succeeded")
                    self._current_provider = llm
                    return result
                except Exception as e:
                    last_error = e
                    if attempt < self._max_retries:
                        wait = 0.5 * (attempt + 1)
                        logger.debug(
                            f"Retry {attempt + 1}/{self._max_retries} for {name} in {wait}s"
                        )
                        time.sleep(wait)
                    else:
                        circuit.record_failure(self._cb_threshold, error=str(e))
                        logger.warning(
                            f"Provider {name} failed after {self._max_retries + 1} attempts: {e}"
                        )

        raise (
            RuntimeError(f"All LLM providers failed. Last error: {last_error}")
            if last_error
            else RuntimeError("No LLM providers available")
        )

    def stream(self, prompt: str):
        """Stream with fallback chain."""
        chain = self._get_provider_chain()
        last_error = None

        for llm in chain:
            circuit = self._circuits[id(llm)]
            name = self._provider_names.get(id(llm), "unknown")

            try:
                gen = self._try_stream(llm, prompt)
                for chunk in gen:
                    circuit.record_success()
                    if llm is not self._primary:
                        logger.info(f"Fallback to {name} succeeded (streaming)")
                    self._current_provider = llm
                    yield chunk
                    for remaining in gen:
                        yield remaining
                    return
            except Exception as e:
                last_error = e
                circuit.record_failure(self._cb_threshold, error=str(e))
                logger.warning(f"Provider {name} streaming failed: {e}")

        raise (
            RuntimeError(
                f"All LLM providers failed (streaming). Last error: {last_error}"
            )
            if last_error
            else RuntimeError("No LLM providers available")
        )

    @staticmethod
    def test_provider(provider_name: str, llm_instance: Any, timeout: int = 15) -> Tuple[bool, str]:
        """Test a specific provider with a simple ping prompt.
        
        Returns (success: bool, message: str).
        """
        test_prompt = "Respond with exactly one word: ping"
        import threading

        result = []
        error = []

        def _test():
            try:
                resp = llm_instance.invoke(test_prompt)
                content = resp.content if hasattr(resp, "content") else str(resp)
                result.append(content.strip().lower()[:20])
            except Exception as e:
                error.append(str(e))

        thread = threading.Thread(target=_test, daemon=True)
        thread.start()
        thread.join(timeout=timeout)

        if thread.is_alive():
            return False, f"Timeout ({timeout}s) — provider {provider_name} not responding"
        if error:
            return False, f"Error: {error[0][:100]}"
        if result:
            return True, f"OK (response: '{result[0]}')"
        return False, "No response"

    def get_status(self) -> Dict[str, Any]:
        """Return detailed status of all providers in the chain."""
        providers = []
        for i, llm in enumerate([self._primary] + self._fallbacks):
            circuit = self._circuits.get(id(llm))
            name = self._provider_names.get(id(llm), "unknown")
            ptype = self._provider_type.get(id(llm), "unknown")
            pmodel = self._provider_model.get(id(llm), "unknown")
            if circuit:
                providers.append({
                    "name": name,
                    "type": ptype,
                    "model": pmodel,
                    "role": "primary" if i == 0 else "fallback",
                    "circuit_state": circuit.state,
                    "failures": circuit.failure_count,
                    "last_error": circuit.last_error,
                    "is_current": llm is self._current_provider,
                })
        return {
            "providers": providers,
            "active_provider": getattr(self._current_provider, "model", "unknown") if self._current_provider else "none",
            "timeout": self._timeout,
        }

    def get_provider_name(self, llm: Any) -> str:
        """Get the human-readable provider name for an LLM instance."""
        return self._provider_names.get(id(llm), "unknown")

    @property
    def model(self) -> str:
        """Backward-compatible model attribute."""
        return getattr(self._primary, "model", "resilient")
