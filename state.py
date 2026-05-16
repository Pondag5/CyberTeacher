"""
🔐 Состояние приложения - глобальные переменные в одном месте
"""

import logging
import os
import shutil
import time
from dataclasses import dataclass, field
from typing import Any

from utils.security import (
    decrypt_value as _decrypt,
    encrypt_value as _encrypt,
    is_encrypted,
)

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

    # Learning state properties
    @property
    def current_course(self) -> str | None:
        return self.learning.current_course

    @current_course.setter
    def current_course(self, value: str | None):
        self.learning.current_course = value

    @property
    def current_topic(self) -> str | None:
        return self.learning.current_topic

    @current_topic.setter
    def current_topic(self, value: str | None):
        self.learning.current_topic = value

    @property
    def course_progress(self) -> dict[str, Any]:
        return self.learning.course_progress

    @course_progress.setter
    def course_progress(self, value: dict[str, Any]):
        self.learning.course_progress = value

    @property
    def learning_context(self) -> dict[str, Any]:
        return self.learning.learning_context

    @learning_context.setter
    def learning_context(self, value: dict[str, Any]):
        self.learning.learning_context = value

    # Achievements state properties
    @property
    def total_flags_collected(self) -> int:
        return self.achievements.total_flags_collected

    @total_flags_collected.setter
    def total_flags_collected(self, value: int):
        self.achievements.total_flags_collected = value

    @property
    def assignments_completed(self) -> int:
        return self.achievements.assignments_completed

    @assignments_completed.setter
    def assignments_completed(self, value: int):
        self.achievements.assignments_completed = value

    @property
    def labs_started(self) -> int:
        return self.achievements.labs_started

    @labs_started.setter
    def labs_started(self, value: int):
        self.achievements.labs_started = value

    @property
    def quizzes_taken(self) -> int:
        return self.achievements.quizzes_taken

    @quizzes_taken.setter
    def quizzes_taken(self, value: int):
        self.achievements.quizzes_taken = value

    @property
    def news_checked(self) -> int:
        return self.achievements.news_checked

    @news_checked.setter
    def news_checked(self, value: int):
        self.achievements.news_checked = value

    @property
    def messages_sent(self) -> int:
        return self.achievements.messages_sent

    @messages_sent.setter
    def messages_sent(self, value: int):
        self.achievements.messages_sent = value

    @property
    def earned_achievements(self) -> list[str]:
        return self.achievements.earned_achievements

    @earned_achievements.setter
    def earned_achievements(self, value: list[str]):
        self.achievements.earned_achievements = value

    @property
    def social_success(self) -> int:
        return self.achievements.social_success

    @social_success.setter
    def social_success(self, value: int):
        self.achievements.social_success = value

    @property
    def apt_groups_viewed(self) -> int:
        return self.achievements.apt_groups_viewed

    @apt_groups_viewed.setter
    def apt_groups_viewed(self, value: int):
        self.achievements.apt_groups_viewed = value

    @property
    def stealth_ops(self) -> int:
        return self.achievements.stealth_ops

    @stealth_ops.setter
    def stealth_ops(self, value: int):
        self.achievements.stealth_ops = value

    @property
    def threat_exposures(self) -> int:
        return self.achievements.threat_exposures

    @threat_exposures.setter
    def threat_exposures(self, value: int):
        self.achievements.threat_exposures = value

    @property
    def points(self) -> float:
        return self.achievements.points

    @points.setter
    def points(self, value: float):
        self.achievements.points = value

    @property
    def xp_boost_multiplier(self) -> float:
        # Prefer shop state for XP boost as it's more specific to shop items
        return self.shop.xp_boost_multiplier

    @xp_boost_multiplier.setter
    def xp_boost_multiplier(self, value: float):
        # Set in both achievements and shop for backward compatibility
        self.achievements.xp_boost_multiplier = value
        self.shop.xp_boost_multiplier = value

    @property
    def xp_boost_expiry(self) -> float:
        # Prefer shop state for XP boost as it's more specific to shop items
        return self.shop.xp_boost_expiry

    @xp_boost_expiry.setter
    def xp_boost_expiry(self, value: float):
        # Set in both achievements and shop for backward compatibility
        self.achievements.xp_boost_expiry = value
        self.shop.xp_boost_expiry = value

    # Metrics state properties
    @property
    def llm_call_count(self) -> int:
        return self.metrics.llm_call_count

    @llm_call_count.setter
    def llm_call_count(self, value: int):
        self.metrics.llm_call_count = value

    @property
    def llm_total_time(self) -> float:
        return self.metrics.llm_total_time

    @llm_total_time.setter
    def llm_total_time(self, value: float):
        self.metrics.llm_total_time = value

    @property
    def llm_total_tokens(self) -> int:
        return self.metrics.llm_total_tokens

    @llm_total_tokens.setter
    def llm_total_tokens(self, value: int):
        self.metrics.llm_total_tokens = value

    @property
    def cache_hits(self) -> int:
        return self.metrics.cache_hits

    @cache_hits.setter
    def cache_hits(self, value: int):
        self.metrics.cache_hits = value

    @property
    def cache_misses(self) -> int:
        return self.metrics.cache_misses

    @cache_misses.setter
    def cache_misses(self, value: int):
        self.metrics.cache_misses = value

    @property
    def start_time(self) -> float:
        return self.metrics.start_time

    @start_time.setter
    def start_time(self, value: float):
        self.metrics.start_time = value

    @property
    def request_timestamps(self) -> list[float]:
        return self.metrics.request_timestamps

    @request_timestamps.setter
    def request_timestamps(self, value: list[float]):
        self.metrics.request_timestamps = value

    @property
    def command_usage(self) -> dict[str, int]:
        return self.metrics.command_usage

    @command_usage.setter
    def command_usage(self, value: dict[str, int]):
        self.metrics.command_usage = value

    # User state properties
    @property
    def username(self) -> str:
        return self.user.username

    @username.setter
    def username(self, value: str):
        self.user.username = value

    @property
    def avatar(self) -> str:
        return self.user.avatar

    @avatar.setter
    def avatar(self, value: str):
        self.user.avatar = value

    @property
    def reputation(self) -> int:
        return self.user.reputation

    @reputation.setter
    def reputation(self, value: int):
        self.user.reputation = value

    @property
    def handle(self) -> str:
        return self.user.handle

    @handle.setter
    def handle(self, value: str):
        self.user.handle = value

    @property
    def htb_email(self) -> str | None:
        return self.user.htb_email

    @htb_email.setter
    def htb_email(self, value: str | None):
        self.user.htb_email = value

    @property
    def htb_password(self) -> str | None:
        return self.user.htb_password

    @htb_password.setter
    def htb_password(self, value: str | None):
        self.user.htb_password = value

    @property
    def htb_completed(self) -> list[str]:
        return self.user.htb_completed

    @htb_completed.setter
    def htb_completed(self, value: list[str]):
        self.user.htb_completed = value

    # Shop state properties
    @property
    def owned_themes(self) -> list[str]:
        return self.shop.owned_themes

    @owned_themes.setter
    def owned_themes(self, value: list[str]):
        self.shop.owned_themes = value

    @property
    def current_theme(self) -> str:
        return self.shop.current_theme

    @current_theme.setter
    def current_theme(self, value: str):
        self.shop.current_theme = value

    @property
    def unlocked_topics(self) -> list[str]:
        return self.shop.unlocked_topics

    @unlocked_topics.setter
    def unlocked_topics(self, value: list[str]):
        self.shop.unlocked_topics = value

    @property
    def hint_credits(self) -> int:
        return self.shop.hint_credits

    @hint_credits.setter
    def hint_credits(self, value: int):
        self.shop.hint_credits = value

    @property
    def selected_tools(self) -> list[str]:
        return self.shop.selected_tools

    @selected_tools.setter
    def selected_tools(self, value: list[str]):
        self.shop.selected_tools = value

    @property
    def trace_deadline(self) -> float | None:
        return self.shop.trace_deadline

    @trace_deadline.setter
    def trace_deadline(self, value: float | None):
        self.shop.trace_deadline = value

    @property
    def trace_hint(self) -> str | None:
        return self.shop.trace_hint

    @trace_hint.setter
    def trace_hint(self, value: str | None):
        self.shop.trace_hint = value

    @property
    def missions_completed(self) -> int:
        return self.shop.missions_completed

    @missions_completed.setter
    def missions_completed(self, value: int):
        self.shop.missions_completed = value

    @property
    def active_mission(self) -> dict[str, Any] | None:
        return self.shop.active_mission

    @active_mission.setter
    def active_mission(self, value: dict[str, Any] | None):
        self.shop.active_mission = value

    # Risk state properties
    @property
    def risk_level(self) -> int:
        return self.risk.risk_level

    @risk_level.setter
    def risk_level(self, value: int):
        self.risk.risk_level = value

    # Voice state properties
    @property
    def voice_enabled(self) -> bool:
        return self.voice.voice_enabled

    @voice_enabled.setter
    def voice_enabled(self, value: bool):
        self.voice.voice_enabled = value

    @property
    def voice_engine(self) -> str:
        return self.voice.voice_engine

    @voice_engine.setter
    def voice_engine(self, value: str):
        self.voice.voice_engine = value

    @property
    def voice_rate(self) -> int:
        return self.voice.voice_rate

    @voice_rate.setter
    def voice_rate(self, value: int):
        self.voice.voice_rate = value

    # Persona state properties
    @property
    def current_persona(self) -> str:
        return self.persona.current_persona

    @current_persona.setter
    def current_persona(self, value: str):
        self.persona.current_persona = value

    @property
    def current_mode(self) -> str:
        return self.persona.current_mode

    @current_mode.setter
    def current_mode(self, value: str):
        self.persona.current_mode = value

    # Hints state properties
    @property
    def hint_enabled(self) -> bool:
        return self.hints.hint_enabled

    @hint_enabled.setter
    def hint_enabled(self, value: bool):
        self.hints.hint_enabled = value

    @property
    def hints_used(self) -> int:
        return self.hints.hints_used

    @hints_used.setter
    def hints_used(self, value: int):
        self.hints.hints_used = value

    @property
    def last_hint_time(self) -> float:
        return self.hints.last_hint_time

    @last_hint_time.setter
    def last_hint_time(self, value: float):
        self.hints.last_hint_time = value

    @property
    def hint_cooldown(self) -> int:
        return self.hints.hint_cooldown

    @hint_cooldown.setter
    def hint_cooldown(self, value: int):
        self.hints.hint_cooldown = value

    # Explanation state properties
    @property
    def explanation_depth(self) -> str:
        return self.explanation.explanation_depth

    @explanation_depth.setter
    def explanation_depth(self, value: str):
        self.explanation.explanation_depth = value

    def __setattr__(self, name: str, value: Any) -> None:
        """Set direct attributes for backward compatibility"""
        # These are direct attributes not covered by explicit properties
        direct_attrs = {
            "last_news",
            "active_assignment",
            "collected_flags",
            "weak_topics",
            "review_schedule",
            "feature_flags",
            "last_writeup_activity",
            "writeup_history",
            "exploit_success",
            "tracks_enrolled",
            "track_progress",
            "bounty_reports",
            "skill_tracker",
            "emotion_mode",
            # Modules themselves
            "achievements",
            "explanation",
            "hints",
            "learning",
            "metrics",
            "persona",
            "risk",
            "shop",
            "user",
            "voice",
        }

        if name in direct_attrs:
            object.__setattr__(self, name, value)
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
        self.learning.set_learning_context(
            course=course, topic=topic, lab=lab, action=action
        )

    def get_learning_context(self) -> dict[str, Any]:
        """Получить контекст обучения"""
        return self.learning.get_learning_context()

    def set_persona(self, persona: str):
        """Установить текущую персону (teacher, expert, ctf, review)"""
        self.persona.set_persona(persona)
        # Также обновляем режим для совместимости
        from shared_types import Mode

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
        """Проверить и выдать новые достижения через сервис"""
        from services.achievement_service import check_achievements

        def state_getter(name: str):
            if name == "xp_multiplier":
                return self.get_xp_multiplier()
            return getattr(self, name)

        def state_setter(name: str, value):
            setattr(self, name, value)

        return check_achievements(
            self.earned_achievements,
            state_getter,
            state_setter,
        )

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
            result.append(
                {
                    "name": name,
                    "level": data["level"],
                    "xp": data["xp"],
                    "attempts": data["attempts"],
                    "successes": data["successes"],
                    "success_rate": round(data["successes"] / data["attempts"] * 100, 1)
                    if data["attempts"] > 0
                    else 0,
                }
            )
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
            "htb_password_enc": _encrypt(self.htb_password)
            if self.htb_password
            else None,
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
        """Загрузить состояние из файла с Pydantic валидацией"""
        import json
        from state_models import AppStateModel

        try:
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    raw_data = json.load(f)

                # Валидация данных через Pydantic
                validated = AppStateModel.model_validate(raw_data)

                # Learning
                self.current_course = validated.current_course
                self.current_topic = validated.current_topic
                self.learning_context = validated.learning_context
                self.course_progress = validated.course_progress
                # User
                self.username = validated.username
                self.avatar = validated.avatar
                self.reputation = validated.reputation
                self.handle = validated.handle
                self.htb_email = validated.htb_email
                pwd_enc = validated.htb_password_enc
                if pwd_enc:
                    self.htb_password = _decrypt(pwd_enc)
                else:
                    self.htb_password = validated.htb_password
                self.htb_completed = validated.htb_completed
                # Achievements
                self.points = validated.points
                self.total_flags_collected = validated.total_flags_collected
                self.assignments_completed = validated.assignments_completed
                self.labs_started = validated.labs_started
                self.quizzes_taken = validated.quizzes_taken
                self.news_checked = validated.news_checked
                self.messages_sent = validated.messages_sent
                self.earned_achievements = validated.earned_achievements
                self.social_success = validated.social_success
                self.apt_groups_viewed = validated.apt_groups_viewed
                self.stealth_ops = validated.stealth_ops
                self.threat_exposures = validated.threat_exposures
                self.xp_boost_multiplier = validated.xp_boost_multiplier
                self.xp_boost_expiry = validated.xp_boost_expiry
                # Metrics
                self.llm_call_count = validated.llm_call_count
                self.llm_total_time = validated.llm_total_time
                self.llm_total_tokens = validated.llm_total_tokens
                self.cache_hits = validated.cache_hits
                self.cache_misses = validated.cache_misses
                self.start_time = validated.start_time
                self.request_timestamps = validated.request_timestamps
                self.command_usage = validated.command_usage
                # Persona
                self.current_persona = validated.current_persona
                self.current_mode = validated.current_mode
                # Risk
                self.risk_level = validated.risk_level
                # Shop
                self.owned_themes = validated.owned_themes
                self.current_theme = validated.current_theme
                self.unlocked_topics = validated.unlocked_topics
                self.hint_credits = validated.hint_credits
                self.selected_tools = validated.selected_tools
                self.trace_deadline = validated.trace_deadline
                self.trace_hint = validated.trace_hint
                self.missions_completed = validated.missions_completed
                self.active_mission = validated.active_mission
                # Hints
                self.hint_enabled = validated.hint_enabled
                self.hints_used = validated.hints_used
                self.last_hint_time = validated.last_hint_time
                self.hint_cooldown = validated.hint_cooldown
                # Voice
                self.voice_enabled = validated.voice_enabled
                self.voice_engine = validated.voice_engine
                self.voice_rate = validated.voice_rate
                # Explanation
                self.explanation_depth = validated.explanation_depth
                # Direct AppState attributes
                self.last_news = validated.last_news
                self.active_assignment = validated.active_assignment
                self.collected_flags = validated.collected_flags
                self.weak_topics = validated.weak_topics
                self.review_schedule = validated.review_schedule
                self.feature_flags = validated.feature_flags
                self.last_writeup_activity = validated.last_writeup_activity
                self.writeup_history = validated.writeup_history
                self.exploit_success = validated.exploit_success
                self.tracks_enrolled = validated.tracks_enrolled
                self.track_progress = validated.track_progress
                self.bounty_reports = validated.bounty_reports
                self.skill_tracker = validated.skill_tracker
                self.emotion_mode = validated.emotion_mode
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.error(f"Не удалось загрузить состояние: {e}")


# Глобальный экземпляр
app_state = AppState()


def get_state() -> AppState:
    """Получить состояние"""
    return app_state
