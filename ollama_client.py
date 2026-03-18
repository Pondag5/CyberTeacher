"""
Обертка для Ollama через subprocess + curl
Исправлена кодировка (UTF-8) и работа с промптами
"""

import json
import logging
import os
import subprocess
import tempfile
from collections.abc import Generator
from typing import Any, List

logger = logging.getLogger(__name__)


class OllamaClient:
    """Клиент для Ollama через curl, оптимизированный для Windows"""

    def __init__(
        self, model: str = "qwen2.5:7b", temperature: float = 0.3, cache_size: int = 100
    ):
        """
        Args:
            model: Имя модели Ollama
            temperature: Температура генерации (0.0-1.0)
            cache_size: Размер кэша в памяти (количество промптов)
        """
        self.model = model
        self.temperature = temperature
        self.streaming_mode = True
        self.max_tokens = 512
        self._cache = {}
        self._cache_size = cache_size

    def stream(self, prompt: str) -> Generator[Any, None, None]:
        """Эмуляция потоковой передачи для совместимости с интерфейсом"""
        response = self.invoke(prompt)
        # Разбиваем на слова для эффекта печати
        for word in response.split(" "):
            yield type("obj", (object,), {"content": word + " "})()

    def invoke(self, prompt: str) -> str:
        """
        Отправить запрос к Ollama с кэшированием.

        Args:
            prompt: Текст запроса пользователя (с системным промптом уже включен)

        Returns:
            Ответ модели или сообщение об ошибке
        """
        if not prompt or not prompt.strip():
            return "Ошибка: пустой промпт"

        prompt = prompt[:8000]  # Ограничиваем длину промпта

        import hashlib

        cache_key = hashlib.md5(prompt.encode("utf-8")).hexdigest()
        if cache_key in self._cache:
            return self._cache[cache_key]

        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self.temperature,
            "stream": False,
        }

        fd, path = tempfile.mkstemp(suffix=".json", text=True)
        response_text = None
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as tmp:
                json.dump(data, tmp, ensure_ascii=False)

            cmd = [
                "curl",
                "-s",
                "-X",
                "POST",
                "http://localhost:11434/v1/chat/completions",
                "-H",
                "Content-Type: application/json",
                "-d",
                f"@{path}",
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="ignore",
                timeout=120,
            )

            if result.returncode != 0:
                response_text = f"Ошибка curl: {result.stderr}"
            elif not result.stdout.strip():
                response_text = "Ошибка: пустой ответ от Ollama"
            else:
                resp_json = json.loads(result.stdout)
                if "error" in resp_json:
                    response_text = f"Ошибка Ollama: {resp_json['error'].get('message', 'Unknown error')}"
                else:
                    response_text = resp_json["choices"][0]["message"]["content"]

        except subprocess.TimeoutExpired:
            response_text = "Ошибка: таймаут"
        except json.JSONDecodeError:
            response_text = f"Ошибка парсинга JSON"
        except Exception as e:
            response_text = f"Ошибка: {e}"
        finally:
            if os.path.exists(path):
                os.remove(path)

        # Кэшируем только успешные ответы
        if response_text and not response_text.startswith("Ошибка"):
            self._cache[cache_key] = response_text
            if len(self._cache) > self._cache_size:
                self._cache.pop(next(iter(self._cache)))

        return response_text or "Ошибка: пустой ответ"

    def chat(self, prompt: str) -> str:
        return self.invoke(prompt)

    def __call__(self, prompt: str) -> str:
        return self.invoke(prompt)
