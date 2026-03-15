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
    
    # Уровень риска / компрометации (для CTF/story режимов)
    risk_level: int = 0  # 0-100, увеличивается при ошибках, снижается при успехах
    
    # Статистика для достижений
    total_flags_collected: int = 0
    assignments_completed: int = 0
    labs_started: int = 0
    quizzes_taken: int = 0
    news_checked: int = 0
    messages_sent: int = 0
    earned_achievements: List[str] = field(default_factory=list)
    
    # Активное задание (для story/ctf)
    active_assignment: Optional[Dict[str, Any]] = None
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
            "review": Mode.CODE_REVIEW
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
    
    # === RISK LEVEL (CTF/Story mode) ===
    def increase_risk(self, amount: int = 10):
        """Увеличить уровень риска (при ошибке/срабатывании защиты)"""
        self.risk_level = min(100, self.risk_level + amount)
        self.check_achievements()
    
    def decrease_risk(self, amount: int = 5):
        """Уменьшить уровень риска (при успехе)"""
        self.risk_level = max(0, self.risk_level - amount)
        self.check_achievements()
    
    def reset_risk(self):
        """Сбросить уровень риска"""
        self.risk_level = 0
    
    def get_risk_status(self) -> str:
        """Получить текстовый статус риска"""
        if self.risk_level < 20:
            return "🟢 Низкий"
        elif self.risk_level < 50:
            return "🟡 Умеренный"
        elif self.risk_level < 80:
            return "🟠 Высокий"
        else:
            return "🔴 Критический"
    
    # === СТАТИСТИКА ===
    def increment_flag(self):
        """Увеличить счётчик собранных флагов"""
        self.total_flags_collected += 1
        self.check_achievements()
    
    def complete_assignment(self):
        """Отметить выполнение задания"""
        self.assignments_completed += 1
        self.check_achievements()
    
    def start_lab(self):
        """Отметить запуск лаборатории"""
        self.labs_started += 1
        self.check_achievements()
    
    def take_quiz(self):
        """Отметить прохождение квиза"""
        self.quizzes_taken += 1
        self.check_achievements()
    
    def check_news(self):
        """Отметить проверку новостей"""
        self.news_checked += 1
        # Не вызываем check_achievements здесь — вызываем в обработчике
    
    def send_message(self):
        """Увеличить счётчик отправленных сообщений"""
        self.messages_sent += 1
        # Не проверяем достижения для каждого сообщения (слишком часто)
    
    def check_achievements(self):
        """Проверить и выдать новые достижения"""
        import json, os
        achievements_file = "data/achievements.json"
        if not os.path.exists(achievements_file):
            return []
        
        try:
            with open(achievements_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            achievements_list = data.get("achievements", [])
        except Exception:
            return []
        
        newly_earned = []
        for ach in achievements_list:
            ach_id = ach.get("id")
            if not ach_id or ach_id in self.earned_achievements:
                continue
            
            cond = ach.get("condition", {})
            cond_type = cond.get("type")
            threshold = cond.get("threshold", 0)
            
            # Проверяем условия
            unlocked = False
            if cond_type == "flags_total":
                unlocked = self.total_flags_collected >= threshold
            elif cond_type == "assignments_completed":
                unlocked = self.assignments_completed >= threshold
            elif cond_type == "total_points":
                unlocked = self.points >= threshold
            elif cond_type == "labs_started":
                unlocked = self.labs_started >= threshold
            elif cond_type == "quizzes_taken":
                unlocked = self.quizzes_taken >= threshold
            elif cond_type == "news_checked":
                unlocked = self.news_checked >= threshold
            
            if unlocked:
                self.earned_achievements.append(ach_id)
                xp = ach.get("points", 0)
                if xp > 0:
                    self.points += xp
                newly_earned.append(ach)
        
        return newly_earned
    
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
            "risk_level": self.risk_level,
            "learning_context": self.learning_context,
            "course_progress": self.course_progress,
            "active_assignment": self.active_assignment,
            "collected_flags": self.collected_flags,
            "total_flags_collected": self.total_flags_collected,
            "assignments_completed": self.assignments_completed,
            "labs_started": self.labs_started,
            "quizzes_taken": self.quizzes_taken,
            "news_checked": self.news_checked,
            "messages_sent": self.messages_sent,
            "earned_achievements": self.earned_achievements if hasattr(self, 'earned_achievements') else []
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
                self.risk_level = data.get("risk_level", 0)
                self.learning_context = data.get("learning_context", self.learning_context)
                self.course_progress = data.get("course_progress", {})
                self.active_assignment = data.get("active_assignment")
                self.collected_flags = data.get("collected_flags", [])
                self.total_flags_collected = data.get("total_flags_collected", 0)
                self.assignments_completed = data.get("assignments_completed", 0)
                self.labs_started = data.get("labs_started", 0)
                self.quizzes_taken = data.get("quizzes_taken", 0)
                self.news_checked = data.get("news_checked", 0)
                self.messages_sent = data.get("messages_sent", 0)
                self.earned_achievements = data.get("earned_achievements", [])
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.error(f"Не удалось загрузить состояние: {e}")

# Глобальный экземпляр
app_state = AppState()


def get_state() -> AppState:
    """Получить состояние"""
    return app_state
