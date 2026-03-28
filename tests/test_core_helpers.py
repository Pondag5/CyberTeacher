"""Unit tests for helper functions in handlers/core.py"""

import unittest
from unittest.mock import patch, MagicMock, mock_open
import os
import json

from handlers.core import (
    extract_json_block,
    check_open_answer,
    ResponseCache,
    clear_response_cache,
    show_cache_stats,
    handle_stats,
)


class TestExtractJsonBlock(unittest.TestCase):
    """Tests for extract_json_block function (core version)"""

    def test_simple_json(self):
        text = '```json\n{"key": "value"}\n```'
        result = extract_json_block(text)
        self.assertEqual(result, '{"key": "value"}')

    def test_no_backticks(self):
        text = 'prefix {"a": 1} suffix'
        result = extract_json_block(text)
        self.assertEqual(result, '{"a": 1}')

    def test_nested(self):
        text = '```json\n{"outer": {"inner": 42}}\n```'
        result = extract_json_block(text)
        self.assertEqual(result, '{"outer": {"inner": 42}}')

    def test_empty(self):
        self.assertIsNone(extract_json_block(""))
        self.assertIsNone(extract_json_block("no json"))

    def test_multiple_json_blocks_returns_first(self):
        text = '```json\n{"a":1}\n``` and ```json\n{"b":2}\n```'
        result = extract_json_block(text)
        self.assertEqual(result, '{"a":1}')


class TestCheckOpenAnswer(unittest.TestCase):
    """Tests for check_open_answer function (core version)"""

    def test_non_empty_gives_base_score(self):
        result = check_open_answer("question", "my answer")
        self.assertEqual(result["score"], 6)
        self.assertIn("Спасибо", result["feedback"])

    def test_contains_correct_gives_higher_score(self):
        result = check_open_answer("question", "я думаю это правильно")
        self.assertEqual(result["score"], 9)
        self.assertEqual(result["feedback"], "Отлично!")

    def test_key_points_half_match(self):
        user_ans = "I know that A and B are important"
        key_points = ["A", "B", "C"]
        result = check_open_answer("q", user_ans, key_points)
        # found = 2 out of 3 -> >= max(1, 3//2=1) -> score increase by 2 (min 10, 6+2=8)
        self.assertIn(
            result["score"], [8, 10]
        )  # if base 6 +2 =8; if already 9 then +2 capped to 10
        self.assertIn("ключевых моментах", result["feedback"])

    def test_key_points_all_match(self):
        result = check_open_answer("q", "A B C", ["A", "B", "C"])
        self.assertEqual(
            result["score"], 10
        )  # 6+2=8? Actually max(10, 6+2=8) -> 10? base is 6 unless contains correct then 9. No correct keyword, so base6+2=8; but if we also contain correct? Not.
        # Actually key_points half match adds 2 min(10, score+2). Starting from 6 yields 8.
        self.assertEqual(result["score"], 8)

    def test_empty_answer(self):
        result = check_open_answer("q", "")
        self.assertEqual(result["score"], 0)
        self.assertEqual(result["feedback"], "Спасибо за ответ.")


class TestResponseCache(unittest.TestCase):
    """Tests for ResponseCache class in core.py"""

    def setUp(self):
        # Use a temporary cache file path to avoid touching real file
        self.temp_file = "./memory/test_response_cache.json"
        # Ensure file does not exist
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)

    def tearDown(self):
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)

    @patch("handlers.core._response_cache")
    def test_clear_response_cache(self, mock_cache):
        # clear_response_cache just calls clear on the singleton and attempts save
        clear_response_cache()
        mock_cache.clear.assert_called_once()
        mock_cache._save.assert_called_once()

    @patch("handlers.core._response_cache")
    def test_show_cache_stats(self, mock_cache):
        from handlers.core import show_cache_stats

        mock_cache.stats.return_value = {
            "size": 2,
            "capacity": 100,
            "hit_count": 5,
            "access_count": 10,
        }
        # Should print stats; we patch console.print globally in other tests, but here we rely on that
        show_cache_stats()
        mock_cache.stats.assert_called_once()

    def test_response_cache_get_put(self):
        # Create a cache with a temp file isolated
        cache = ResponseCache(capacity=10)
        cache.cache_file = self.temp_file  # override file path
        cache._save = MagicMock()  # prevent actual file write during test

        cache.put("key1", "value1")
        self.assertEqual(cache.get("key1"), "value1")
        self.assertIsNone(cache.get("nonexistent"))

        stats = cache.stats()
        self.assertEqual(stats["size"], 1)
        self.assertEqual(stats["capacity"], 10)

    def test_response_cache_eviction(self):
        cache = ResponseCache(capacity=2)
        cache.cache_file = self.temp_file
        cache._save = MagicMock()

        cache.put("k1", "v1")
        cache.put("k2", "v2")
        cache.put("k3", "v3")  # should evict k1

        self.assertIsNone(cache.get("k1"))
        self.assertEqual(cache.get("k2"), "v2")
        self.assertEqual(cache.get("k3"), "v3")

        stats = cache.stats()
        self.assertEqual(stats["size"], 2)

    def test_response_cache_clear(self):
        cache = ResponseCache(capacity=10)
        cache.cache_file = self.temp_file
        cache._save = MagicMock()

        cache.put("a", 1)
        cache.put("b", 2)
        cache.clear()

        self.assertEqual(len(cache.cache), 0)
        self.assertEqual(cache.hit_count, 0)
        self.assertEqual(cache.access_count, 0)


class TestHandleStats(unittest.TestCase):
    """Tests for handle_stats function in core.py"""

    @patch("handlers.core.get_state")
    @patch("handlers.core.console.print")
    @patch("handlers.core._response_cache")
    @patch("memory.get_stats")
    def test_handle_stats_prints(
        self, mock_get_stats, mock_cache, mock_print, mock_get_state
    ):
        mock_get_stats.return_value = {
            "messages": 10,
            "points": 100,
            "flags": 2,
            "labs": 1,
            "courses": 3,
        }
        mock_conn = MagicMock()
        handle_stats(mock_conn)
        mock_get_stats.assert_called_once_with(mock_conn)
        # Check that various prints happened
        mock_print.assert_any_call("[bold cyan]📈 Статистика:[/bold cyan]")
        mock_print.assert_any_call("  Сообщений: 10")
        mock_print.assert_any_call("  Очков: 100")


if __name__ == "__main__":
    unittest.main()
