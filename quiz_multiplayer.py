"""Multiplayer Quiz — real-time quizzes via WebSocket.

Room-based system: a host creates a room, players join,
questions are sent to all, scores tracked in real-time.
"""

import asyncio
import json
import random
import time
from typing import Any, Dict, List, Optional


class QuizRoom:
    """A single quiz room with host and players."""

    def __init__(self, room_id: str, host_name: str) -> None:
        self.room_id = room_id
        self.host_name = host_name
        self.players: Dict[str, Dict[str, Any]] = {}
        self.questions: List[Dict[str, Any]] = []
        self.current_question: int = -1
        self.started: bool = False
        self.finished: bool = False
        self.answers: Dict[str, int] = {}
        self.created_at: float = time.time()

    def add_player(self, name: str, ws: Any) -> None:
        self.players[name] = {"ws": ws, "score": 0, "streak": 0}

    def remove_player(self, name: str) -> None:
        self.players.pop(name, None)

    def set_questions(self, questions: List[Dict[str, Any]]) -> None:
        self.questions = questions
        self.current_question = -1

    def submit_answer(self, player_name: str, answer_idx: int) -> Dict[str, Any]:
        if self.current_question < 0 or self.current_question >= len(self.questions):
            return {"error": "No active question"}

        q = self.questions[self.current_question]
        correct = q.get("correct", 0)
        is_correct = answer_idx == correct

        if player_name in self.players:
            if is_correct:
                streak = self.players[player_name]["streak"] + 1
                bonus = min(streak, 5) * 2
                self.players[player_name]["score"] += 10 + bonus
                self.players[player_name]["streak"] = streak
            else:
                self.players[player_name]["streak"] = 0

        self.answers[player_name] = answer_idx

        return {
            "correct": is_correct,
            "correct_answer": correct,
            "options": q.get("options", []),
            "explanation": q.get("explanation", ""),
        }

    def get_leaderboard(self) -> List[Dict[str, Any]]:
        board = [
            {"name": n, "score": p["score"], "streak": p["streak"]}
            for n, p in self.players.items()
        ]
        return sorted(board, key=lambda x: x["score"], reverse=True)

    def get_state(self) -> Dict[str, Any]:
        q = (
            self.questions[self.current_question]
            if 0 <= self.current_question < len(self.questions)
            else None
        )
        return {
            "room_id": self.room_id,
            "host": self.host_name,
            "players": len(self.players),
            "started": self.started,
            "finished": self.finished,
            "current_question": self.current_question,
            "total_questions": len(self.questions),
            "leaderboard": self.get_leaderboard(),
            "question": {
                "question": q.get("question", "") if q else "",
                "options": q.get("options", []) if q else [],
            }
            if q
            else None,
        }


# Global room registry
rooms: Dict[str, QuizRoom] = {}


def create_room(room_id: str, host_name: str) -> QuizRoom:
    room = QuizRoom(room_id, host_name)
    rooms[room_id] = room
    return room


def get_room(room_id: str) -> Optional[QuizRoom]:
    return rooms.get(room_id)


def delete_room(room_id: str) -> None:
    rooms.pop(room_id, None)


def cleanup_old_rooms(max_age: int = 3600) -> int:
    """Remove rooms older than max_age seconds."""
    now = time.time()
    to_delete = [rid for rid, r in rooms.items() if now - r.created_at > max_age]
    for rid in to_delete:
        del rooms[rid]
    return len(to_delete)
