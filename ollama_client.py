"""
Обертка для Ollama через subprocess + curl
Исправлена кодировка (UTF-8) и работа с промптами
"""
import subprocess
import json
import logging
import os
import tempfile
from typing import Any, List, Generator

logger = logging.getLogger(__name__)

class OllamaClient:
    """Клиент для Ollama через curl, оптимизированный для Windows"""
    
    def __init__(self, model: str = "qwen2.5:7b", temperature: float = 0.3):
        self.model = model
        self.temperature = temperature
        self.streaming_mode = True
        self.max_tokens = 512

    def stream(self, prompt: str) -> Generator[Any, None, None]:
        """Эмуляция потоковой передачи для совместимости с интерфейсом"""
        response = self.invoke(prompt)
        # Разбиваем на слова для эффекта печати
        for word in response.split(' '):
            yield type('obj', (object,), {'content': word + ' '})()

    def invoke(self, prompt: str) -> str:
        """Отправить запрос к Ollama через временный файл и curl"""
        # Формируем структуру запроса. 
        # Мы не добавляем системный промпт здесь, так как main.py передает его в prompt
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self.temperature,
            "stream": False
        }
        
        # Используем контекстный менеджер для временного файла
        fd, path = tempfile.mkstemp(suffix='.json', text=True)
        try:
            with os.fdopen(fd, 'w', encoding='utf-8') as tmp:
                json.dump(data, tmp, ensure_ascii=False)
            
            # Вызываем curl. Важно: используем -d @путь для передачи файла
            cmd = [
                'curl', '-s', 
                '-X', 'POST', 
                'http://localhost:11434/v1/chat/completions',
                '-H', 'Content-Type: application/json',
                '-d', f'@{path}'
            ]
            
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                encoding='utf-8', # Фикс кракозябр
                errors='ignore',
                timeout=120
            )
            
            if result.returncode != 0:
                return f"Ошибка выполнения curl: {result.stderr}"
            
            if not result.stdout.strip():
                return "Ошибка: Ollama вернула пустой ответ"
                
            resp_json = json.loads(result.stdout)
            
            if 'error' in resp_json:
                return f"Ошибка Ollama: {resp_json['error'].get('message', 'Unknown error')}"
                
            return resp_json['choices'][0]['message']['content']
            
        except subprocess.TimeoutExpired:
            return "Ошибка: Превышено время ожидания ответа от модели"
        except json.JSONDecodeError:
            return f"Ошибка парсинга ответа: {result.stdout[:200]}"
        except Exception as e:
            return f"Критическая ошибка клиента: {e}"
        finally:
            if os.path.exists(path):
                os.remove(path)

    def chat(self, prompt: str) -> str:
        return self.invoke(prompt)

    def __call__(self, prompt: str) -> str:
        return self.invoke(prompt)
