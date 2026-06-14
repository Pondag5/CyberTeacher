"""MockLLM — offline fallback when no LLM provider is available.

Provides template-based responses so the application works "out of the box"
without any API keys or GPU. Every command responds with a helpful message
explaining how to set up a real LLM.
"""

import logging
from typing import Any, Iterator

logger = logging.getLogger(__name__)

MOCK_RESPONSES = {
    "default": (
        "[MockLLM] Учитель сейчас в офлайн-режиме. "
        "Для живого AI установите Ollama или введите API-ключ.\n\n"
        "Команда /doctor покажет статус подключения LLM."
    ),
    "quiz": (
        "[MockLLM] Генерация квизов требует LLM.\n"
        "Установите Ollama: `ollama pull qwen2.5:7b`\n"
        "Или введите ключ Groq: `/set-api-key groq YOUR_KEY`"
    ),
    "hint": "[MockLLM] Подсказки недоступны в оффлайн-режиме.",
    "explanation": (
        "[MockLLM] Объяснения требуют LLM. "
        "Используйте `/doctor` для настройки AI-провайдера."
    ),
}


class MockLLM:
    """LLM stub that returns helpful offline messages.

    Works without API keys, GPU, or network. Every method returns
    a template response directing the user to set up a real provider.
    """

    model = "mock-llm"
    provider = "mock"

    def invoke(self, prompt: str) -> Any:
        """Return a mock response. Never fails."""

        class MockResponse:
            def __init__(self, content: str):
                self.content = content

        # Detect intent from prompt keywords
        lower = prompt.lower()
        if any(w in lower for w in ["квиз", "quiz", "вопрос", "question"]):
            text = MOCK_RESPONSES["quiz"]
        elif any(w in lower for w in ["подсказк", "hint", "помоги"]):
            text = MOCK_RESPONSES["hint"]
        elif any(w in lower for w in ["объясни", "explain", "почему", "что такое"]):
            text = MOCK_RESPONSES["explanation"]
        else:
            text = MOCK_RESPONSES["default"]

        logger.debug("MockLLM invoked — returning offline message")
        return MockResponse(text)

    def stream(self, prompt: str) -> Iterator[str]:
        """Yield a mock response chunk. Never fails."""
        response = self.invoke(prompt)
        yield response.content

    def __repr__(self) -> str:
        return "MockLLM(offline)"
