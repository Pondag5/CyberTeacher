"""
🎯 Генератор практических заданий
Автоматически создаёт CTF-задачи, лаборатории и exercises на основе knowledge base
"""

import random
from datetime import datetime
from typing import Any, Dict, List, Optional

from config import LazyLoader
from knowledge import get_relevant_docs


class AssignmentGenerator:
    """Генератор практических заданий по кибербезопасности"""

    ASSIGNMENT_TYPES = {
        "ctf": {
            "name": "CTF-задача",
            "templates": [
                "Найди флаг в предоставленном файле/контейнере",
                "Взломай веб-приложение и получь флаг",
                "Реши криптозадачу и извлеки секрет",
                "Проанализируй дамп памяти и найди улику",
                "Восстанови повреждённый файл стеганографии",
            ],
            "categories": ["web", "crypto", "forensics", "reverse", "pwn", "stego"],
        },
        "lab": {
            "name": "Лаборатория",
            "templates": [
                "Установи и защити сервис {service}",
                "Настрой firewall для блокировки атаки",
                "Проведи пентест на {target} и составь отчёт",
                "Устрани уязвимости в конфигурации",
                "Автоматизируй сканирование уязвимостей",
            ],
            "categories": ["network", "web", "system", "cloud"],
        },
        "exercise": {
            "name": "Упражнение",
            "templates": [
                "Напиши exploit для {vulnerability}",
                "Создай WAF правило для блокировки {attack}",
                "Настрой IDS/IPS для обнаружения атаки",
                "Реализуй защиту от {threat} в коде",
                "Проведи код-ревью и найди уязвимости",
            ],
            "categories": ["coding", "defense", "detection"],
        },
    }

    def __init__(self):
        self.llm = None
        self._init_llm()

    def _init_llm(self):
        """Lazy load LLM"""
        if self.llm is None:
            self.llm = LazyLoader.get_llm()

    def generate_assignment(
        self,
        topic: str,
        difficulty: str = "intermediate",
        assignment_type: str = "ctf",
        context_docs: list | None = None,
    ) -> dict[str, Any]:
        """
        Генерирует задание на основе темы и контекста.

        Args:
            topic: Тема задания (например, "SQL Injection")
            difficulty: Сложность (beginner, intermediate, advanced)
            assignment_type: Тип задания (ctf, lab, exercise)
            context_docs: Документы из knowledge base для контекста

        Returns:
            Dict с заданием: title, description, flags, hints, solution, resources
        """
        self._init_llm()

        # Получаем контекст из knowledge base если не передан
        if context_docs is None:
            from knowledge import get_knowledge_status

            # Используем поиск по теме
            try:
                vectordb = get_knowledge_status().get("vectordb")
                if vectordb:
                    docs = get_relevant_docs(vectordb, topic, k=5)
                    context_docs = [d.page_content for d in docs]
            except Exception:
                context_docs = []

        context = "\n".join(context_docs[:3]) if context_docs else ""

        # Выбираем шаблон
        template = random.choice(self.ASSIGNMENT_TYPES[assignment_type]["templates"])

        # Генерация через LLM
        prompt = self._build_prompt(
            topic, difficulty, assignment_type, template, context
        )

        try:
            response = self.llm.invoke(prompt)
            assignment = self._parse_response(str(response.content), assignment_type)

            # Добавляем метаданные
            assignment.update(
                {
                    "id": f"{assignment_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    "topic": topic,
                    "difficulty": difficulty,
                    "type": assignment_type,
                    "created": datetime.now().isoformat(),
                    "time_estimate": self._estimate_time(difficulty),
                    "points": self._calculate_points(difficulty),
                }
            )

            return assignment

        except Exception:
            # Fallback: создаём простое задание без LLM
            return self._create_fallback_assignment(
                topic, difficulty, assignment_type, template
            )

    def _build_prompt(
        self,
        topic: str,
        difficulty: str,
        assignment_type: str,
        template: str,
        context: str,
    ) -> str:
        """Строит промпт для генерации задания"""
        return f"""
Ты - опытный преподаватель кибербезопасности. Создай практическое задание.

Тема: {topic}
Сложность: {difficulty}
Тип: {assignment_type}
Шаблон: {template}

Контекст из базы знаний:
{context if context else "(контекст отсутствует)"}

Создай задание со seguinte структурой:
1. Заголовок (краткий и ёмкий)
2. Описание (что нужно сделать, цель)
3. Сценарий атаки/задачи (пошагово)
4. Флаги (если CTF) - один или несколько флагов в формате FLAG{{...}}
5. Подсказки (2-3 уровня: лёгкая, средняя, сложная)
6. Решение (подробное, с объяснениями)
7. Необходимые ресурсы (инструменты, команды, ссылки)

Формат ответа (JSON):
{{
  "title": "...",
  "description": "...",
  "scenario": "...",
  "flags": ["FLAG{...}"],
  "hints": ["подсказка 1", "подсказка 2", "подсказка 3"],
  "solution": "...",
  "resources": ["инструмент1", "команда2", "ссылка3"]
}}

Будь креативным, но реалистичным. Задание должно быть выполнимо и обучающим.
"""

    def _parse_response(self, response: str, assignment_type: str) -> dict[str, Any]:
        """Парсит ответ LLM в结构化 задание"""
        import json
        import re

        # Извлекаем JSON из ответа
        json_match = re.search(r"\{.*\}", response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass

        # Fallback: создаём простое задание из текста
        return {
            "title": f"Практическое задание по теме",
            "description": response[:500] if response else "Создайте задание вручную",
            "flags": [],
            "hints": [],
            "solution": "См. описание выше",
            "resources": [],
        }

    def _create_fallback_assignment(
        self, topic: str, difficulty: str, assignment_type: str, template: str
    ) -> dict[str, Any]:
        """Создаёт простое задание без LLM (fallback)"""
        templates = {
            "ctf": {
                "title": f"CTF: {topic}",
                "description": f"Найдите флаг, используя знания по {topic}. Примените соответствующие инструменты и техники.",
                "scenario": f"Вы получили артефакт (файл/контейнер/сервис), содержащий скрытый флаг. Используйте {topic} для его извлечения.",
                "flags": [f"FLAG{{{topic.upper()}_PLEASE_WRITE_YOUR_OWN}}"],
                "hints": [
                    f"Изучите документацию по {topic}",
                    f"Попробуйте стандартные инструменты для {topic}",
                    "Флаг может быть скрыт в метаданных или steganography",
                ],
                "solution": "Это fallback задание. Настройте LLM для генерации подробного решения.",
                "resources": ["nmap", "sqlmap", "burpsuite", "john", "stegsolve"],
            }
        }

        base = templates.get(assignment_type, templates["ctf"]).copy()
        base.update(
            {
                "id": f"{assignment_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "topic": topic,
                "difficulty": difficulty,
                "type": assignment_type,
                "created": datetime.now().isoformat(),
                "time_estimate": self._estimate_time(difficulty),
                "points": self._calculate_points(difficulty),
            }
        )
        return base

    def _estimate_time(self, difficulty: str) -> str:
        """Оценивает время выполнения"""
        times = {
            "beginner": "15-30 минут",
            "intermediate": "30-60 минут",
            "advanced": "1-3 часа",
            "expert": "3+ часа",
        }
        return times.get(difficulty, "30-60 минут")

    def _calculate_points(self, difficulty: str) -> int:
        """Вычисляет баллы за задание"""
        points = {"beginner": 10, "intermediate": 25, "advanced": 50, "expert": 100}
        return points.get(difficulty, 25)

    def generate_batch(self, topics: list[str], count: int = 5) -> list[dict[str, Any]]:
        """Генерирует несколько заданий"""
        assignments = []
        for _ in range(count):
            topic = random.choice(topics)
            diff = random.choice(["beginner", "intermediate", "advanced"])
            a_type = random.choice(list(self.ASSIGNMENT_TYPES.keys()))

            assignment = self.generate_assignment(topic, diff, a_type)
            assignments.append(assignment)

        return assignments


# Convenience function
def generate_assignment(topic: str, **kwargs) -> dict[str, Any]:
    """Быстрая генерация задания"""
    generator = AssignmentGenerator()
    return generator.generate_assignment(topic, **kwargs)
