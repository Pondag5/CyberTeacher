"""Unit tests for handlers/quiz.py"""

import time
import unittest
from unittest.mock import MagicMock, call, patch


class MockState:
    """Mock AppState for testing"""

    def __init__(self):
        self.risk_level = 0
        self.weak_topics = []
        self.review_schedule = {}
        self.last_writeup_activity = None
        self.assignments_completed = 0
        self.quizzes_taken = 0
        self.stealth_ops = 0
        self.earned_achievements = []
        self.points = 0.0

    def get_next_weak_topic(self, threshold=70.0):
        weak = [t for t in self.weak_topics if t["success_rate"] < threshold]
        return weak[0]["topic"] if weak else None

    def increase_risk(self, amount=10):
        self.risk_level = min(100, self.risk_level + amount)
        self.check_achievements()

    def decrease_risk(self, amount=5):
        self.risk_level = max(0, self.risk_level - amount)
        self.check_achievements()

    def increment_stealth_ops(self):
        self.stealth_ops += 1
        self.check_achievements()

    def complete_assignment(self):
        self.assignments_completed += 1
        self.check_achievements()

    def update_weak_topic(self, topic, score, max_score=10.0):
        for entry in self.weak_topics:
            if entry["topic"] == topic:
                entry["attempts"] += 1
                entry["total_score"] += score
                entry["max_score"] += max_score
                entry["success_rate"] = (
                    (entry["total_score"] / entry["max_score"]) * 100
                    if entry["max_score"] > 0
                    else 0
                )
                return
        self.weak_topics.append(
            {
                "topic": topic,
                "attempts": 1,
                "total_score": score,
                "max_score": max_score,
                "success_rate": (score / max_score) * 100 if max_score > 0 else 0,
            }
        )

    def schedule_review(self, topic, grade, max_grade=10.0):
        quality = (grade / max_grade) * 5 if max_grade > 0 else 0
        if topic not in self.review_schedule:
            entry = {
                "repetitions": 0,
                "interval": 1,
                "next_review": time.time() + 86400,
                "last_grade": grade,
                "ef": 2.5,
            }
        else:
            entry = self.review_schedule[topic].copy()
            if quality < 3:
                entry["repetitions"] = 0
                entry["interval"] = 1
                entry["ef"] = 2.5
            else:
                entry["repetitions"] = entry.get("repetitions", 0) + 1
                if entry["repetitions"] == 1:
                    entry["interval"] = 1
                elif entry["repetitions"] == 2:
                    entry["interval"] = 3
                else:
                    ef = entry.get("ef", 2.5) + (
                        0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)
                    )
                    entry["ef"] = max(1.3, ef)
                    entry["interval"] = max(
                        1, int(entry.get("interval", 1) * entry["ef"])
                    )
            entry["next_review"] = time.time() + entry["interval"] * 86400
            entry["last_grade"] = grade
        self.review_schedule[topic] = entry

    def get_weak_topics(self, threshold=70.0):
        weak = [t for t in self.weak_topics if t["success_rate"] < threshold]
        return sorted(weak, key=lambda x: x["success_rate"])

    def take_quiz(self):
        self.quizzes_taken += 1
        self.check_achievements()

    def take_quiz(self):
        self.quizzes_taken += 1
        self.check_achievements()

    def check_achievements(self):
        """Return mock achievements (simplified)"""
        # In tests we mock the file; this returns empty list unless mocked
        return []

    def save_to_file(self):
        pass


class TestHandlersQuiz(unittest.TestCase):
    """Tests for handlers/quiz module"""

    @patch("handlers.quiz.GENERATORS_AVAILABLE", False)
    @patch("handlers.quiz.get_context")
    def test_handle_quiz_action_no_generators(self, mock_get_context):
        """Test handle_quiz_action when generators unavailable"""
        from handlers import quiz

        mock_state = MockState()
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        with patch("handlers.quiz.console.print") as mock_print:
            result = quiz.handle_quiz_action()

        self.assertEqual(result, (True, None, None, True))
        mock_print.assert_any_call("[yellow]Генератор квизов недоступен[/yellow]")

    @patch("handlers.quiz.GENERATORS_AVAILABLE", True)
    @patch("handlers.quiz.get_context")
    @patch("knowledge.get_current_vectordb")
    @patch("handlers.quiz.generate_quiz")
    @patch("builtins.input")
    @patch("handlers.quiz.console.print")
    def test_handle_quiz_action_multiple_choice_success(
        self, mock_print, mock_input, mock_generate_quiz, mock_vectordb, mock_get_context
    ):
        """Test quiz with multiple choice questions - correct answers"""
        from handlers import quiz

        mock_state = MockState()
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        # Mock quiz data
        mock_generate_quiz.return_value = {
            "questions": [
                {
                    "question": "Q1?",
                    "options": {"A": "AnsA", "B": "AnsB"},
                    "correct": "A",
                    "explanation": "Expl1",
                },
                {
                    "question": "Q2?",
                    "options": {"A": "AnsA", "B": "AnsB", "C": "AnsC"},
                    "correct": "C",
                    "explanation": "Expl2",
                },
            ],
            "topic": "test_topic",
        }
        mock_vectordb.return_value = MagicMock()
        # Simulate user answering: correct, correct
        mock_input.side_effect = ["A", "C"]

        result = quiz.handle_quiz_action()

        self.assertEqual(result, (True, None, None, True))
        # State should be updated
        self.assertEqual(mock_state.quizzes_taken, 1)
        self.assertEqual(mock_state.weak_topics[0]["topic"], "test_topic")
        self.assertTrue(mock_state.review_schedule.get("test_topic") is not None)

    @patch("handlers.quiz.GENERATORS_AVAILABLE", True)
    @patch("handlers.quiz.get_context")
    @patch("knowledge.get_current_vectordb")
    @patch("handlers.quiz.generate_quiz")
    @patch("builtins.input")
    @patch("handlers.quiz.console.print")
    def test_handle_quiz_action_with_skips_and_exit(
        self, mock_print, mock_input, mock_generate_quiz, mock_vectordb, mock_get_context
    ):
        """Test quiz with skip, empty, and exit commands"""
        from handlers import quiz

        mock_state = MockState()
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        mock_generate_quiz.return_value = {
            "questions": [
                {
                    "question": "Q1?",
                    "options": {"A": "AnsA", "B": "AnsB"},
                    "correct": "A",
                    "explanation": "Expl1",
                },
                {
                    "question": "Q2?",
                    "options": {"A": "AnsA", "B": "AnsB"},
                    "correct": "B",
                    "explanation": "Expl2",
                },
                {
                    "question": "Q3?",
                    "options": {"A": "AnsA", "B": "AnsB"},
                    "correct": "A",
                    "explanation": "Expl3",
                },
            ],
            "topic": "test_topic",
        }
        mock_vectordb.return_value = MagicMock()
        # User: skip, empty answer, exit
        mock_input.side_effect = ["/skip", "", "/exit"]

        result = quiz.handle_quiz_action()

        self.assertEqual(result, (True, None, None, True))
        # Quiz should be taken
        self.assertEqual(mock_state.quizzes_taken, 1)
        # Should have partial scores (skipped and empty both 0)
        # Weak topic update and review schedule still set
        self.assertTrue("test_topic" in mock_state.review_schedule)

    @patch("handlers.quiz.GENERATORS_AVAILABLE", True)
    @patch("handlers.quiz.get_context")
    @patch("knowledge.get_current_vectordb")
    @patch("handlers.quiz.generate_quiz")
    @patch("handlers.quiz.check_open_answer")
    @patch("builtins.input")
    @patch("handlers.quiz.console.print")
    def test_handle_quiz_action_open_ended(  # noqa: PLR0913
        self,
        mock_print,
        mock_input,
        mock_check_open,
        mock_generate_quiz,
        mock_vectordb,
        mock_get_context,
    ):
        """Test quiz with open-ended questions"""
        from handlers import quiz

        mock_state = MockState()
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        mock_generate_quiz.return_value = {
            "questions": [
                {
                    "question": "Explain XSS",
                    "correct": None,
                    "explanation": "",
                },
            ],
            "topic": "xss",
        }
        mock_vectordb.return_value = MagicMock()
        mock_check_open.return_value = {"score": 8, "feedback": "Good"}
        mock_input.return_value = "My answer details"

        result = quiz.handle_quiz_action()

        self.assertEqual(result, (True, None, None, True))
        mock_check_open.assert_called_once()
        self.assertEqual(mock_state.quizzes_taken, 1)

    @patch("handlers.quiz.GENERATORS_AVAILABLE", True)
    @patch("handlers.quiz.get_context")
    @patch("knowledge.get_current_vectordb")
    @patch("handlers.quiz.generate_quiz")
    @patch("builtins.input")
    @patch("handlers.quiz.console.print")
    def test_handle_quiz_action_risk_adjustment_low_score(
        self, mock_print, mock_input, mock_generate_quiz, mock_vectordb, mock_get_context
    ):
        """Test risk level increases when success rate < 50%"""
        from handlers import quiz

        mock_state = MockState()
        mock_state.risk_level = 10
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        mock_generate_quiz.return_value = {
            "questions": [
                {
                    "question": "Q1?",
                    "options": {"A": "A"},
                    "correct": "B",
                    "explanation": "",
                },
                {
                    "question": "Q2?",
                    "options": {"A": "A"},
                    "correct": "B",
                    "explanation": "",
                },
            ],
            "topic": "low_score",
        }
        mock_vectordb.return_value = MagicMock()
        mock_input.side_effect = ["A", "A"]  # both wrong -> 0/20 = 0%

        result = quiz.handle_quiz_action()

        self.assertEqual(mock_state.risk_level, 20)  # increased by 10

    @patch("handlers.quiz.GENERATORS_AVAILABLE", True)
    @patch("handlers.quiz.get_context")
    @patch("knowledge.get_current_vectordb")
    @patch("handlers.quiz.generate_quiz")
    @patch("builtins.input")
    @patch("handlers.quiz.console.print")
    def test_handle_quiz_action_stealth_ops_low_risk(
        self, mock_print, mock_input, mock_generate_quiz, mock_vectordb, mock_get_context
    ):
        """Test stealth_ops increment when risk < 20 and success >= 50%"""
        from handlers import quiz

        mock_state = MockState()
        mock_state.risk_level = 10
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        mock_generate_quiz.return_value = {
            "questions": [
                {
                    "question": "Q1?",
                    "options": {"A": "A"},
                    "correct": "A",
                    "explanation": "",
                },
            ],
            "topic": "test",
        }
        mock_vectordb.return_value = MagicMock()
        mock_input.return_value = "A"

        result = quiz.handle_quiz_action()

        self.assertEqual(mock_state.stealth_ops, 1)

    @patch("handlers.quiz.GENERATORS_AVAILABLE", True)
    @patch("handlers.quiz.get_context")
    @patch("knowledge.get_current_vectordb")
    @patch("handlers.quiz.generate_quiz")
    @patch("builtins.input")
    @patch("handlers.quiz.console.print")
    def test_handle_quiz_action_with_weak_topic_focus(
        self, mock_print, mock_input, mock_generate_quiz, mock_vectordb, mock_get_context
    ):
        """Test that weak topic is passed to generator"""
        from handlers import quiz

        mock_state = MockState()
        mock_state.weak_topics = [
            {
                "topic": "weak_topic",
                "success_rate": 50.0,
                "attempts": 2,
                "total_score": 100,
                "max_score": 200,
            }
        ]
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        mock_generate_quiz.return_value = {
            "questions": [
                {"question": "Explain XSS", "correct": None, "explanation": ""},
            ],
            "topic": "weak_topic",
        }
        mock_vectordb.return_value = MagicMock()
        mock_input.return_value = "answer"

        result = quiz.handle_quiz_action()

        mock_generate_quiz.assert_called_once()
        _, kwargs = mock_generate_quiz.call_args
        self.assertEqual(kwargs.get("topic"), "weak_topic")

    @patch("handlers.quiz.GENERATORS_AVAILABLE", True)
    @patch("handlers.quiz.get_context")
    @patch("knowledge.get_current_vectordb")
    @patch("handlers.quiz.generate_quiz")
    @patch("builtins.input")
    @patch("handlers.quiz.console.print")
    def test_handle_quiz_action_no_questions_generated(
        self, mock_print, mock_input, mock_generate_quiz, mock_vectordb, mock_get_context
    ):
        """Test when generator returns empty questions list"""
        from handlers import quiz

        mock_state = MockState()
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        mock_generate_quiz.return_value = {"questions": [], "topic": "test"}
        mock_vectordb.return_value = MagicMock()

        result = quiz.handle_quiz_action()

        self.assertEqual(result, (True, None, None, True))
        mock_print.assert_any_call("[yellow]Не удалось сгенерировать вопросы[/yellow]")

    @patch("handlers.quiz.GENERATORS_AVAILABLE", False)
    @patch("handlers.quiz.get_context")
    def test_handle_task_action_no_generators(self, mock_get_context):
        """Test handle_task_action when generators unavailable"""
        from handlers import quiz

        mock_state = MockState()
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        with patch("handlers.quiz.console.print") as mock_print:
            result = quiz.handle_task_action()

        self.assertEqual(result, (True, None, None, True))
        mock_print.assert_any_call("[yellow]Генератор заданий недоступен[/yellow]")

    @patch("handlers.quiz.GENERATORS_AVAILABLE", True)
    @patch("handlers.quiz.get_context")
    @patch("knowledge.get_current_vectordb")
    @patch("handlers.quiz.generate_task")
    @patch("builtins.input")
    @patch("handlers.quiz.console.print")
    def test_handle_task_action_success(
        self, mock_print, mock_input, mock_generate_task, mock_vectordb, mock_get_context
    ):
        """Test task action successful completion"""
        from handlers import quiz

        mock_state = MockState()
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        # Create mock task object
        mock_task = MagicMock()
        mock_task.question = "Do thing"
        mock_task.answer = "flag{abc}"
        mock_task.hint = "Think about input validation"
        mock_task.category = "web"
        mock_generate_task.return_value = mock_task
        mock_vectordb.return_value = MagicMock()
        mock_input.return_value = "flag{abc}"

        result = quiz.handle_task_action()

        self.assertEqual(result, (True, None, None, True))
        # Verify keyword-based scoring
        # First review should have repetitions = 0 (SM-2)
        self.assertIn("web", mock_state.review_schedule)
        self.assertEqual(mock_state.review_schedule["web"]["repetitions"], 0)
        self.assertIsNotNone(mock_state.last_writeup_activity)

    @patch("handlers.quiz.GENERATORS_AVAILABLE", True)
    @patch("handlers.quiz.get_context")
    @patch("knowledge.get_current_vectordb")
    @patch("handlers.quiz.generate_task")
    @patch("builtins.input")
    @patch("handlers.quiz.console.print")
    def test_handle_task_action_skip(
        self, mock_print, mock_input, mock_generate_task, mock_vectordb, mock_get_context
    ):
        """Test task action with skip command"""
        from handlers import quiz

        mock_state = MockState()
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        mock_task = MagicMock()
        mock_task.question = "Task?"
        mock_task.answer = "flag{123}"
        mock_task.hint = "hint"
        mock_task.category = "crypto"
        mock_generate_task.return_value = mock_task
        mock_vectordb.return_value = MagicMock()
        mock_input.return_value = "/skip"

        result = quiz.handle_task_action()

        self.assertEqual(result, (True, None, None, True))
        # Score should be 0, review still scheduled
        self.assertTrue("crypto" in mock_state.review_schedule)

    @patch("handlers.quiz.GENERATORS_AVAILABLE", True)
    @patch("handlers.quiz.get_context")
    def test_handle_quiz_generation_with_generators(self, mock_get_context):
        """Test handle_quiz_generation shows questions"""
        from handlers import quiz

        mock_state = MockState()
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        with (
            patch("handlers.quiz.generate_quiz") as mock_gen,
            patch("handlers.quiz.console.print") as mock_print,
            patch("builtins.input", side_effect=["A", "B", "/exit"]),
        ):
            mock_gen.return_value = {
                "questions": [
                    {
                        "question": "Q1?",
                        "options": {"A": "opt1", "B": "opt2"},
                        "correct": "A",
                        "explanation": "",
                    },
                    {
                        "question": "Q2?",
                        "options": {"A": "opt1", "B": "opt2"},
                        "correct": "B",
                        "explanation": "",
                    },
                ],
                "topic": "test",
            }
            result = quiz.handle_quiz_generation("/smart_test", None)

            self.assertEqual(result, (True, None, None, True))
            # Should print multiple questions
            calls = [str(c) for c in mock_print.call_args_list]
            self.assertTrue(any("Q1?" in c for c in calls))
            self.assertTrue(any("Q2?" in c for c in calls))

    @patch("handlers.quiz.GENERATORS_AVAILABLE", False)
    @patch("handlers.quiz.get_context")
    def test_handle_quiz_generation_no_generators(self, mock_get_context):
        """Test handle_quiz_generation when unavailable"""
        from handlers import quiz

        mock_state = MockState()
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        with patch("handlers.quiz.console.print") as mock_print:
            result = quiz.handle_quiz_generation("/smart_test", None)

        self.assertEqual(result, (True, None, None, True))
        mock_print.assert_any_call("[yellow]Генератор квизов недоступен[/yellow]")

    @patch("handlers.quiz.get_context")
    @patch("handlers.quiz.console.print")
    def test_handle_code_review_stub(self, mock_print, mock_get_context):
        """Test handle_code_review returns stub message"""
        from handlers import quiz

        mock_state = MockState()
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        result = quiz.handle_code_review("code_review")

        self.assertEqual(result, (True, None, None, True))
        mock_print.assert_any_call(
            "[yellow]Отправьте код для анализа (в разработке)[/yellow]"
        )


class TestCheckOpenAnswer(unittest.TestCase):
    """Tests for check_open_answer from misc.py"""

    def test_check_open_answer_empty(self):
        from handlers.misc import check_open_answer

        result = check_open_answer("Q?", "", None)
        self.assertEqual(result["score"], 0)

    def test_check_open_answer_non_empty(self):
        from handlers.misc import check_open_answer

        result = check_open_answer("Q?", "some answer", None)
        self.assertEqual(result["score"], 6)

    def test_check_open_answer_contains_correctly(self):
        from handlers.misc import check_open_answer

        result = check_open_answer("Q?", "Ответ правильно", None)
        self.assertEqual(result["score"], 9)
        self.assertIn("Отлично", result["feedback"])

    def test_check_open_answer_key_points(self):
        from handlers.misc import check_open_answer

        result = check_open_answer(
            "Q?", "point1 and point2", ["point1", "point2", "point3"]
        )
        self.assertGreaterEqual(result["score"], 8)  # 6 + at least 2 from key points
        self.assertIn("ключевых", result["feedback"])


if __name__ == "__main__":
    unittest.main()
