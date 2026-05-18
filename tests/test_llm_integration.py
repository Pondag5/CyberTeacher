"""
Интеграционные тесты LLM (LLM Integration Tests).

Проверяют реальное взаимодействие с LLM провайдером (Groq).
Тесты пропускаются, если API ключ не настроен.
"""

import os
import unittest

from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Проверяем наличие ключа
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")

# Пропускаем тесты, если не используется Groq или нет ключа
skip_llm_tests = unittest.skipIf(
    LLM_PROVIDER != "groq" or not GROQ_API_KEY,
    "LLM Integration tests require LLM_PROVIDER=groq and GROQ_API_KEY to be set"
)


@skip_llm_tests
class TestLLMIntegration(unittest.TestCase):
    """Тесты реального вызова LLM."""

    def test_llm_initialization(self):
        """Тест: LLM успешно инициализируется через LazyLoader."""
        from config import LazyLoader
        
        # Сбрасываем кэш, чтобы получить свежий экземпляр
        LazyLoader._llm = None
        
        llm = LazyLoader.get_llm()
        
        self.assertIsNotNone(llm)
        # Проверяем, что это объект ChatGroq (или аналогичный)
        self.assertTrue(hasattr(llm, "invoke"))

    def test_llm_simple_invoke(self):
        """Тест: LLM отвечает на простой вопрос."""
        from config import LazyLoader
        
        LazyLoader._llm = None
        llm = LazyLoader.get_llm()
        
        response = llm.invoke("Скажи только слово: ТЕСТ")
        
        self.assertIsNotNone(response)
        # Получаем текст ответа
        content = response.content if hasattr(response, 'content') else str(response)
        self.assertIn("ТЕСТ", content.upper())

    def test_llm_cybersecurity_knowledge(self):
        """Тест: LLM знает базовые понятия кибербезопасности."""
        from config import LazyLoader
        
        LazyLoader._llm = None
        llm = LazyLoader.get_llm()
        
        prompt = (
            "Что такое XSS? Ответь одним предложением. "
            "Если не знаешь, скажи 'НЕ ЗНАЮ'."
        )
        response = llm.invoke(prompt)
        
        content = response.content if hasattr(response, 'content') else str(response)
        content_lower = content.lower()
        
        # Проверяем, что ответ содержит ключевые слова или хотя бы не пустой
        self.assertTrue(len(content) > 10)
        # XSS обычно связан с скриптами или сайтами
        self.assertTrue(
            "скрипт" in content_lower or
            "сайт" in content_lower or
            "код" in content_lower or
            "xss" in content_lower
        )

    def test_llm_json_generation(self):
        """Тест: LLM может генерировать валидный JSON."""
        import json
        import re

        from config import LazyLoader
        
        LazyLoader._llm = None
        llm = LazyLoader.get_llm()
        
        prompt = (
            "Верни JSON объект с полями 'name' (строка) и 'age' (число). "
            "Никакого текста, только JSON. Пример: {\"name\": \"Ivan\", \"age\": 25}"
        )
        response = llm.invoke(prompt)
        
        content = response.content if hasattr(response, 'content') else str(response)
        
        # Пытаемся найти JSON в ответе
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        self.assertIsNotNone(json_match, "LLM didn't return JSON")
        
        try:
            data = json.loads(json_match.group())
            self.assertIn("name", data)
            self.assertIn("age", data)
        except json.JSONDecodeError:
            self.fail("LLM returned invalid JSON")


if __name__ == "__main__":
    unittest.main()
