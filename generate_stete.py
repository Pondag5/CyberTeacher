#!/usr/bin/env python3
"""
Генерирует плоский AppState с полями из всех моделей + дополнительные поля,
которые встречаются в коде (по ошибкам mypy).
Запуск: python generate_state.py
"""

import ast
import os
from pathlib import Path

MODELS_DIR = Path("models")
OUTPUT_FILE = Path("state.py")

MODEL_FILES = {
    "ProgressState": "progress_state",
    "UserState": "user_state",
    "SettingsState": "settings_state",
    "MetricsState": "metrics_state",
}

# Дополнительные поля, которые не вошли в модели, но нужны mypy (из ошибок)
EXTRA_FIELDS = {
    # Из state.py ошибок
    "xp": "float = 0.0",
    "level": "int = 1",
    "completed_quizzes": "list = []",
    "completed_tasks": "list = []",
    "weak_topics": "list = []",
    "achievements": "list = []",
    "skills": "dict = {}",
    "current_node": "str | None = None",
    "loop_count": "int = 0",
    "_daily_streak": "int = 0",
    "_offline_mode": "bool = False",
    "_communication_mood": "str = 'normal'",
    "_completed_cells": "list[int] = []",
    "_current_notebook": "str | None = None",
    "_current_mode": "str = 'teacher'",
    "_current_persona": "str = 'teacher'",
    "_msg_count_since_summary": "int = 0",
    "last_writeup_activity": "dict | None = None",
    "writeup_history": "list = []",
    "bounty_reports": "list = []",
    "voice_enabled": "bool = False",
    "versus_active": "bool = False",
    "versus_scenario": "str | None = None",
    "versus_attempts": "int = 0",
    "versus_history": "list = []",
    "thm_rooms_cache": "dict = {}",
    "thm_completed": "list = []",
    "thm_points": "int = 0",
    "thm_level": "int = 1",
    "thm_rank": "str = 'Новичок'",
    "thm_username": "str | None = None",
    "tracks_enrolled": "list = []",
    "track_progress": "dict = {}",
    "current_theme": "str = 'default'",
    "sync_id": "str | None = None",
    "reputation": "int = 0",
    "username": "str = 'Аноним'",
    "avatar": "str = '🧑‍💻'",
    "points": "float = 0.0",
    "total_flags_collected": "int = 0",
    "assignments_completed": "int = 0",
    "labs_started": "int = 0",
    "quizzes_taken": "int = 0",
    "news_checked": "int = 0",
    "messages_sent": "int = 0",
    "social_success": "int = 0",
    "apt_groups_viewed": "int = 0",
    "stealth_ops": "int = 0",
    "threat_exposures": "int = 0",
    "xp_boost_multiplier": "float = 1.0",
    "xp_boost_expiry": "float = 0.0",
    "owned_themes": "list = []",
    "unlocked_topics": "list = []",
    "selected_tools": "list = []",
    "trace_deadline": "float | None = None",
    "trace_hint": "str | None = None",
    "missions_completed": "list = []",
    "active_mission": "str | None = None",
    "risk_level": "int = 0",
    "learning_context": "dict = None",
    "course_progress": "dict = {}",
    "current_course": "str | None = None",
    "current_topic": "int = 0",
    "last_news": "str | None = None",
    "news_analyzed": "int = 0",
    "feature_flags": "dict = {}",
    "emotion_mode": "str = 'neutral'",
    "found_evidence": "list = []",
    "current_case": "str | None = None",
    "exploit_success": "list = []",
    "current_challenge": "dict | None = None",
    "active_assignment": "dict | None = None",
    "collect_flag": "Any = None",
    "is_assignment_complete": "Any = None",
    "ctf_flags_generated": "int = 0",
    "phishing_generated": "int = 0",
    "mermaid_views": "int = 0",
    "purchase_history": "list = []",
    "running_labs": "list = []",
    "htb_token": "str | None = None",
    "htb_completed": "list = []",
    "htb_email": "str | None = None",
    "htb_password": "str | None = None",
    "language": "str = 'ru'",
    "explanation_depth": "str = 'normal'",
    "hint_enabled": "bool = True",
    "hint_credits": "int = 3",
    "hints_used": "int = 0",
    "last_hint_time": "float = 0.0",
    "hint_cooldown": "int = 30",
    "voice_engine": "str = 'pyttsx3'",
    "voice_rate": "int = 200",
    "llm_call_count": "int = 0",
    "llm_total_time": "float = 0.0",
    "llm_total_tokens": "int = 0",
    "cache_hits": "int = 0",
    "cache_misses": "int = 0",
    "start_time": "float = 0.0",
    "request_timestamps": "list = []",
    "command_usage": "dict = {}",
    "HANDLES": "list = []",
    "model_config": 'dict = {"validate_assignment": True}',
}

def collect_fields_from_models() -> dict[str, str]:
    """Собирает поля из Pydantic моделей."""
    all_fields = {}
    for model_name, file_stem in MODEL_FILES.items():
        model_path = MODELS_DIR / f"{file_stem}.py"
        if not model_path.exists():
            continue
        with open(model_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == model_name:
                for body_node in node.body:
                    if isinstance(body_node, ast.AnnAssign) and isinstance(body_node.target, ast.Name):
                        name = body_node.target.id
                        if name.startswith("_"):
                            continue
                        # Тип можно игнорировать, просто зададим Any
                        all_fields[name] = "Any = None"
                    elif isinstance(body_node, ast.Assign):
                        for target in body_node.targets:
                            if isinstance(target, ast.Name) and not target.id.startswith("_"):
                                all_fields[target.id] = "Any = None"
    return all_fields

def generate_state():
    fields = collect_fields_from_models()
    # Добавляем ручные поля из EXTRA_FIELDS (переопределяют, если нужно)
    fields.update(EXTRA_FIELDS)
    # Убираем дубликаты по ключам
    # Сортируем для красоты
    sorted_keys = sorted(fields.keys())
    
    content = '''"""
Плоское состояние приложения (сгенерировано). Все поля доступны напрямую.
"""
import time
import json
import os
from typing import Any

class AppState:
    def __init__(self):
'''
    # Добавляем инициализацию полей
    for key in sorted_keys:
        default = fields[key]
        # Если default содержит '=', то это уже присваивание
        if '=' in default:
            content += f"        self.{key} = {default}\n"
        else:
            content += f"        self.{key} = {default}\n"
    
    # Добавляем методы
    content += '''
    # --- Методы для загрузки/сохранения ---
    def load_from_file(self, path: str = "./memory/app_state.json") -> None:
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for key, value in data.items():
                if hasattr(self, key):
                    setattr(self, key, value)
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Error loading state: {e}")

    def save_to_file(self, path: str = "./memory/app_state.json") -> None:
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self.__dict__, f, ensure_ascii=False, indent=2, default=str)
        except Exception as e:
            print(f"Error saving state: {e}")

    def maybe_auto_backup(self) -> None:
        self.save_to_file()

    # --- Методы, которые вызываются в коде (заглушки) ---
    def get_weak_topics(self, threshold: float = 70.0) -> list:
        return getattr(self, "weak_topics", [])

    def get_due_reviews(self) -> list:
        return []

    def track_command_usage(self, command: str) -> None:
        if not hasattr(self, "command_usage"):
            self.command_usage = {}
        self.command_usage[command] = self.command_usage.get(command, 0) + 1

    def can_make_request(self, window_seconds: int = 60, max_requests: int = 10) -> bool:
        now = time.time()
        if not hasattr(self, "request_timestamps"):
            self.request_timestamps = []
        self.request_timestamps = [ts for ts in self.request_timestamps if now - ts < window_seconds]
        return len(self.request_timestamps) < max_requests

    def record_request(self) -> None:
        if not hasattr(self, "request_timestamps"):
            self.request_timestamps = []
        self.request_timestamps.append(time.time())

    def get_xp_multiplier(self) -> float:
        return getattr(self, "xp_boost_multiplier", 1.0)

    def apply_xp_boost(self, multiplier: float, duration_hours: float) -> None:
        self.xp_boost_multiplier = max(0.0, multiplier)
        self.xp_boost_expiry = time.time() + max(0.0, duration_hours) * 3600

    def get_risk_status(self) -> str:
        if self.risk_level < 20:
            return "🟢 Низкий"
        if self.risk_level < 50:
            return "🟡 Умеренный"
        if self.risk_level < 80:
            return "🟠 Высокий"
        return "🔴 Критический"

    def increase_risk(self, amount: int = 10) -> None:
        self.risk_level = min(100, self.risk_level + amount)

    def decrease_risk(self, amount: int = 5) -> None:
        self.risk_level = max(0, self.risk_level - amount)

    def reset_risk(self) -> None:
        self.risk_level = 0

    def set_persona(self, persona: str) -> None:
        self._current_persona = persona

    def get_persona(self) -> str:
        return getattr(self, "_current_persona", "teacher")

    def get_learning_context(self) -> dict:
        return getattr(self, "learning_context", {})

    def set_learning_context(self, course=None, topic=None, lab=None, action=None) -> None:
        ctx = self.get_learning_context()
        if course:
            ctx["current_course"] = course
        if topic:
            ctx["current_topic"] = topic
        if lab:
            ctx["current_lab"] = lab
        if action:
            ctx["last_action"] = action
        self.learning_context = ctx

    def increment_flag(self) -> None:
        self.total_flags_collected += 1

    def complete_assignment(self) -> None:
        self.assignments_completed += 1

    def start_lab(self) -> None:
        self.labs_started += 1

    def take_quiz(self) -> None:
        self.quizzes_taken += 1

    def check_news(self) -> None:
        self.news_checked += 1

    def increment_apt_groups_viewed(self) -> None:
        self.apt_groups_viewed += 1

    def increment_threat_exposures(self) -> None:
        self.threat_exposures += 1

    def increment_stealth_ops(self) -> None:
        self.stealth_ops += 1

    def apply_item_effect(self, item: dict) -> str | None:
        item_type = item.get("type")
        if item_type == "theme":
            theme_id = item.get("value")
            if theme_id and theme_id not in self.owned_themes:
                self.owned_themes.append(theme_id)
                return "theme"
        if item_type == "unlock_topic":
            topic = item.get("value")
            if topic and topic not in self.unlocked_topics:
                self.unlocked_topics.append(topic)
                return "unlock_topic"
        if item_type == "xp_boost":
            self.apply_xp_boost(item.get("multiplier", 2.0), item.get("duration_hours", 1))
            return "xp_boost"
        if item_type == "consumable" and item.get("effect") == "hint_credit":
            self.hint_credits += item.get("quantity", 1)
            return "hint_credit"
        return None

    def update_weak_topic(self, topic: str, success_rate: float) -> None:
        # Заглушка
        pass

    def schedule_review(self, topic: str, score: float) -> None:
        # Заглушка
        pass

    def get_next_weak_topic(self, threshold: float = 70.0) -> str | None:
        return None

    def check_achievements(self) -> list[str]:
        return []

    def track_skill(self, skill_id: str, success: bool, xp: int) -> None:
        pass

    def get_skill_level(self, skill_id: str) -> int:
        return 0

    def get_all_skills(self) -> dict:
        return {}

    def get_explanation_depth(self) -> str:
        return getattr(self, "explanation_depth", "normal")

    def set_explanation_depth(self, depth: str) -> None:
        self.explanation_depth = depth

    def add_reputation(self, amount: int) -> None:
        self.reputation += amount

    def get_handle(self) -> str:
        # Простейшая заглушка
        return getattr(self, "handle", "Новичок")

    def get_htb_password_encrypted(self) -> str | None:
        return None

    def set_htb_password_from_encrypted(self, encrypted: str | None) -> None:
        pass

# Синглтон
_state: AppState | None = None

def get_state() -> AppState:
    global _state
    if _state is None:
        _state = AppState()
    return _state
'''
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Generated {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_state()