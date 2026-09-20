"""Learning Memory Service — teacher's long-term memory about student errors.

Stores:
- misconceptions
- errors
- breakthroughs
- hint_needed

Provides:
- semantic retrieval of similar past errors
- weak topics aggregation
- personality insights for drift adjustments
"""

from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any, Dict, List, Optional

import numpy as np
from sqlalchemy.orm import Session

from config import LazyLoader
from db import LearningEvent, _utc_now_naive, get_session

logger = logging.getLogger(__name__)


class LearningMemoryService:
    def __init__(self) -> None:
        self._embeddings_model = None
        self._index: Optional[np.ndarray] = None
        self._ids: List[int] = []
        self._user_ids: List[str] = []

    def _get_embeddings_model(self):
        if self._embeddings_model is None:
            self._embeddings_model = LazyLoader.get_embeddings()
        return self._embeddings_model

    def _rebuild_index(self) -> None:
        db = get_session()
        try:
            events = db.query(LearningEvent).order_by(LearningEvent.id).all()
            self._ids = [e.id for e in events]
            self._user_ids = [e.user_id for e in events]
            vectors = [e.embedding for e in events if e.embedding]
            if vectors:
                self._index = np.array(vectors, dtype=np.float32)
            else:
                self._index = np.empty((0, 0), dtype=np.float32)
        finally:
            db.close()

    def _ensure_index(self) -> None:
        if self._index is None or self._index.size == 0:
            self._rebuild_index()

    def record_event(
        self,
        topic: str,
        event_type: str,
        user_belief: str = "",
        correct_model: str = "",
        root_cause: str = "",
        resolution: str = "",
        context_ref: str = "",
        user_id: str = "default",
        importance: float = 0.5,
    ) -> Optional[Dict[str, Any]]:
        db = get_session()
        try:
            event = LearningEvent(
                user_id=user_id,
                topic=topic,
                event_type=event_type,
                user_belief=user_belief,
                correct_model=correct_model,
                root_cause=root_cause,
                resolution=resolution,
                context_ref=context_ref,
                importance=importance,
            )
            embeddings_model = self._get_embeddings_model()
            if embeddings_model:
                text = " ".join(
                    part
                    for part in [topic, event_type, user_belief, correct_model, root_cause]
                    if part
                )
                event.embedding = embeddings_model.embed_query(text)
            db.add(event)
            db.commit()
            db.refresh(event)

            self._rebuild_index()

            return {
                "id": event.id,
                "topic": event.topic,
                "event_type": event.event_type,
                "user_belief": event.user_belief,
                "correct_model": event.correct_model,
                "root_cause": event.root_cause,
                "resolution": event.resolution,
                "context_ref": event.context_ref,
                "timestamp": event.timestamp,
            }
        except Exception as exc:
            db.rollback()
            logger.error("Failed to record learning event: %s", exc)
            return None
        finally:
            db.close()

    def get_similar_events(
        self,
        query: str,
        top_k: int = 3,
        user_id: str = "default",
    ) -> List[Dict[str, Any]]:
        embeddings_model = self._get_embeddings_model()
        if not embeddings_model:
            return []

        self._ensure_index()
        if self._index is None or self._index.size == 0:
            return []

        query_emb = np.array(embeddings_model.embed_query(query), dtype=np.float32).reshape(1, -1)

        index = self._index
        if index.ndim != 2 or index.shape[0] == 0:
            return []

        norms = np.linalg.norm(index, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        normalized = index / norms
        query_norm = np.linalg.norm(query_emb)
        if query_norm == 0:
            query_norm = 1.0
        query_normalized = query_emb / query_norm

        scores = np.dot(normalized, query_normalized.T).flatten()
        candidate_indices = np.argsort(scores)[::-1][: top_k * 3]

        db = get_session()
        try:
            candidates: List[Dict[str, Any]] = []
            for idx in candidate_indices:
                event_id = self._ids[idx]
                event = db.query(LearningEvent).filter_by(id=event_id, user_id=user_id).first()
                if event:
                    candidates.append(
                        {
                            "id": event.id,
                            "topic": event.topic,
                            "event_type": event.event_type,
                            "user_belief": event.user_belief,
                            "correct_model": event.correct_model,
                            "root_cause": event.root_cause,
                            "resolution": event.resolution,
                            "context_ref": event.context_ref,
                            "timestamp": event.timestamp,
                            "importance": float(event.importance or 0.5),
                            "cosine_score": float(scores[idx]),
                        }
                    )
            if not candidates:
                return []

            now = _utc_now_naive()
            for c in candidates:
                age_days = max((now - c["timestamp"]).total_seconds() / 86400.0, 0.0)
                recency_boost = max(0.0, 1.0 - age_days / 30.0)
                c["final_score"] = c["cosine_score"] * c["importance"] * (0.7 + 0.3 * recency_boost)

            candidates.sort(key=lambda x: x["final_score"], reverse=True)
            ranked = candidates[:top_k]
            for r in ranked:
                r.pop("final_score", None)
            return ranked
        finally:
            db.close()

    def get_weak_topics(self, limit: int = 5, user_id: str = "default") -> List[Dict[str, Any]]:
        db = get_session()
        try:
            from sqlalchemy import func

            rows = (
                db.query(
                    LearningEvent.topic,
                    func.count(LearningEvent.id).label("error_count"),
                )
                .filter(
                    LearningEvent.user_id == user_id,
                    LearningEvent.event_type.in_(["misconception", "error"]),
                )
                .group_by(LearningEvent.topic)
                .order_by(func.count(LearningEvent.id).desc())
                .limit(limit)
                .all()
            )
            return [{"topic": r.topic, "error_count": r.error_count} for r in rows]
        finally:
            db.close()

    def get_personality_insights(self, user_id: str = "default") -> Dict[str, float]:
        weak = self.get_weak_topics(limit=3, user_id=user_id)
        total_errors = sum(item["error_count"] for item in weak)

        mods: Dict[str, float] = {}
        if total_errors >= 5:
            mods["patience"] = 0.15
        if total_errors >= 10:
            mods["patience"] = 0.25
            mods["sarcasm"] = -0.1

        db = get_session()
        try:
            week_ago = _utc_now_naive() - timedelta(days=7)
            breakthroughs = (
                db.query(LearningEvent)
                .filter(
                    LearningEvent.user_id == user_id,
                    LearningEvent.event_type == "breakthrough",
                    LearningEvent.timestamp >= week_ago,
                )
                .count()
            )
            if breakthroughs >= 3:
                mods["enthusiasm"] = 0.1
                mods["sarcasm"] = -0.05
        finally:
            db.close()

        return mods


_service = LearningMemoryService()


def get_learning_memory_service() -> LearningMemoryService:
    return _service
