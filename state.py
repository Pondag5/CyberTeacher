"""
🔐 Состояние приложения - глобальные переменные в одном месте
"""

import os
import logging
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List, Tuple

@dataclass
class AppState:
    """Глобальное состояние приложения"""
    
    # Курс
    current_course: Optional[str] = None
    current_topic: int = 0
    
    # Новости
    last_news: Optional[str] = None
    
    # Статистика
    points: int = 0
    
    # Режим
    current_mode: str = "teacher"
    
    # Контекст обучения
    learning_context: Dict[str, Any] = field(default_factory=lambda: {
        "current_course": None,
        "current_topic": None,
        "current_lab": None,
        "last_action": None
    })
    
    # Для курсов
    course_progress: Dict[str, int] = field(default_factory=dict)
    
    # Персона (персистентная)
    current_persona: str = "teacher"
    
    # Активное задание и прогресс по флагам
    active_assignment: Optional[Dict] = None
    collected_flags: List[str] = field(default_factory=list)
    
    def reset_course(self):
        """Сбросить прогресс курса"""
        self.current_course = None
        self.current_topic = 0
    
    def set_course(self, course_id: str):
        """Установить текущий курс"""
        self.current_course = course_id
        self.current_topic = 0
    
    def next_topic(self):
        """Следующая тема"""
        self.current_topic += 1
    
    def set_learning_context(self, course=None, topic=None, lab=None, action=None):
        """Установить контекст обучения"""
        if course:
            self.learning_context["current_course"] = course
        if topic:
            self.learning_context["current_topic"] = topic
        if lab:
            self.learning_context["current_lab"] = lab
        if action:
            self.learning_context["last_action"] = action
    
    def get_learning_context(self) -> Dict[str, Any]:
        """Получить контекст обучения"""
        return self.learning_context
    
    def set_persona(self, persona: str):
        """Установить текущую персону (teacher, expert, ctf, review)"""
        self.current_persona = persona
        # Также обновляем режим для совместимости
        from ui import Mode
        persona_to_mode = {
            "teacher": Mode.TEACHER,
            "expert": Mode.EXPERT,
            "ctf": Mode.CTF,
            "review": Mode.REVIEW
        }
        if persona in persona_to_mode:
            # Сохраняем режим как строку, чтобы избежать циклического импорта
            self.current_mode = persona_to_mode[persona].value if hasattr(persona_to_mode[persona], 'value') else persona
    
    def get_persona(self) -> str:
        """Получить текущую персону"""
        return self.current_persona
    
    def set_active_assignment(self, assignment: Dict):
        """Установить активное задание и сбросить собранные флаги"""
        self.active_assignment = assignment
        self.collected_flags = []
    
    def collect_flag(self, flag: str) -> Tuple[bool, int]:
        """Собрать флаг в активном задании. Возвращает (успех, очки)"""
        if self.active_assignment:
            flags = self.active_assignment.get('flags', [])
            if flag in flags and flag not in self.collected_flags:
                self.collected_flags.append(flag)
                total_points = self.active_assignment.get('points', 0)
                per_flag = total_points // len(flags) if flags else total_points
                return True, per_flag
        return False, 0
    
    def is_assignment_complete(self) -> bool:
        """Проверить, все ли флаги задания собраны"""
        if not self.active_assignment:
            return False
        flags = self.active_assignment.get('flags', [])
        return len(self.collected_flags) >= len(flags)
    
    def get_assignment_progress(self) -> Dict[str, Any]:
        """Получить прогресс по активному заданию"""
        if not self.active_assignment:
            return {}
        flags = self.active_assignment.get('flags', [])
        total = len(flags)
        collected = len(self.collected_flags)
        per_flag = self.active_assignment.get('points', 0) // total if total else 0
        earned = per_flag * collected
        return {
            'id': self.active_assignment.get('id'),
            'title': self.active_assignment.get('title'),
            'total_flags': total,
            'collected_flags': collected,
            'remaining': total - collected,
            'points_earned': earned
        }
    
    def save_to_file(self, path: str = "./memory/app_state.json"):
        """Сохранить состояние в файл"""
        import json
        state_dict = {
            "current_course": self.current_course,
            "current_topic": self.current_topic,
            "last_news": self.last_news,
            "points": self.points,
            "current_mode": self.current_mode,
            "current_persona": self.current_persona,
            "learning_context": self.learning_context,
            "course_progress": self.course_progress,
            "active_assignment": self.active_assignment,
            "collected_flags": self.collected_flags
        }
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(state_dict, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.error(f"Не удалось сохранить состояние: {e}")
    
    def load_from_file(self, path: str = "./memory/app_state.json"):
        """Загрузить состояние из файла"""
        import json
        try:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.current_course = data.get("current_course")
                self.current_topic = data.get("current_topic", 0)
                self.last_news = data.get("last_news")
                self.points = data.get("points", 0)
                self.current_mode = data.get("current_mode", "teacher")
                self.current_persona = data.get("current_persona", "teacher")
                self.learning_context = data.get("learning_context", self.learning_context)
                self.course_progress = data.get("course_progress", {})
                self.active_assignment = data.get("active_assignment")
                self.collected_flags = data.get("collected_flags", [])
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.error(f"Не удалось загрузить состояние: {e}")

# Глобальный экземпляр
app_state = AppState()


def get_state() -> AppState:
    """Получить состояние"""
    return app_state
