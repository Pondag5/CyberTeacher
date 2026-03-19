import json
import unittest
from unittest.mock import patch, MagicMock

from quiz_generator import (
    generate_quiz_question,
    generate_assignment,
    extract_json_block,
)


class TestQuizGenerator(unittest.TestCase):
    @patch("quiz_generator.get_llm")
    def test_generate_quiz_question_success(self, mock_get_llm):
        mock_llm = MagicMock()
        response = {
            "question": "What is SQL injection?",
            "options": [
                "A type of attack",
                "A database type",
                "A programming language",
                "A security tool",
            ],
            "correct_answer": 0,
            "explanation": "SQL injection is a code injection technique...",
        }
        mock_llm.invoke.return_value.content = f"```json\n{json.dumps(response)}\n```"
        mock_get_llm.return_value = mock_llm

        result = generate_quiz_question("SQL injection", "medium")
        self.assertIsInstance(result, dict)
        self.assertEqual(result["question"], "What is SQL injection?")
        self.assertEqual(result["correct_answer"], 0)
        self.assertEqual(result["options"], response["options"])

    @patch("quiz_generator.get_llm")
    def test_generate_quiz_question_invalid_response(self, mock_get_llm):
        mock_llm = MagicMock()
        mock_llm.invoke.return_value.content = "Some plain text without JSON"
        mock_get_llm.return_value = mock_llm

        result = generate_quiz_question("XSS", "easy")
        self.assertIsNone(result)

    @patch("quiz_generator.get_llm")
    def test_generate_quiz_question_llm_error(self, mock_get_llm):
        mock_llm = MagicMock()
        mock_llm.invoke.side_effect = Exception("LLM unavailable")
        mock_get_llm.return_value = mock_llm

        result = generate_quiz_question("CSRF", "hard")
        self.assertIsNone(result)

    def test_extract_json_block(self):
        text = '```json\n{"key": "value"}\n```'
        block = extract_json_block(text)
        self.assertEqual(block, '{"key": "value"}')
        text2 = "No json here"
        block2 = extract_json_block(text2)
        self.assertIsNone(block2)

    @patch("quiz_generator.get_llm")
    def test_generate_assignment_success(self, mock_get_llm):
        mock_llm = MagicMock()
        assignment = {
            "title": "SQL Injection Lab",
            "description": "Find the vulnerability",
            "steps": ["Open page", "Enter payload"],
            "hints": ["Try 'OR 1=1--"],
            "expected_flag": "FLAG{123}",
            "points": 100,
        }
        mock_llm.invoke.return_value.content = f"```json\n{json.dumps(assignment)}\n```"
        mock_get_llm.return_value = mock_llm

        result = generate_assignment("SQLi", "hard")
        self.assertIsInstance(result, dict)
        self.assertEqual(result["title"], "SQL Injection Lab")
        self.assertEqual(result["expected_flag"], "FLAG{123}")

    @patch("quiz_generator.get_llm")
    def test_generate_assignment_invalid(self, mock_get_llm):
        mock_llm = MagicMock()
        mock_llm.invoke.return_value.content = "Some text"
        mock_get_llm.return_value = mock_llm
        result = generate_assignment("XSS")
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
