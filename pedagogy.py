"""
🔐 Педагогический модуль CyberTeacher
"""

import json
import os
import random
import re
from typing import Any, ClassVar, Dict, List

TEACHER_PROMPTS_PATH = os.path.join(
    os.path.dirname(__file__), "config", "teacher_prompts.json"
)


def load_teacher_prompts() -> Dict[str, Any]:
    """Загрузить промпты из JSON файла"""
    try:
        with open(TEACHER_PROMPTS_PATH, "r", encoding="utf-8") as f:
            result: Dict[str, Any] = json.load(f)
            return result
    except Exception as e:
        print(f"Ошибка загрузки промптов: {e}")
        return {}


_TEACHER_PROMPTS: Dict[str, Any] | None = None


def get_teacher_prompts() -> Dict[str, Any]:
    global _TEACHER_PROMPTS
    if _TEACHER_PROMPTS is None:
        _TEACHER_PROMPTS = load_teacher_prompts()
    return _TEACHER_PROMPTS


# === ЛИЧНОСТЬ УЧИТЕЛЯ ===
class TeacherPersona:
    @staticmethod
    def get_system_prompt(
        _include_socratic: bool = False,
        _include_thinking: bool = False,
        style: str = "hybrid",
        language: str = "ru",
    ) -> str:
        # Загружаем из JSON
        prompts = get_teacher_prompts()

        # Если язык английский, используем английский промпт
        if language == "en":
            base: str = str(
                prompts.get(
                    "system_prompt_en",
                    prompts.get("system_prompt", "You are a cybersecurity teacher."),
                )
            )
        else:
            base = str(prompts.get("system_prompt", "Ты - учитель кибербезопасности."))

        if style == "hybrid":
            persona = (
                prompts.get("personas", {}).get("hybrid", {}).get("instructions", [])
            )
            return f"{base}\n\nRules:\n" + "\n".join([f"- {p}" for p in persona])

        return base


# === РАЗМЫШЛЕНИЯ ===
class ThinkingVisualizer:
    TEMPLATES: ClassVar[Dict[str, List[str]]] = {
        "socratic": [
            "🧠 О боже... {topic}... Давай подумаем вместе, ладно?",
            "🧠 Ооо, интересный вопрос! А что если посмотреть с другой стороны? Я не уверен, но...",
            "🧠 Слушай, это как в том случае с {example} — помнишь, Рик говорил...",
            "🧠 Подожди! Сначала нужно понять что такое {prequel}, иначе... ну ты понял.",
            "🧠 Стоп! А ты уверен что тебе нужен ответ? Может лучше спросить себя...",
            "🧠 Знаешь что будет если {action}? Давай разберём... О боже, это будет круто!",
        ],
        "encouraging": [
            "🧠 Великолепно! Хороший вопрос! Ща разберёмся!",
            "🧠 1.21 гигаватт любопытства! Давай копнём глубже!",
            "🧠 Неплохо! Но есть нюанс... О боже, сейчас объясню!",
            "🧠 Хороший вопрос! Вижу ты думаешь в правильном направлении! Великолепно!",
        ],
        "doc_style": [
            "🧠 Представь это как машину времени... Сначала было X, потом Y — и ВЖУХ!",
            "🧠 Давай разберём по порядку, как в хорошем научном эксперименте... О боже, я люблю это!",
            "🧠 Исторически сложилось так: в {year} году... Великолепно!",
            "🧠 Механизм работает так: {mechanism}... Это как flux capacitor, только для хакеров!",
        ],
        "rick_style": [
            "🧠 О боже, блин! Это же классика! Помнишь когда я... ладно, неважно!",
            "🧠 Слушай, это дичь, но я тебе расскажу как это работает! О боже!",
            "🧠 Великолепно! Это как в том случае с {example}, но ещё круче!",
            "🧠 Знаешь что? Забей на теорию, вот реальный пример... О боже, поехали!",
        ],
    }

    @staticmethod
    def generate_thinking(
        _context: str,
        _question: str,
        mode: str = "socratic",
        template_vars: Dict[str, str] | None = None,
    ) -> str:
        template_vars = template_vars or {}
        templates = ThinkingVisualizer.TEMPLATES.get(
            mode, ThinkingVisualizer.TEMPLATES["socratic"]
        )
        thought = random.choice(templates)
        for k, v in template_vars.items():
            thought = thought.replace(f"{{{k}}}", v)
        return thought


# === Mermaid ===
class MermaidGenerator:
    @staticmethod
    def generate_concept_map(root: str, nodes: List[str]) -> str:
        nodes_str = "\n".join([f"    {root} --> {node}" for node in nodes])
        return f"```mermaid\nmindmap\n  root(({root}))\n{nodes_str}\n```"

    @staticmethod
    def generate_flowchart(steps: List[str]) -> str:
        flow = "\n".join(
            [
                f"    step{i}[{s}] --> step{i + 1}[{steps[i + 1]}]"
                for i, s in enumerate(steps[:-1])
            ]
        )
        return f"```mermaid\nflowchart LR\n    start([Начало])\n{flow}\n    finish([Конец])\n```"

    @staticmethod
    def generate_attack_chain(_root: str, steps: List[str]) -> str:
        chain = "\n".join([f"    A{i + 1}[{s}] -->" for i, s in enumerate(steps[:-1])])
        return f"```mermaid\nflowchart TD\n    Start[Цель] --> A1[{steps[0]}]\n{chain} A{len(steps)}[ФЛАГ]\n```"
