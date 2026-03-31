"""
🎯 Path-based Learning Tracks - структурированные траектории обучения
Модуль для управления учебными путями (tracks) и адаптивного подбора.
"""

import logging
import os
from dataclasses import dataclass, field

import yaml

logger = logging.getLogger(__name__)

# Путь к директории с треками
TRACKS_DIR = "./tracks"


@dataclass
class TrackTopic:
    """Единица темы в треке"""

    topic_id: str
    order: int
    title: str
    description: str
    required: bool = True  # обязательна ли для прохождения трека
    linked_course: str | None = None  # опционально: связанный курс
    linked_topic: str | None = None  # опционально: конкретная тема курса
    quiz_topic: str | None = None  # квиз для проверки
    lab_id: str | None = None  # лаборатория для практики
    min_score: float = 70.0  # минимальный балл для завершения


@dataclass
class Track:
    """Учебный трек - последовательность тем для изучения"""

    id: str
    name: str
    description: str
    level: str  # beginner, intermediate, advanced
    prerequisites: list[str] = field(
        default_factory=list
    )  # ID треков, которые нужно пройти сначала
    topics: list[TrackTopic] = field(default_factory=list)
    adaptive: bool = False  # может ли трек адаптироваться к слабым темам
    estimated_hours: int = 1

    def get_next_topic(
        self, completed_topics: list[str], current_idx: int
    ) -> TrackTopic | None:
        """Получить следующую тему для изучения"""
        if current_idx >= len(self.topics):
            return None

        # Если есть адаптация, проверим, не нужно ли пропустить какую-то тему
        if self.adaptive:
            # Пока просто возвращаем по порядку, потом можно добавить пропуск пройденных
            pass

        topic = self.topics[current_idx]
        if topic.topic_id in completed_topics:
            # Эта тема уже пройдена, вернём следующую
            return self.get_next_topic(completed_topics, current_idx + 1)
        return topic

    def get_topic_by_id(self, topic_id: str) -> TrackTopic | None:
        """Найти тему по ID"""
        for topic in self.topics:
            if topic.topic_id == topic_id:
                return topic
        return None

    def is_completed(self, completed_topics: list[str]) -> bool:
        """Проверить, все ли обязательные темы пройдены"""
        required_ids = [t.topic_id for t in self.topics if t.required]
        return all(tid in completed_topics for tid in required_ids)

    def progress(self, completed_topics: list[str]) -> tuple[int, int]:
        """Вернуть (пройдено, всего)"""
        required_ids = [t.topic_id for t in self.topics if t.required]
        completed = sum(1 for tid in required_ids if tid in completed_topics)
        return completed, len(required_ids)


class TrackEngine:
    """Движок управления треками"""

    def __init__(self, tracks_dir: str = TRACKS_DIR):
        self.tracks_dir = tracks_dir
        self.tracks: dict[str, Track] = {}
        self.load_all_tracks()

    def load_all_tracks(self) -> None:
        """Загрузить все треки из YAML файлов"""
        if not os.path.exists(self.tracks_dir):
            logger.warning(f"Директория треков не найдена: {self.tracks_dir}")
            return

        for fname in os.listdir(self.tracks_dir):
            if fname.endswith((".yaml", ".yml")):
                try:
                    track = self._load_track_from_file(
                        os.path.join(self.tracks_dir, fname)
                    )
                    if track:
                        self.tracks[track.id] = track
                        logger.info(f"Трек загружен: {track.name} ({track.id})")
                except Exception as e:
                    logger.error(f"Ошибка загрузки трека {fname}: {e}")

    def _load_track_from_file(self, path: str) -> Track | None:
        """Загрузить один трек из YAML файла"""
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)

            if not data:
                return None

            # Парсим темы
            topics = []
            for tdata in data.get("topics", []):
                topic = TrackTopic(
                    topic_id=tdata["topic_id"],
                    order=tdata["order"],
                    title=tdata["title"],
                    description=tdata.get("description", ""),
                    required=tdata.get("required", True),
                    linked_course=tdata.get("linked_course"),
                    linked_topic=tdata.get("linked_topic"),
                    quiz_topic=tdata.get("quiz_topic"),
                    lab_id=tdata.get("lab_id"),
                    min_score=tdata.get("min_score", 70.0),
                )
                topics.append(topic)

            # Сортируем по порядку
            topics.sort(key=lambda t: t.order)

            track = Track(
                id=data["id"],
                name=data["name"],
                description=data.get("description", ""),
                level=data.get("level", "beginner"),
                prerequisites=data.get("prerequisites", []),
                topics=topics,
                adaptive=data.get("adaptive", False),
                estimated_hours=data.get("estimated_hours", 1),
            )
            return track
        except Exception as e:
            logger.error(f"Ошибка парсинга {path}: {e}")
            return None

    def get_track(self, track_id: str) -> Track | None:
        """Получить трек по ID"""
        return self.tracks.get(track_id)

    def list_tracks(self) -> list[Track]:
        """Вернуть список всех треков"""
        return list(self.tracks.values())

    def get_available_tracks(
        self, completed_tracks: list[str], _weak_topics: list[dict] | None = None
    ) -> list[Track]:
        """Получить треки, доступные для прохождения (примитивы выполнены)"""
        available = []
        for track in self.tracks.values():
            # Проверяем prerequisites
            prereqs_ok = all(pid in completed_tracks for pid in track.prerequisites)
            if prereqs_ok:
                available.append(track)
        return available

    def recommend_tracks(
        self, weak_topics: list[dict], completed_tracks: list[str] | None = None
    ) -> list[tuple[Track, float]]:
        """Рекомендовать треки на основе слабых тем.

        Returns:
            List of (track, score) пар, отсортированных по релевантности
        """
        if completed_tracks is None:
            completed_tracks = []

        available = self.get_available_tracks(completed_tracks)
        recommendations = []

        weak_topic_names = [t["topic"] for t in weak_topics] if weak_topics else []

        for track in available:
            score = 0.0
            # Если трек помечен как адаптивный и есть слабые темы - повышаем score
            if track.adaptive and weak_topic_names:
                # Проверяем, покрывает ли трек слабые темы
                covered = sum(
                    1
                    for topic in track.topics
                    if topic.topic_id in weak_topic_names
                    or topic.linked_topic in weak_topic_names
                )
                if covered > 0:
                    score += covered * 2.0

            # Если нет слабых тем, предлагаем beginner треки
            if not weak_topic_names and track.level == "beginner":
                score += 1.0

            # Учитываем приоритет по level
            level_weights = {"beginner": 3.0, "intermediate": 2.0, "advanced": 1.0}
            if score == 0:  # если нет специальных совпадений
                score = level_weights.get(track.level, 1.0)

            recommendations.append((track, score))

        # Сортируем по score descending
        recommendations.sort(key=lambda x: x[1], reverse=True)
        return recommendations

    def validate_topic_completion(
        self,
        track: Track,
        topic_id: str,
        score: float | None = None,
        min_score: float | None = None,
    ) -> bool:
        """Проверить, пройдена ли тема (достигнут ли минимальный балл)"""
        topic = track.get_topic_by_id(topic_id)
        if not topic:
            return False
        if score is None:
            return True  # Если score не передан, считаем пройденной
        threshold = min_score if min_score is not None else topic.min_score
        return score >= threshold


# Глобальный экземпляр движка
_engine: TrackEngine | None = None


def get_track_engine() -> TrackEngine:
    """Получить глобальный экземпляр TrackEngine (ленивая загрузка)"""
    global _engine  # noqa: PLW0603
    if _engine is None:
        _engine = TrackEngine()
    return _engine
