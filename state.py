"""
🔐 Состояние приложения - глобальные переменные в одном месте
"""

import logging
import os
import shutil
import time
from dataclasses import dataclass, field
from typing import Any

from utils.security import decrypt_value as _decrypt, encrypt_value as _encrypt, is_encrypted

# Импорты модульных компонентов состояния
from achievements_state import AchievementsState
from explanation_state import ExplanationState
from hints_state import HintsState
from learning_state import LearningState
from metrics_state import MetricsState
from persona_state import PersonaState
from risk_state import RiskState
from shop_state import ShopState
from user_state import UserState
from voice_state import VoiceState


class AppState:
    """Глобальное состояние приложения с модульной архитектурой"""

    # Модули состояния
    achievements: AchievementsState
    explanation: ExplanationState
    hints: HintsState
    learning: LearningState
    metrics: MetricsState
    persona: PersonaState
    risk: RiskState
    shop: ShopState
    user: UserState
    voice: VoiceState

    # Оставшиеся атрибуты, которые ещё не вынесены в модули
    last_news: str | None
    active_assignment: dict[str, Any] | None
    collected_flags: list[str]
    weak_topics: list[dict[str, Any]]
    review_schedule: dict[str, dict[str, Any]]
    feature_flags: dict[str, bool]
    last_writeup_activity: dict[str, Any] | None
    writeup_history: list[dict[str, Any]]
    exploit_success: list[dict]
    tracks_enrolled: list[str]
    track_progress: dict[str, dict[str, Any]]
    bounty_reports: list[dict[str, Any]]
    skill_tracker: dict[str, dict[str, Any]]
    emotion_mode: str

    def __init__(self):
        # Инициализация модульных компонентов
        self.achievements = AchievementsState()
        self.explanation = ExplanationState()
        self.hints = HintsState()
        self.learning = LearningState()
        self.metrics = MetricsState()
        self.persona = PersonaState()
        self.risk = RiskState()
        self.shop = ShopState()
        self.user = UserState()
        self.voice = VoiceState()

        # Инициализация оставшихся атрибутов
        self.last_news = None
        self.active_assignment = None
        self.collected_flags = []
        self.weak_topics = []
        self.review_schedule = {}
        self.feature_flags = {}
        self.last_writeup_activity = None
        self.writeup_history = []
        self.exploit_success = []
        self.tracks_enrolled = []
        self.track_progress = {}
        self.bounty_reports = []
        self.skill_tracker = {}
        self.emotion_mode = "neutral"

    def __getattr__(self, name: str) -> Any:
        """Делегирование доступа к атрибутам модулей для обратной совместимости"""
        # Маппинг атрибутов к модулям
        module_mapping = {
            # learning_state
            "current_course": "learning", "current_topic": "learning",
            "course_progress": "learning", "learning_context": "learning",
            # achievements_state
            "total_flags_collected": "achievements", "assignments_completed": "achievements",
            "labs_started": "achievements", "quizzes_taken": "achievements",
            "news_checked": "achievements", "messages_sent": "achievements",
            "earned_achievements": "achievements", "social_success": "achievements",
            "apt_groups_viewed": "achievements", "stealth_ops": "achievements",
            "threat_exposures": "achievements", "points": "achievements",
            "xp_boost_multiplier": "achievements", "xp_boost_expiry": "achievements",
            # metrics_state
            "llm_call_count": "metrics", "llm_total_time": "metrics",
            "llm_total_tokens": "metrics", "cache_hits": "metrics",
            "cache_misses": "metrics", "start_time": "metrics",
            "request_timestamps": "metrics", "command_usage": "metrics",
            # user_state
            "username": "user", "avatar": "user", "reputation": "user",
            "handle": "user", "htb_email": "user", "htb_password": "user",
            "htb_completed": "user",
            # shop_state
            "owned_themes": "shop", "current_theme": "shop",
            "unlocked_topics": "shop", "hint_credits": "shop",
            "selected_tools": "shop", "trace_deadline": "shop",
            "trace_hint": "shop", "missions_completed": "shop",
            "active_mission": "shop", "xp_boost_multiplier": "shop",
            "xp_boost_expiry": "shop",
            # risk_state
            "risk_level": "risk",
            # voice_state
            "voice_enabled": "voice", "voice_engine": "voice", "voice_rate": "voice",
            # persona_state
            "current_persona": "persona", "current_mode": "persona",
            # hints_state
            "hint_enabled": "hints", "hints_used": "hints",
            "last_hint_time": "hints", "hint_cooldown": "hints",
            # explanation_state
            "explanation_depth": "explanation",
        }

        if name in module_mapping:
            module_name = module_mapping[name]
            return getattr(getattr(self, module_name), name)
        
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    def __setattr__(self, name: str, value: Any) -> None:
        """Делегирование записи атрибутов модулям для обратной совместимости"""
        module_mapping = {
            "current_course": "learning", "current_topic": "learning",
            "course_progress": "learning", "learning_context": "learning",
            "total_flags_collected": "achievements", "assignments_completed": "achievements",
            "labs_started": "achievements", "quizzes_taken": "achievements",
            "news_checked": "achievements", "messages_sent": "achievements",
            "earned_achievements": "achievements", "social_success": "achievements",
            "apt_groups_viewed": "achievements", "stealth_ops": "achievements",
            "threat_exposures": "achievements", "points": "achievements",
            "xp_boost_multiplier": "achievements", "xp_boost_expiry": "achievements",
            "llm_call_count": "metrics", "llm_total_time": "metrics",
            "llm_total_tokens": "metrics", "cache_hits": "metrics",
            "cache_misses": "metrics", "start_time": "metrics",
            "request_timestamps": "metrics", "command_usage": "metrics",
            "username": "user", "avatar": "user", "reputation": "user",
            "handle": "user", "htb_email": "user", "htb_password": "user",
            "htb_completed": "user",
            "owned_themes": "shop", "current_theme": "shop",
            "unlocked_topics": "shop", "hint_credits": "shop",
            "selected_tools": "shop", "trace_deadline": "shop",
            "trace_hint": "shop", "missions_completed": "shop",
            "active_mission": "shop", "xp_boost_multiplier": "shop",
            "xp_boost_expiry": "shop",
            "risk_level": "risk",
            "voice_enabled": "voice", "voice_engine": "voice", "voice_rate": "voice",
            "current_persona": "persona", "current_mode": "persona",
            "hint_enabled": "hints", "hints_used": "hints",
            "last_hint_time": "hints", "hint_cooldown": "hints",
            "explanation_depth": "explanation",
        }

        # Прямые атрибуты AppState
        direct_attrs = {
            "last_news", "active_assignment", "collected_flags", "weak_topics",
            "review_schedule", "feature_flags", "last_writeup_activity",
            "writeup_history", "exploit_success", "tracks_enrolled",
            "track_progress", "bounty_reports", "skill_tracker", "emotion_mode",
            # Модули
            "achievements", "explanation", "hints", "learning", "metrics",
            "persona", "risk", "shop", "user", "voice"
        }

        if name in direct_attrs:
            object.__setattr__(self, name, value)
        elif name in module_mapping:
            module_name = module_mapping[name]
            setattr(getattr(self, module_name), name, value)
        else:
            object.__setattr__(self, name, value)

    def update_weak_topic(self, topic: str, score: float, max_score: float = 10.0):
        """Обновить статистику по слабой теме.

        Args:
            topic: Название темы (например, "sql", "xss")
            score: Полученный балл
            max_score: Максимальный возможный балл (по умолчанию 10)
        """
        # Найти существующую запись
        for entry in self.weak_topics:
            if entry["topic"] == topic:
                # Обновить: добавить новый результат к совокупной статистике
                entry["attempts"] += 1
                entry["total_score"] += score
                entry["max_score"] += max_score
                entry["success_rate"] = (
                    (entry["total_score"] / entry["max_score"]) * 100
                    if entry["max_score"] > 0
                    else 0
                )
                return

        # Создать новую запись
        self.weak_topics.append(
            {
                "topic": topic,
                "attempts": 1,
                "total_score": score,
                "max_score": max_score,
                "success_rate": (score / max_score) * 100 if max_score > 0 else 0,
            }
        )

    def get_weak_topics(self, threshold: float = 70.0) -> list[dict[str, Any]]:
        """Получить список тем с успешностью ниже threshold%.

        Returns:
            list[dict] с полями topic, success_rate, attempts, отсортированный по возрастанию success_rate
        """
        weak = [t for t in self.weak_topics if t["success_rate"] < threshold]
        return sorted(weak, key=lambda x: x["success_rate"])

    def get_next_weak_topic(self, threshold: float = 70.0) -> str | None:
        """Получить следующую тему для фокуса (самую слабую).

        Returns:
            topic ID (str) или None если всё хорошо
        """
        weak = self.get_weak_topics(threshold)
        if weak:
            return weak[0]["topic"]
        return None

    def clear_weak_topics(self):
        """Очистить статистику слабых тем."""
        self.weak_topics = []

    # === SPACED REPETITION (SuperMemo-like) ===

    def _compute_next_review(self, interval_days: int) -> float:
        """Вычислить timestamp следующего повторения."""
        import time

        return time.time() + interval_days * 86400

    def schedule_review(self, topic: str, grade: float, max_grade: float = 10.0):
        """Запланировать следующее повторение для темы на основе оценки (SM-2 algorithm simplified).

        Args:
            topic: Название темы
            grade: Полученный балл (0..max_grade)
            max_grade: Максимальный балл (по умолчанию 10)
        """
        quality = (grade / max_grade) * 5  # Преобразуем в шкалу 0-5

        if topic not in self.review_schedule:
            # Первое изучение: первое повторение через 1 день
            entry = {
                "repetitions": 0,
                "interval": 1,
                "next_review": self._compute_next_review(1),
                "last_grade": grade,
                "ef": 2.5,  # ease factor
            }
        else:
            entry = self.review_schedule[topic]
            repetitions = entry.get("repetitions", 0)
            interval = entry.get("interval", 1)
            ef = entry.get("ef", 2.5)

            if quality < 3:
                # Плохое запоминание - начать заново
                repetitions = 0
                interval = 1
                ef = 2.5
            else:
                repetitions += 1
                if repetitions == 1:
                    interval = 1
                elif repetitions == 2:
                    interval = 3
                else:
                    # Увеличить интервал на основе коэффициента легкости (EF)
                    new_ef = ef + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
                    new_ef = max(1.3, new_ef)
                    entry["ef"] = new_ef
                    interval = max(1, int(interval * new_ef))
                entry["repetitions"] = repetitions
                entry["interval"] = interval

            entry["next_review"] = self._compute_next_review(interval)
            entry["last_grade"] = grade

        self.review_schedule[topic] = entry

    def get_due_reviews(self) -> list[dict[str, Any]]:
        """Получить список тем, готовых к повторению (next_review <= сейчас).

        Returns:
            list[dict] с полями: topic, interval, repetitions, отсортированный по дате
        """
        import time

        now = time.time()
        due = []
        for topic, entry in self.review_schedule.items():
            if entry.get("next_review", 0) <= now:
                due.append(
                    {
                        "topic": topic,
                        "interval": entry.get("interval", 0),
                        "repetitions": entry.get("repetitions", 0),
                    }
                )
        due.sort(key=lambda x: self.review_schedule[x["topic"]]["next_review"])
        return due

    def mark_reviewed(self, topic: str, grade: float, max_grade: float = 10.0):
        """Отметить повторение как завершённое и запланировать следующее."""
        self.schedule_review(topic, grade, max_grade)

    def clear_review_schedule(self):
        """Очистить всё расписание повторений."""
        self.review_schedule = {}

    def reset_course(self):
        """Сбросить прогресс курса"""
        self.learning.reset_course()

    def set_course(self, course_id: str):
        """Установить текущий курс"""
        self.learning.set_course(course_id)

    def next_topic(self):
        """Следующая тема"""
        self.learning.next_topic()

    def set_learning_context(self, course=None, topic=None, lab=None, action=None):
        """Установить контекст обучения"""
        self.learning.set_learning_context(course=course, topic=topic, lab=lab, action=action)

    def get_learning_context(self) -> dict[str, Any]:
        """Получить контекст обучения"""
        return self.learning.get_learning_context()

    def set_persona(self, persona: str):
        """Установить текущую персону (teacher, expert, ctf, review)"""
        self.persona.set_persona(persona)
        # Также обновляем режим для совместимости
        from ui import Mode

        persona_to_mode = {
            "teacher": Mode.TEACHER,
            "expert": Mode.EXPERT,
            "ctf": Mode.CTF,
            "review": Mode.CODE_REVIEW,
        }
        if persona in persona_to_mode:
            self.current_mode = (
                persona_to_mode[persona].value
                if hasattr(persona_to_mode[persona], "value")
                else persona
            )

    def get_persona(self) -> str:
        """Получить текущую персону"""
        return self.persona.current_persona

    def set_active_assignment(self, assignment: dict):
        """Установить активное задание и сбросить собранные флаги"""
        self.active_assignment = assignment
        self.collected_flags = []

    def collect_flag(self, flag: str) -> tuple[bool, int]:
        """Собрать флаг в активном задании. Возвращает (успех, очки)"""
        if self.active_assignment:
            flags = self.active_assignment.get("flags", [])
            if flag in flags and flag not in self.collected_flags:
                self.collected_flags.append(flag)
                total_points = self.active_assignment.get("points", 0)
                per_flag = total_points // len(flags) if flags else total_points
                return True, per_flag
        return False, 0

    def is_assignment_complete(self) -> bool:
        """Проверить, все ли флаги задания собраны"""
        if not self.active_assignment:
            return False
        flags = self.active_assignment.get("flags", [])
        return len(self.collected_flags) >= len(flags)

    def get_assignment_progress(self) -> dict[str, Any]:
        """Получить прогресс по активному заданию"""
        if not self.active_assignment:
            return {}
        flags = self.active_assignment.get("flags", [])
        total = len(flags)
        collected = len(self.collected_flags)
        per_flag = self.active_assignment.get("points", 0) // total if total else 0
        earned = per_flag * collected
        return {
            "id": self.active_assignment.get("id"),
            "title": self.active_assignment.get("title"),
            "total_flags": total,
            "collected_flags": collected,
            "remaining": total - collected,
            "points_earned": earned,
        }

    # === RISK LEVEL (CTF/Story mode) ===
    def increase_risk(self, amount: int = 10):
        """Увеличить уровень риска (при ошибке/срабатывании защиты)"""
        self.risk.increase_risk(amount)
        self.check_achievements()

    def decrease_risk(self, amount: int = 5):
        """Уменьшить уровень риска (при успехе)"""
        self.risk.decrease_risk(amount)
        self.check_achievements()

    def reset_risk(self):
        """Сбросить уровень риска"""
        self.risk.reset_risk()

    def get_risk_status(self) -> str:
        """Получить текстовый статус риска"""
        return self.risk.get_risk_status()

    def get_xp_multiplier(self) -> float:
        """Возвращает текущий множитель XP с учетом активного буста."""
        return self.shop.get_xp_multiplier()

    def apply_item_effect(self, item: dict) -> None:
        """Применить эффект купленного предмета к состоянию."""
        self.shop.apply_item_effect(item)

    # === СТАТИСТИКА ===
    def increment_flag(self):
        """Увеличить счётчик собранных флагов"""
        self.achievements.increment_flag()
        self.check_achievements()

    def complete_assignment(self):
        """Отметить выполнение задания"""
        self.achievements.complete_assignment()
        self.check_achievements()

    def start_lab(self):
        """Отметить запуск лаборатории"""
        self.achievements.start_lab()
        self.check_achievements()

    def take_quiz(self):
        """Отметить прохождение квиза"""
        self.achievements.take_quiz()
        self.check_achievements()

    def check_news(self):
        """Отметить проверку новостей"""
        self.achievements.check_news()
        # Не вызываем check_achievements здесь — вызываем в обработчике

    def send_message(self):
        """Увеличить счётчик отправленных сообщений"""
        self.achievements.send_message()
        # Не проверяем достижения для каждого сообщения (слишком часто)

    # === Алиасы для обратной совместимости с тестами ===
    def increment_labs_started(self):
        """Alias for start_lab (for test compatibility)"""
        self.start_lab()

    def increment_messages_sent(self):
        """Alias for send_message (for test compatibility)"""
        self.send_message()

    def increment_news_checked(self):
        """Alias for check_news (for test compatibility)"""
        self.check_news()

    def increment_quizzes_taken(self):
        """Alias for take_quiz (for test compatibility)"""
        self.take_quiz()

    # === НОВЫЕ СЧЁТЧИКИ ДЛЯ РАСШИРЕННЫХ ДОСТИЖЕНИЙ (C-13) ===

    def increment_social_success(self):
        """Увеличить счётчик успешных сценариев социальной инженерии"""
        self.achievements.increment_social_success()
        self.check_achievements()

    def increment_apt_groups_viewed(self):
        """Увеличить счётчик просмотренных досье APT-групп"""
        self.achievements.increment_apt_groups_viewed()
        self.check_achievements()

    def increment_stealth_ops(self):
        """Увеличить счётчик стелс-операций (задания с низким риском)"""
        self.achievements.increment_stealth_ops()
        self.check_achievements()

    def increment_threat_exposures(self):
        """Увеличить счётчик изучения угроз (сводки, анализ)"""
        self.achievements.increment_threat_exposures()
        self.check_achievements()

    def check_achievements(self):
        """Проверить и выдать новые достижения"""
        import json
        import os

        achievements_file = "data/achievements.json"
        if not os.path.exists(achievements_file):
            return []

        try:
            with open(achievements_file, "r", encoding="utf-8") as f:
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
            elif cond_type == "social_success":
                unlocked = self.social_success >= threshold
            elif cond_type == "apt_groups_viewed":
                unlocked = self.apt_groups_viewed >= threshold
            elif cond_type == "stealth_ops":
                unlocked = self.stealth_ops >= threshold
            elif cond_type == "threat_exposures":
                unlocked = self.threat_exposures >= threshold

            if unlocked:
                self.earned_achievements.append(ach_id)
                xp = ach.get("points", 0)
                if xp > 0:
                    self.points += xp * self.get_xp_multiplier()
                newly_earned.append(ach)

        return newly_earned

    # === RATE LIMITING (Q-05) ===

    def can_make_request(
        self, window_seconds: int = 60, max_requests: int = 10
    ) -> bool:
        """Check if a new request is allowed within the rate limit."""
        return self.metrics.can_make_request(window_seconds, max_requests)

    def record_request(self) -> None:
        """Record that a request was made."""
        self.metrics.record_request()

    def track_command_usage(self, command: str) -> None:
        """Отслеживать использование команды (M-31)."""
        self.metrics.track_command_usage(command)

    # === REPUTATION & HANDLES (L-10) ===

    def add_reputation(self, amount: int) -> None:
        """Добавить очки репутации и обновить хэндл."""
        self.user.add_reputation(amount)

    def get_handle(self) -> str:
        """Получить текущий хэндл."""
        return self.user.get_handle()

    # === EXPLANATION DEPTH (L-05) ===

    def set_explanation_depth(self, depth: str) -> str:
        """Установить глубину объяснений: beginner, normal, expert."""
        return self.explanation.set_explanation_depth(depth)

    def get_explanation_depth(self) -> str:
        """Получить текущую глубину объяснений."""
        return self.explanation.get_explanation_depth()

    # === SKILL TRACKER (L-02) ===

    def track_skill(self, skill: str, success: bool, xp: int = 10) -> None:
        """Отследить использование навыка."""
        if skill not in self.skill_tracker:
            self.skill_tracker[skill] = {
                "level": 0,
                "xp": 0,
                "last_practice": time.time(),
                "attempts": 0,
                "successes": 0,
            }
        s = self.skill_tracker[skill]
        s["xp"] += xp
        s["attempts"] += 1
        s["last_practice"] = time.time()
        if success:
            s["successes"] += 1
        # Level up: каждые 50 XP = +1 уровень (макс 5)
        new_level = min(5, s["xp"] // 50)
        if new_level > s["level"]:
            s["level"] = new_level
        self.save_to_file()

    def get_skill_level(self, skill: str) -> int:
        """Получить уровень навыка (0-5)."""
        if skill in self.skill_tracker:
            return self.skill_tracker[skill]["level"]
        return 0

    def get_all_skills(self) -> list[dict[str, Any]]:
        """Получить все навыки с прогрессом."""
        result = []
        for name, data in self.skill_tracker.items():
            result.append({
                "name": name,
                "level": data["level"],
                "xp": data["xp"],
                "attempts": data["attempts"],
                "successes": data["successes"],
                "success_rate": round(data["successes"] / data["attempts"] * 100, 1) if data["attempts"] > 0 else 0,
            })
        return sorted(result, key=lambda x: x["level"], reverse=True)

    # === BACKUP (Q-06) ===

    def maybe_auto_backup(
        self, backup_dir: str = "./backups", max_age_hours: int = 24
    ) -> None:
        """Создать бэкап state и news cache, если последний бэкап старше max_age_hours."""
        os.makedirs(backup_dir, exist_ok=True)
        # Find latest backup of app_state
        state_backups = [
            f
            for f in os.listdir(backup_dir)
            if f.startswith("app_state_") and f.endswith(".json")
        ]
        latest_state_ts = 0
        for fname in state_backups:
            try:
                # Extract timestamp from filename like app_state_2026-03-29_21-58.json
                parts = fname.split("_")
                if len(parts) >= 3:
                    ts_str = parts[2].replace(".json", "")
                    ts = time.mktime(time.strptime(ts_str, "%Y-%m-%d_%H-%M"))
                    latest_state_ts = max(latest_state_ts, ts)
            except Exception:
                continue
        now = time.time()
        if now - latest_state_ts < max_age_hours * 3600:
            return  # recent backup exists

        # Create new backup
        timestamp = time.strftime("%Y-%m-%d_%H-%M")
        state_src = "./memory/app_state.json"
        news_src = "./knowledge_base/news_cache.json"
        if os.path.exists(state_src):
            dst = os.path.join(backup_dir, f"app_state_{timestamp}.json")
            shutil.copy2(state_src, dst)
        if os.path.exists(news_src):
            dst = os.path.join(backup_dir, f"news_cache_{timestamp}.json")
            shutil.copy2(news_src, dst)

    def save_to_file(self, path: str = "./memory/app_state.json"):
        """Сохранить состояние в файл"""
        import json

        state_dict = {
            # Learning
            "current_course": self.current_course,
            "current_topic": self.current_topic,
            "learning_context": self.learning_context,
            "course_progress": self.course_progress,
            # User
            "username": self.username,
            "avatar": self.avatar,
            "reputation": self.reputation,
            "handle": self.handle,
            "htb_email": self.htb_email,
            "htb_password_enc": _encrypt(self.htb_password) if self.htb_password else None,
            "htb_completed": self.htb_completed,
            # Achievements
            "points": self.points,
            "total_flags_collected": self.total_flags_collected,
            "assignments_completed": self.assignments_completed,
            "labs_started": self.labs_started,
            "quizzes_taken": self.quizzes_taken,
            "news_checked": self.news_checked,
            "messages_sent": self.messages_sent,
            "earned_achievements": self.earned_achievements,
            "social_success": self.social_success,
            "apt_groups_viewed": self.apt_groups_viewed,
            "stealth_ops": self.stealth_ops,
            "threat_exposures": self.threat_exposures,
            "xp_boost_multiplier": self.xp_boost_multiplier,
            "xp_boost_expiry": self.xp_boost_expiry,
            # Metrics
            "llm_call_count": self.llm_call_count,
            "llm_total_time": self.llm_total_time,
            "llm_total_tokens": self.llm_total_tokens,
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses,
            "start_time": self.start_time,
            "request_timestamps": self.request_timestamps,
            "command_usage": self.command_usage,
            # Persona
            "current_persona": self.current_persona,
            "current_mode": self.current_mode,
            # Risk
            "risk_level": self.risk_level,
            # Shop
            "owned_themes": self.owned_themes,
            "current_theme": self.current_theme,
            "unlocked_topics": self.unlocked_topics,
            "hint_credits": self.hint_credits,
            "selected_tools": self.selected_tools,
            "trace_deadline": self.trace_deadline,
            "trace_hint": self.trace_hint,
            "missions_completed": self.missions_completed,
            "active_mission": self.active_mission,
            # Hints
            "hint_enabled": self.hint_enabled,
            "hints_used": self.hints_used,
            "last_hint_time": self.last_hint_time,
            "hint_cooldown": self.hint_cooldown,
            # Voice
            "voice_enabled": self.voice_enabled,
            "voice_engine": self.voice_engine,
            "voice_rate": self.voice_rate,
            # Explanation
            "explanation_depth": self.explanation_depth,
            # Direct AppState attributes
            "last_news": self.last_news,
            "active_assignment": self.active_assignment,
            "collected_flags": self.collected_flags,
            "weak_topics": self.weak_topics,
            "review_schedule": self.review_schedule,
            "feature_flags": self.feature_flags,
            "last_writeup_activity": self.last_writeup_activity,
            "writeup_history": self.writeup_history,
            "exploit_success": self.exploit_success,
            "tracks_enrolled": self.tracks_enrolled,
            "track_progress": self.track_progress,
            "bounty_reports": self.bounty_reports,
            "skill_tracker": self.skill_tracker,
            "emotion_mode": self.emotion_mode,
        }
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(state_dict, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.error(f"Не удалось сохранить состояние: {e}")

    def load_from_file(self, path: str = "./memory/app_state.json"):
        """Загрузить состояние из файла"""
        import json

        try:
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                # Learning
                self.current_course = data.get("current_course")
                self.current_topic = data.get("current_topic", 0)
                self.learning_context = data.get("learning_context", self.learning_context)
                self.course_progress = data.get("course_progress", {})
                # User
                self.username = data.get("username", "Аноним")
                self.avatar = data.get("avatar", "🧑‍💻")
                self.reputation = data.get("reputation", 0)
                self.handle = data.get("handle", "Новичок")
                self.htb_email = data.get("htb_email")
                pwd_enc = data.get("htb_password_enc")
                if pwd_enc:
                    self.htb_password = _decrypt(pwd_enc)
                else:
                    self.htb_password = data.get("htb_password")
                self.htb_completed = data.get("htb_completed", [])
                # Achievements
                self.points = data.get("points", 0)
                self.total_flags_collected = data.get("total_flags_collected", 0)
                self.assignments_completed = data.get("assignments_completed", 0)
                self.labs_started = data.get("labs_started", 0)
                self.quizzes_taken = data.get("quizzes_taken", 0)
                self.news_checked = data.get("news_checked", 0)
                self.messages_sent = data.get("messages_sent", 0)
                self.earned_achievements = data.get("earned_achievements", [])
                self.social_success = data.get("social_success", 0)
                self.apt_groups_viewed = data.get("apt_groups_viewed", 0)
                self.stealth_ops = data.get("stealth_ops", 0)
                self.threat_exposures = data.get("threat_exposures", 0)
                self.xp_boost_multiplier = data.get("xp_boost_multiplier", 1.0)
                self.xp_boost_expiry = data.get("xp_boost_expiry", 0.0)
                # Metrics
                self.llm_call_count = data.get("llm_call_count", 0)
                self.llm_total_time = data.get("llm_total_time", 0.0)
                self.llm_total_tokens = data.get("llm_total_tokens", 0)
                self.cache_hits = data.get("cache_hits", 0)
                self.cache_misses = data.get("cache_misses", 0)
                self.start_time = data.get("start_time", time.time())
                self.request_timestamps = data.get("request_timestamps", [])
                self.command_usage = data.get("command_usage", {})
                # Persona
                self.current_persona = data.get("current_persona", "teacher")
                self.current_mode = data.get("current_mode", "teacher")
                # Risk
                self.risk_level = data.get("risk_level", 0)
                # Shop
                self.owned_themes = data.get("owned_themes", [])
                self.current_theme = data.get("current_theme", "default")
                self.unlocked_topics = data.get("unlocked_topics", [])
                self.hint_credits = data.get("hint_credits", 3)
                self.selected_tools = data.get("selected_tools", [])
                self.trace_deadline = data.get("trace_deadline")
                self.trace_hint = data.get("trace_hint")
                self.missions_completed = data.get("missions_completed", [])
                self.active_mission = data.get("active_mission")
                # Hints
                self.hint_enabled = data.get("hint_enabled", True)
                self.hints_used = data.get("hints_used", 0)
                self.last_hint_time = data.get("last_hint_time", 0.0)
                self.hint_cooldown = data.get("hint_cooldown", 30)
                # Voice
                self.voice_enabled = data.get("voice_enabled", False)
                self.voice_engine = data.get("voice_engine", "pyttsx3")
                self.voice_rate = data.get("voice_rate", 200)
                # Explanation
                self.explanation_depth = data.get("explanation_depth", "normal")
                # Direct AppState attributes
                self.last_news = data.get("last_news")
                self.active_assignment = data.get("active_assignment")
                self.collected_flags = data.get("collected_flags", [])
                self.weak_topics = data.get("weak_topics", [])
                self.review_schedule = data.get("review_schedule", {})
                self.feature_flags = data.get("feature_flags", {})
                self.last_writeup_activity = data.get("last_writeup_activity")
                self.writeup_history = data.get("writeup_history", [])
                self.exploit_success = data.get("exploit_success", [])
                self.tracks_enrolled = data.get("tracks_enrolled", [])
                self.track_progress = data.get("track_progress", {})
                self.bounty_reports = data.get("bounty_reports", [])
                self.skill_tracker = data.get("skill_tracker", {})
                self.emotion_mode = data.get("emotion_mode", "neutral")
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.error(f"Не удалось загрузить состояние: {e}")


# Глобальный экземпляр
app_state = AppState()


def get_state() -> AppState:
    """Получить состояние"""
    return app_state
