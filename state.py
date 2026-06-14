"""
Плоское состояние приложения. Все поля доступны напрямую.
"""

import logging
import time
import json
import os
from typing import Any, List, Dict, Optional


class AppState:
    SAVE_DEBOUNCE_SECONDS = 2
    SCHEMA_VERSION = 1

    def __init__(self) -> None:
        self._last_save_time: float = 0.0
        self.schema_version: int = self.SCHEMA_VERSION
        # Прогресс и достижения
        self.xp: float = 0.0
        self.level: int = 1
        self.points: float = 0.0
        self.total_flags_collected: int = 0
        self.assignments_completed: int = 0
        self.labs_started: int = 0
        self.quizzes_taken: int = 0
        self.news_checked: int = 0
        self.messages_sent: int = 0
        self.social_success: int = 0
        self.apt_groups_viewed: int = 0
        self.stealth_ops: int = 0
        self.threat_exposures: int = 0
        self.earned_achievements: List[str] = []
        self.weak_topics: List[Dict[str, Any]] = []
        self.completed_quizzes: List[str] = []
        self.completed_tasks: List[str] = []
        self.skills: Dict[str, Any] = {}
        self.reputation: int = 0
        self.handle: str = "Новичок"
        self.username: str = "Аноним"
        self.avatar: str = "🧑‍💻"

        # Курсы и обучение
        self.current_course: Optional[str] = None
        self.current_topic: int = 0
        self.course_progress: Dict[str, int] = {}
        self.learning_context: Dict[str, Any] = {}

        # Прогресс (для API)
        self.progress: Dict[str, Any] = {}

        # Метрики (для аналитики)
        self.metrics: Dict[str, Any] = {
            "start_time": time.time(),
            "session_count": 0,
        }
        self.achievements: List[str] = []
        self.current_node: Optional[str] = None
        self.loop_count: int = 0

        # XP бусты
        self.xp_boost_multiplier: float = 1.0
        self.xp_boost_expiry: float = 0.0

        # Магазин / предметы
        self.owned_themes: List[str] = []
        self.current_theme: str = "default"
        self.unlocked_topics: List[str] = []
        self.selected_tools: List[str] = []
        self.purchase_history: List[Dict[str, Any]] = []

        # Лаборатории
        self.trace_hint: Optional[str] = None
        self.running_labs: List[str] = []

        # Миссии
        self.missions_completed: List[str] = []
        self.active_mission: Optional[str] = None

        # Треки
        self.tracks_enrolled: List[str] = []
        self.track_progress: Dict[str, Any] = {}

        # Spaced repetition
        self.review_schedule: Dict[str, Any] = {}

        # Context Budget (persisted across sessions)
        self.context_budget: Dict[str, Any] = {}

        # Подсказки
        self.hint_enabled: bool = True
        self.hint_credits: int = 3
        self.hints_used: int = 0
        self.last_hint_time: float = 0.0
        self.hint_cooldown: int = 30

        # Риск
        self.risk_level: int = 0

        # World Stability (Chapter 7)
        self.world_stability: int = 100  # 0-100, снижается от плохих решений

        # Noise / stealth
        self.noise_level: int = 0
        self.stealth_mode: bool = False
        self.stealth_mode_until: float = 0.0

        # Trace
        self.trace_active: bool = False
        self.trace_deadline: Optional[float] = None
        self.trace_target: str = ""

        # Dirty logs
        self.dirty_logs: List[Dict[str, Any]] = []

        # Digital debts
        self.digital_debts: int = 0
        self.debt_details: List[str] = []

        # Factions
        self.faction_reputation: Dict[str, int] = {"rick": 0, "ghost": 0, "archive": 0}
        self.faction_chosen: Optional[str] = None

        # Memory
        self.student_memories: List[str] = []

        # Watchers counterattack
        self.watcher_attack_active: bool = False
        self.watcher_attack_until: float = 0.0
        self.last_watcher_attack: float = 0.0

        # Phantom labs
        self.phantom_labs: List[Dict[str, Any]] = []
        self.phantom_labs_completed: List[str] = []

        # Secret room
        self.secret_room_unlocked: bool = False
        self.secret_room_expires: float = 0.0
        self.secret_room_visited: bool = False
        self.truth_artifact: bool = False

        # Новости
        self.last_news: Optional[str] = None
        self.news_analyzed: int = 0

        # Флаги возможностей
        self.feature_flags: Dict[str, bool] = {}

        # Эмоции
        self.emotion_mode: str = "neutral"

        # Writeups и отчёты
        self.last_writeup_activity: Optional[Dict[str, Any]] = None
        self.writeup_history: List[Dict[str, Any]] = []
        self.bounty_reports: List[Dict[str, Any]] = []

        # CTF, phishing, mermaid
        self.ctf_flags_generated: int = 0
        self.phishing_generated: int = 0
        self.mermaid_views: int = 0

        # Расследования
        self.found_evidence: List[str] = []
        self.current_case: Optional[str] = None

        # Эксплойты
        self.exploit_success: List[Dict[str, Any]] = []
        self.current_challenge: Optional[str] = None

        # Задания
        self.active_assignment: Optional[Dict[str, Any]] = None
        self.collect_flag: Any = None
        self.is_assignment_complete: Any = None

        # Голос
        self.voice_enabled: bool = False
        self.voice_engine: str = "pyttsx3"
        self.voice_rate: int = 200

        # Язык и глубина объяснений
        self.language: str = "ru"
        self.explanation_depth: str = "normal"

        # Метрики LLM
        self.llm_call_count: int = 0
        self.llm_total_time: float = 0.0
        self.llm_total_tokens: int = 0
        self.cache_hits: int = 0
        self.cache_misses: int = 0
        self.start_time: float = time.time()
        self.request_timestamps: List[float] = []
        self.command_usage: Dict[str, int] = {}

        # HTB
        self.htb_token: Optional[str] = None
        self.htb_completed: List[int] = []
        self.htb_email: Optional[str] = None
        self.htb_password: Optional[str] = None

        # THM
        self.thm_username: Optional[str] = None
        self.thm_rooms_cache: Dict[str, Any] = {}
        self.thm_completed: List[Dict[str, str]] = []
        self.thm_points: int = 0
        self.thm_level: int = 1
        self.thm_rank: str = "Новичок"

        # Versus
        self.versus_active: bool = False
        self.versus_scenario: Optional[str] = None
        self.versus_attempts: int = 0
        self.versus_history: List[Dict[str, str]] = []

        # Синхронизация
        self.sync_id: Optional[str] = None

        # Story mode
        self.story_completed: List[int] = []
        self.current_story_episode: Optional[int] = None

        # Chapters
        self.current_chapter: int = 1
        self.chapter_completed: List[int] = []
        self.chapter_artifacts: List[int] = []

        # History timeline
        self.timeline_completed: List[str] = []

        # Memorable events for echo system
        self.memorable_events: List[Dict[str, Any]] = []

        # Adaptive difficulty
        self.difficulty_level: str = "beginner"
        self.tutorial_completed: bool = False
        self.tutorial_step: int = 0

        # Session summary
        self.last_session_summary: Dict[str, Any] = {}

        # Дополнительные внутренние поля
        self._daily_streak: int = 0
        self._offline_mode: bool = False
        self._communication_mood: str = "normal"
        self._completed_cells: List[int] = []
        self._current_notebook: Optional[str] = None
        self._current_mode: str = "teacher"
        self._current_persona: str = "teacher"
        self._msg_count_since_summary: int = 0

        # Ежедневные задания
        self.daily_completed: bool = False
        self.last_daily_date: str = ""
        self.last_daily_idx: int = 0
        self.daily_streak: int = 0
        self.flags_captured: int = 0
        self.ctf_active: bool = False
        self.current_track: Optional[str] = None
        self.current_mission: Optional[str] = None

        # Ранги
        self.HANDLES: List[tuple[int, str]] = [
            (0, "Новичок"),
            (50, "Script Kiddie"),
            (150, "Хакер"),
            (300, "Пентестер"),
            (500, "Эксперт"),
            (800, "Призрак"),
            (1200, "Легенда"),
            (2000, "Фантом"),
        ]

    # ---------- Методы сохранения / загрузки ----------
    @staticmethod
    def _upgrade_state(data: dict) -> dict:
        """Upgrade loaded state dict from older schema versions.

        Mutates data in-place and returns it for convenience.
        """
        loaded_version = data.get("schema_version", 0)
        if loaded_version >= AppState.SCHEMA_VERSION:
            return data

        # v0 → v1: Initial versioning (no actual migration needed yet)
        if loaded_version < 1:
            # schema_version was added; all existing states are v0
            data.setdefault("context_budget", {})
            data.setdefault("schema_version", 1)

        data["schema_version"] = AppState.SCHEMA_VERSION
        return data

    def load_from_file(self, path: str = "./memory/app_state.json") -> None:
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            data = self._upgrade_state(data)
            for key, value in data.items():
                if hasattr(self, key):
                    setattr(self, key, value)
        except FileNotFoundError:
            pass
        except json.JSONDecodeError as e:
            logger = logging.getLogger(__name__)
            logger.error(f"Corrupt state file {path}: {e}")
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.warning(f"Error loading state from {path}: {e}")

    def save_to_file(
        self, path: str = "./memory/app_state.json", force: bool = False
    ) -> None:
        logger = logging.getLogger(__name__)
        try:
            now = time.time()
            if not force and now - self._last_save_time < self.SAVE_DEBOUNCE_SECONDS:
                return
            self._last_save_time = now
            self._trim_unbounded_lists()
            os.makedirs(os.path.dirname(path), exist_ok=True)
            save_dict = {}
            for k, v in self.__dict__.items():
                if k.startswith("_") or k == "HANDLES":
                    continue
                if isinstance(v, (list, dict, str)) and not v:
                    continue
                save_dict[k] = v
            with open(path + ".tmp", "w", encoding="utf-8") as f:
                json.dump(save_dict, f, ensure_ascii=False, indent=2, default=str)
            os.replace(path + ".tmp", path)
        except (TypeError, ValueError, OSError) as e:
            logger.error(f"Failed to save state to {path}: {e}")
            raise
        except Exception as e:
            logger.warning(f"Unexpected error saving state: {e}")

    def _trim_unbounded_lists(self) -> None:
        """Cap unbounded lists to prevent JSON state from growing indefinitely."""
        caps = {
            "exploit_success": 200,
            "bounty_reports": 100,
            "writeup_history": 100,
            "purchase_history": 100,
            "versus_history": 50,
            "htb_completed": 100,
            "thm_completed": 100,
            "weak_topics": 50,
            "missions_completed": 100,
            "story_completed": 100,
            "chapter_completed": 20,
            "chapter_artifacts": 20,
            "timeline_completed": 100,
            "found_evidence": 100,
            "tracks_enrolled": 50,
            "dirty_logs": 100,
            "debt_details": 50,
            "student_memories": 50,
        }
        for field, max_size in caps.items():
            lst = getattr(self, field, None)
            if isinstance(lst, list) and len(lst) > max_size:
                setattr(self, field, lst[-max_size:])

        # Cap command_usage at 50 most-used commands
        if hasattr(self, "command_usage") and isinstance(self.command_usage, dict):
            if len(self.command_usage) > 50:
                sorted_cmds = sorted(
                    self.command_usage.items(), key=lambda x: x[1], reverse=True
                )
                self.command_usage = dict(sorted_cmds[:50])

        # Cap skills at 50 entries
        if hasattr(self, "skills") and isinstance(self.skills, dict):
            if len(self.skills) > 50:
                sorted_skills = sorted(
                    self.skills.items(),
                    key=lambda x: x[1].get("xp", 0) if isinstance(x[1], dict) else 0,
                    reverse=True,
                )
                self.skills = dict(sorted_skills[:50])

        # Cap request_timestamps at 100 (absolute safety net)
        if hasattr(self, "request_timestamps") and isinstance(
            self.request_timestamps, list
        ):
            if len(self.request_timestamps) > 100:
                self.request_timestamps = self.request_timestamps[-100:]

    def maybe_auto_backup(
        self, backup_dir: str = "", max_age_hours: int = 0, max_backups: int = 5
    ) -> None:
        """Автоматическое резервное копирование с ротацией по количеству и возрасту."""
        self.save_to_file()
        backup_path = backup_dir or "./memory/backups"
        os.makedirs(backup_path, exist_ok=True)
        # Create timestamped backup
        import shutil
        from datetime import datetime

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        src = "./memory/app_state.json"
        if os.path.exists(src):
            dst = os.path.join(backup_path, f"app_state_{ts}.json")
            try:
                shutil.copy2(src, dst)
            except (OSError, IOError, shutil.Error):
                pass
        # Rotate: keep only max_backups newest
        if max_backups > 0 and os.path.isdir(backup_path):
            backups = sorted(
                [f for f in os.listdir(backup_path) if f.endswith(".json")],
                key=lambda f: os.path.getmtime(os.path.join(backup_path, f)),
                reverse=True,
            )
            for old in backups[max_backups:]:
                try:
                    os.remove(os.path.join(backup_path, old))
                except (OSError, IOError):
                    pass
        # Rotate: delete backups older than max_age_hours
        if max_age_hours > 0 and os.path.isdir(backup_path):
            now = time.time()
            max_age_seconds = max_age_hours * 3600
            for f in os.listdir(backup_path):
                if f.endswith(".json"):
                    path = os.path.join(backup_path, f)
                    try:
                        mtime = os.path.getmtime(path)
                        if now - mtime > max_age_seconds:
                            os.remove(path)
                    except (OSError, IOError):
                        pass

    # ---------- Методы для работы со слабыми темами ----------
    def get_weak_topics(self, threshold: float = 70.0) -> List[Dict[str, Any]]:
        return [wt for wt in self.weak_topics if wt.get("success_rate", 0) < threshold]

    def get_due_reviews(self) -> List[Any]:
        from services.spaced_repetition_service import get_due_reviews as _get_due

        return _get_due(self.review_schedule)

    def update_weak_topic(self, topic: str, success_rate: float) -> None:
        from services.weak_topics_service import update_weak_topic as _update

        _update(self.weak_topics, topic, success_rate, 100.0)

    def schedule_review(
        self, topic: str, grade: float, max_grade: float = 10.0
    ) -> None:
        from services.spaced_repetition_service import schedule_review as _schedule

        _schedule(self.review_schedule, topic, grade, max_grade)

    def get_next_weak_topic(self, threshold: float = 70.0) -> Optional[str]:
        weak = self.get_weak_topics(threshold)
        if not weak:
            return None
        weak.sort(key=lambda x: x["success_rate"])
        result: str = weak[0]["topic"]
        return result

    # ---------- Другие методы ----------
    def track_command_usage(self, command: str) -> None:
        self.command_usage[command] = self.command_usage.get(command, 0) + 1

    def can_make_request(
        self, window_seconds: int = 60, max_requests: int = 10
    ) -> bool:
        now = time.time()
        self.request_timestamps = [
            ts for ts in self.request_timestamps if now - ts < window_seconds
        ]
        return len(self.request_timestamps) < max_requests

    def record_request(self) -> None:
        self.request_timestamps.append(time.time())
        if len(self.request_timestamps) > 100:
            self.request_timestamps = self.request_timestamps[-100:]

    def send_message(self) -> None:
        self.messages_sent += 1

    def get_xp_multiplier(self) -> float:
        now = time.time()
        if self.xp_boost_expiry > 0 and now < self.xp_boost_expiry:
            return self.xp_boost_multiplier
        self.xp_boost_multiplier = 1.0
        self.xp_boost_expiry = 0.0
        return 1.0

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

    def get_learning_context(self) -> Dict[str, Any]:
        return self.learning_context

    def set_learning_context(
        self, course=None, topic=None, lab=None, action=None
    ) -> None:
        if course:
            self.learning_context["current_course"] = course
        if topic:
            self.learning_context["current_topic"] = topic
        if lab:
            self.learning_context["current_lab"] = lab
        if action:
            self.learning_context["last_action"] = action

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

    def apply_item_effect(self, item: Dict[str, Any]) -> Optional[str]:
        item_type = item.get("type")
        if item_type == "theme":
            theme_id = item.get("value")
            if theme_id and theme_id not in self.owned_themes:
                self.owned_themes.append(theme_id)
                return "theme"
        elif item_type == "unlock_topic":
            topic = item.get("value")
            if topic and topic not in self.unlocked_topics:
                self.unlocked_topics.append(topic)
                return "unlock_topic"
        elif item_type == "xp_boost":
            self.apply_xp_boost(
                item.get("multiplier", 2.0), item.get("duration_hours", 1)
            )
            return "xp_boost"
        elif item_type == "consumable" and item.get("effect") == "hint_credit":
            self.hint_credits += item.get("quantity", 1)
            return "hint_credit"
        return None

    def check_achievements(self) -> List[str]:
        """Check achievements using comprehensive achievement_service (rule-based, no LLM)."""
        try:
            from services.achievement_service import check_achievements as _check_all

            state_getter = lambda attr: getattr(self, attr, 0)
            state_setter = lambda attr, val: setattr(self, attr, val)
            newly = _check_all(self.earned_achievements, state_getter, state_setter)
            result = [a.get("id", "") for a in newly]
            if result:
                try:
                    from episode_memory import get_episode_memory

                    mem = get_episode_memory()
                    for a in newly:
                        mem.record(
                            "milestone",
                            f"Achievement: {a.get('name', a.get('id', '?'))}",
                            f"+{a.get('points', 0)} XP",
                            importance=9,
                        )
                except (ImportError, RuntimeError):
                    pass
            return result
        except (FileNotFoundError, json.JSONDecodeError, ValueError, OSError):
            new_achievements = []
            if (
                self.quizzes_taken >= 10
                and "quiz_master" not in self.earned_achievements
            ):
                self.earned_achievements.append("quiz_master")
                new_achievements.append("quiz_master")
            return new_achievements

    def track_skill(self, skill_id: str, success: bool, xp: int) -> None:
        if skill_id not in self.skills:
            self.skills[skill_id] = {"xp": 0, "attempts": 0, "successes": 0}
        old_level = self.get_skill_level(skill_id)
        self.skills[skill_id]["xp"] += xp if success else xp // 2
        self.skills[skill_id]["attempts"] += 1
        if success:
            self.skills[skill_id]["successes"] += 1
        new_level = self.get_skill_level(skill_id)
        if new_level > old_level:
            try:
                from episode_memory import get_episode_memory

                mem = get_episode_memory()
                mem.record(
                    "breakthrough",
                    f"Skill leveled up: {skill_id}",
                    f"Level {old_level} → {new_level}",
                    importance=7,
                )
            except (ImportError, RuntimeError):
                pass

    def get_skill_level(self, skill_id: str) -> int:
        data = self.skills.get(skill_id, {"xp": 0})
        xp = data["xp"]
        if xp < 100:
            return 1
        if xp < 300:
            return 2
        if xp < 600:
            return 3
        return 4

    def get_all_skills(self) -> Dict[str, Any]:
        return self.skills

    def get_explanation_depth(self) -> str:
        return self.explanation_depth

    def set_explanation_depth(self, depth: str) -> None:
        if depth in ("beginner", "normal", "expert"):
            self.explanation_depth = depth

    def add_reputation(self, amount: int) -> None:
        self.reputation += amount
        new_handle = self.get_handle()
        if new_handle != self.handle:
            self.handle = new_handle

    def record_memorable_event(
        self, action: str, result: str = "", issue: str = ""
    ) -> None:
        """Record a significant event for the echo system (max 7 events)."""
        event = {
            "action": action,
            "result": result,
            "issue": issue,
            "timestamp": time.time(),
        }
        self.memorable_events.append(event)
        if len(self.memorable_events) > 7:
            self.memorable_events = self.memorable_events[-7:]

    def get_handle(self) -> str:
        handle = "Новичок"
        for threshold, name in self.HANDLES:
            if self.reputation >= threshold:
                handle = name
        return handle

    def get_htb_password_encrypted(self) -> Optional[str]:
        return None

    def set_htb_password_from_encrypted(self, encrypted: Optional[str]) -> None:
        pass

    @property
    def daily_streak(self) -> int:
        return self._daily_streak

    @daily_streak.setter
    def daily_streak(self, value: int) -> None:
        self._daily_streak = value

    @property
    def offline_mode(self) -> bool:
        return self._offline_mode

    @offline_mode.setter
    def offline_mode(self, value: bool) -> None:
        self._offline_mode = value

    @property
    def communication_mood(self) -> str:
        return self._communication_mood

    @communication_mood.setter
    def communication_mood(self, value: str) -> None:
        self._communication_mood = value

    @property
    def completed_cells(self) -> List[int]:
        return self._completed_cells

    @completed_cells.setter
    def completed_cells(self, value: List[int]) -> None:
        self._completed_cells = value

    @property
    def current_notebook(self) -> Optional[str]:
        return self._current_notebook

    @current_notebook.setter
    def current_notebook(self, value: Optional[str]) -> None:
        self._current_notebook = value

    @property
    def current_mode(self) -> str:
        return self._current_mode

    @current_mode.setter
    def current_mode(self, value: str) -> None:
        self._current_mode = value

    # World Stability (Chapter 7)
    def adjust_world_stability(self, amount: int) -> None:
        """Adjust world stability (-100 to +100). Negative = bad decisions."""
        self.world_stability = max(0, min(100, self.world_stability + amount))

    def get_world_stability_status(self) -> str:
        """Get human-readable world stability status."""
        if self.world_stability >= 80:
            return "🟢 Стабилен"
        elif self.world_stability >= 50:
            return "🟡 Нестабилен"
        elif self.world_stability >= 20:
            return "🟠 Критичен"
        return "🔴 Коллапс"

    def is_teacher_sleeping(self) -> bool:
        """Check if it's 4 AM (teacher sleep time)."""
        import time
        local_hour = time.localtime().tm_hour
        return local_hour == 4

    def get_teacher_sleep_status(self) -> str:
        """Get teacher sleep status."""
        if self.is_teacher_sleeping():
            return "😴 Учитель спит (4:00). Доступен /logs secret."
        return "🟢 Учитель на связи"

    def can_access_secret_logs(self) -> bool:
        """Check if user can access /logs secret (only at 4 AM)."""
        return self.is_teacher_sleeping()


_state: Optional[AppState] = None


def get_state() -> AppState:
    global _state
    if _state is None:
        _state = AppState()
    return _state
