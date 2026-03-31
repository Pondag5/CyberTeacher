"""Tests for Bug Bounty Simulation (M-31)"""
# isort: skip_file

import unittest
from unittest.mock import MagicMock, patch

from state import AppState
from handlers.bug_bounty import handle_bounty, _select_scenario, _get_llm_review


class TestBugBounty(unittest.TestCase):
    """Test bug bounty simulation"""

    @patch("handlers.bug_bounty.get_state")
    def test_handle_bounty_runs_interactive(self, mock_get_state):
        """Basic interaction: connection to LLM and report creation"""
        mock_state = MagicMock(spec=AppState)
        mock_state.points = 0.0
        mock_state.bounty_reports = []
        mock_get_state.return_value = mock_state

        # Mock the LLM
        mock_llm = MagicMock()
        mock_response = MagicMock()
        mock_response.content = '{"score": 85, "feedback": "Good", "strengths": [], "improvements": [], "badges": ["clear"]}'
        mock_llm.invoke.return_value = mock_response

        with (
            patch("handlers.bug_bounty.get_llm", return_value=mock_llm),
            patch("handlers.bug_bounty._select_scenario") as mock_scenario,
            patch("rich.console.Console.print"),
            patch("rich.prompt.Prompt.ask") as mock_ask,
        ):
            # Setup scenario
            mock_scenario.return_value = {
                "id": "test",
                "title": "Test Vuln",
                "description": "desc",
                "vulnerability": "SQLi",
                "context": "ctx",
                "expected_cwe": "CWE-89",
            }
            # Mock prompts: order: title, vuln_type, summary, steps, impact, fix
            mock_ask.side_effect = [
                "My Report",  # title
                "SQL Injection",  # vuln_type
                "It is a SQLi",  # summary
                "1. step",  # steps
                "DB leak",  # impact
                "Use params",  # fix
            ]

            success, _, __ = handle_bounty("bounty", "")
            self.assertTrue(success)
            self.assertEqual(mock_state.points, 220)  # base 50 + 85*2
            self.assertEqual(len(mock_state.bounty_reports), 1)
            report = mock_state.bounty_reports[0]
            self.assertEqual(report["title"], "My Report")
            self.assertEqual(report["review"]["score"], 85)

    @patch("handlers.bug_bounty.get_state")
    def test_handle_bounty_llm_failure(self, mock_get_state):
        """If LLM fails, still saves with low score"""
        mock_state = MagicMock(spec=AppState)
        mock_state.points = 0.0
        mock_state.bounty_reports = []
        mock_get_state.return_value = mock_state

        mock_llm = MagicMock()
        mock_llm.invoke.side_effect = Exception("LLM down")

        with (
            patch("handlers.bug_bounty.get_llm", return_value=mock_llm),
            patch("handlers.bug_bounty._select_scenario") as mock_scenario,
            patch("rich.console.Console.print"),
            patch("rich.prompt.Prompt.ask") as mock_ask,
        ):
            mock_scenario.return_value = {
                "id": "test",
                "title": "t",
                "description": "d",
                "vulnerability": "v",
                "context": "c",
                "expected_cwe": "CWE-1",
            }
            mock_ask.side_effect = ["R", "V", "S", "St", "I", "F"]

            success, _, __ = handle_bounty("bounty", "")
            self.assertTrue(success)
            # Despite error, report saved with default score 30
            self.assertEqual(mock_state.points, 110)  # 50+60
            self.assertEqual(mock_state.bounty_reports[0]["review"]["score"], 30)

    def test_select_scenario_returns_valid(self):
        """_select_scenario returns a scenario dict"""
        for _ in range(5):
            scenario = _select_scenario()
            self.assertIn("id", scenario)
            self.assertIn("title", scenario)
            self.assertIn("vulnerability", scenario)

    def test_get_llm_review_parses_json(self):
        """_get_llm_review parses JSON from LLM response"""
        mock_llm = MagicMock()
        mock_response = MagicMock()
        mock_response.content = 'Some text { "score": 92, "feedback": "Great", "strengths": ["A"], "improvements": ["B"], "badges": ["thorough"] }'
        mock_llm.invoke.return_value = mock_response

        report = {
            "title": "Test",
            "vulnerability": "XSS",
            "summary": "...",
            "steps": "...",
            "impact": "...",
            "fix": "...",
        }
        with patch("handlers.bug_bounty.get_llm", return_value=mock_llm):
            result = _get_llm_review(report)
            self.assertEqual(result["score"], 92)
            self.assertEqual(result["feedback"], "Great")


if __name__ == "__main__":
    unittest.main()
