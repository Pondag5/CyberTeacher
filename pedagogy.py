
"""
🔐 Педагогический модуль CyberTeacher
"""

import json
import re
import random
from enum import Enum
from dataclasses import dataclass
from typing import List

# === ЗАГРУЗКА ПРОМПТОВ ИЗ JSON ===
import os
import json

TEACHER_PROMPTS_PATH = os.path.join(os.path.dirname(__file__), "config", "teacher_prompts.json")

def load_teacher_prompts():
    """Загрузить промпты из JSON файла"""
    try:
        with open(TEACHER_PROMPTS_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Ошибка загрузки промптов: {e}")
        return {}

_TEACHER_PROMPTS = None

def get_teacher_prompts():
    global _TEACHER_PROMPTS
    if _TEACHER_PROMPTS is None:
        _TEACHER_PROMPTS = load_teacher_prompts()
    return _TEACHER_PROMPTS

# === ENUMS ===
class StudentLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

@dataclass
class AssessmentResult:
    level: StudentLevel
    strengths: List[str]
    weaknesses: List[str]
    recommended_topics: List[str]
    overall_score: float

# === ТЕМЫ ДЛЯ ОЦЕНКИ ===
ASSESSMENT_TOPICS = {
    "basics": {"name": "Основы", "questions": [
        {"q": "Что такое IP-адрес?", "type": "open", "depth": 1},
        {"q": "TCP vs UDP?", "type": "choice", "options": ["Надёжность", "Скорость", "Оба"], "correct": "Оба"},
        {"q": "Что такое DNS?", "type": "open", "depth": 2}
    ]},
    "web": {"name": "Веб", "questions": [
        {"q": "Что такое SQL-инъекция?", "type": "open", "depth": 1},
        {"q": "HTTP методы?", "type": "choice", "options": ["GET", "POST", "PUT/DELETE", "HEAD"], "correct": "PUT/DELETE"},
        {"q": "Типы XSS?", "type": "open", "depth": 2}
    ]},
    "crypto": {"name": "Крипто", "questions": [
        {"q": "Симметричное vs Асимметричное?", "type": "open", "depth": 1},
        {"q": "Что такое хеширование?", "type": "choice", "options": ["Шифрование", "Односторонняя", "Сжатие"], "correct": "Односторонняя"},
        {"q": "Зачем salt?", "type": "open", "depth": 2}
    ]},
    "practice": {"name": "Практика", "questions": [
        {"q": "Инструменты nmap?", "type": "open", "depth": 1},
        {"q": "Что такое CTF?", "type": "choice", "options": ["Язык", "Соревнования", "Протокол"], "correct": "Соревнования"},
        {"q": "OWASP процесс?", "type": "open", "depth": 3}
    ]},
    "social": {"name": "Социнжен", "questions": [
        {"q": "Что такое фишинг?", "type": "open", "depth": 1},
        {"q": "Типы фишинга?", "type": "choice", "options": ["Email", "SMS", "Голосовой", "Все"], "correct": "Все"},
        {"q": "Как распознать фишинг?", "type": "open", "depth": 2}
    ]}
}

# === ЛИЧНОСТЬ УЧИТЕЛЯ ===
class TeacherPersona:
    @staticmethod
    def get_system_prompt(include_socratic=False, include_thinking=False, style="hybrid") -> str:
        # Загружаем из JSON
        prompts = get_teacher_prompts()
        
        if style == "hybrid":
            persona = prompts.get("personas", {}).get("hybrid", {}).get("instructions", [])
            base = prompts.get("system_prompt", "Ты - учитель кибербезопасности.")
            return f"{base}\n\nПравила:\n" + "\n".join([f"- {p}" for p in persona])
        
        return prompts.get("system_prompt", "Ты - учитель кибербезопасности.")

# === РАЗМЫШЛЕНИЯ ===
class ThinkingVisualizer:
    TEMPLATES = {
        "socratic": [
            "🧠 Хмм... {topic}... Давай подумаем вместе...",
            "🧠 Ооо, интересно! А что если посмотреть с другой стороны?",
            "🧠 Слушай, это как в том случае с {example}...",
            "🧠 Подожди! Сначала нужно понять что такое {prequel}...",
            "🧠 Стоп! А ты уверен что тебе нужен ответ? Может лучше спросить себя...",
            "🧠 Знаешь что будет если {action}? Давай разберём...",
        ],
        "encouraging": [
            "🧠 Ооо, хороший вопрос! Ща разберёмся!",
            "🧠 Интересный ход мысли! Давай копнём глубже!",
            "🧠 Неплохо! Но есть нюанс...",
            "🧠 Хороший вопрос! Вижу ты думаешь в правильном направлении!",
        ],
        "doc_style": [
            "🧠 Представь это как машину времени... Сначала было X, потом Y...",
            "🧠 Давай разберём по порядку, как в хорошем научном эксперименте...",
            "🧠 Исторически сложилось так: в {year} году...",
            "🧠 Механизм работает так: {mechanism}...",
        ],
        "rick_style": [
            "🧠 Ооо, блин! Это же классика! Помнишь когда я в {year}...",
            "🧠 Слушай, это дичь, но я тебе расскажу как это работает!",
            "🧠 База! Это как в том случае с {example}, но ещё круче!",
            "🧠 Знаешь что? Забей на теорию, вот реальный пример...",
        ]
    }

    @staticmethod
    def generate_thinking(context: str, question: str, mode: str = "socratic", template_vars: dict = None) -> str:
        template_vars = template_vars or {}
        templates = ThinkingVisualizer.TEMPLATES.get(mode, ThinkingVisualizer.TEMPLATES["socratic"])
        thought = random.choice(templates)
        for k, v in template_vars.items():
            thought = thought.replace(f"{{{k}}}", v)
        return thought

# === ОЦЕНКА УРОВНЯ ===
class LevelAssessor:
    def __init__(self):
        self.current_questions = []
        self.scores = []

    def generate_assessment(self):
        questions = []
        for topic_id, topic_data in ASSESSMENT_TOPICS.items():
            for q in topic_data["questions"][:2]:
                questions.append({"topic": topic_id, "topic_name": topic_data["name"], **q})
        random.shuffle(questions)
        self.current_questions = questions[:10]
        return self.current_questions

    def analyze_results(self):
        if not self.scores:
            return AssessmentResult(StudentLevel.BEGINNER, [], [], ["basics"], 0.0)

        topic_scores = {}
        for i, score in enumerate(self.scores):
            if i < len(self.current_questions):
                topic = self.current_questions[i]["topic"]
                if topic not in topic_scores:
                    topic_scores[topic] = []
                topic_scores[topic].append(score)

        overall = sum(self.scores) / len(self.scores)

        if overall >= 80: level = StudentLevel.EXPERT
        elif overall >= 60: level = StudentLevel.ADVANCED
        elif overall >= 40: level = StudentLevel.INTERMEDIATE
        else: level = StudentLevel.BEGINNER

        strengths = [t for t, s in topic_scores.items() if sum(s)/len(s) >= 50]
        weaknesses = [t for t, s in topic_scores.items() if sum(s)/len(s) < 50]

        return AssessmentResult(level, strengths, weaknesses, weaknesses[:3], overall)

# === MEREAD ===

class MermaidGenerator:
    @staticmethod
    def generate_concept_map(root, nodes):
        nodes_str = "\n".join([f"    {root} --> {node}" for node in nodes])
        return f"```mermaid\nmindmap\n  root(({root}))\n{nodes_str}\n```"

    @staticmethod
    def generate_flowchart(steps):
        flow = "\n".join([f"    step{i}[{s}] --> step{i+1}[{steps[i+1]}]"
                          for i, s in enumerate(steps[:-1])])
        return f"```mermaid\nflowchart LR\n    start([Начало])\n{flow}\n    finish([Конец])\n```"

    @staticmethod
    def generate_attack_chain(root, steps):
        chain = "\n".join([f"    A{i+1}[{s}] -->" for i, s in enumerate(steps[:-1])])
        # ИСПРАВЛЕНО: streads -> steps
        return f"```mermaid\nflowchart TD\n    Start[Цель] --> A1[{steps[0]}]\n{chain} A{len(steps)}[ФЛАГ]\n```"