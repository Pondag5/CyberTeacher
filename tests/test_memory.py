"""Тесты для модуля memory"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class TestMemory(unittest.TestCase):
    """Тесты для модуля memory с изолированной БД на каждый тест"""

    def setUp(self):
        import config

        self._original_db_file = config.DB_FILE
        config.DB_FILE = ":memory:"
        from memory import init_db

        self.conn = init_db()

    def tearDown(self):
        self.conn.close()
        import config

        config.DB_FILE = self._original_db_file

    def test_init_db_creates_tables(self):
        from memory import init_db  # уже вызван в setUp, но проверим наличие таблиц

        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = {row[0] for row in cursor.fetchall()}
        expected = {"messages", "stats", "progress", "query_cache"}
        self.assertTrue(expected.issubset(tables))

    def test_save_and_get_chat_history(self):
        from memory import save_message, get_chat_history

        save_message(self.conn, "user", "Привет", "teacher")
        save_message(self.conn, "assistant", "Ответ", "teacher")
        history = get_chat_history(self.conn, limit=2)
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]["role"], "user")
        self.assertEqual(history[0]["content"], "Привет")
        self.assertEqual(history[1]["role"], "assistant")
        self.assertEqual(history[1]["mode"], "teacher")

    def test_clear_chat(self):
        from memory import save_message, clear_chat

        save_message(self.conn, "user", "Текст", "teacher")
        save_message(self.conn, "assistant", "Ответ", "teacher")
        clear_chat(self.conn)
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM messages")
        count = cursor.fetchone()[0]
        self.assertEqual(count, 0)

    def test_update_and_get_stats(self):
        from memory import update_stats, get_stats

        # При increment quizzes/tasks к points тоже добавляется указанное значение (1)
        update_stats(self.conn, 10, "points")  # +10 points
        update_stats(self.conn, 1, "quizzes_passed")  # +1 point and quizzes +1
        update_stats(self.conn, 1, "tasks_solved")  # +1 point and tasks +1
        stats = get_stats(self.conn)
        self.assertEqual(stats["points"], 12)  # 10 + 1 + 1
        self.assertEqual(stats["quizzes"], 1)
        self.assertEqual(stats["tasks"], 1)

    def test_update_topic_progress_creates_new(self):
        from memory import update_topic_progress

        update_topic_progress(self.conn, "sql", True)
        cursor = self.conn.cursor()
        cursor.execute("SELECT correct, total FROM progress WHERE topic='sql'")
        row = cursor.fetchone()
        self.assertEqual(row, (1, 1))

    def test_update_topic_progress_updates_existing(self):
        from memory import update_topic_progress

        update_topic_progress(self.conn, "xss", True)
        update_topic_progress(self.conn, "xss", False)
        cursor = self.conn.cursor()
        cursor.execute("SELECT correct, total FROM progress WHERE topic='xss'")
        row = cursor.fetchone()
        self.assertEqual(row, (1, 2))

    def test_get_weak_topics_filters_below_60(self):
        from memory import update_topic_progress, get_weak_topics

        # Создаём тему с 33% успехом (1 из 3)
        for _ in range(2):
            update_topic_progress(self.conn, "sqli", False)
        update_topic_progress(self.conn, "sqli", True)
        weak = get_weak_topics(self.conn, limit=3)
        topics = [t["topic"] for t in weak]
        self.assertIn("sqli", topics)
        # Проверим rate
        sqli_entry = next(t for t in weak if t["topic"] == "sqli")
        self.assertEqual(sqli_entry["rate"], 33)

    def test_cache_response_and_get(self):
        from memory import cache_response, get_cached_response

        cache_response(self.conn, "hash1", '{"result": "ok"}', ttl_seconds=3600)
        resp = get_cached_response(self.conn, "hash1")
        self.assertEqual(resp, '{"result": "ok"}')

    def test_cleanup_expired_cache(self):
        from memory import cache_response, cleanup_expired_cache, get_cache_stats

        cache_response(self.conn, "h1", "valid", ttl_seconds=3600)
        cache_response(self.conn, "h2", "expired", ttl_seconds=0)
        # manually set expires_at in past for h2
        cursor = self.conn.cursor()
        past = "2000-01-01T00:00:00"
        cursor.execute(
            "UPDATE query_cache SET expires_at = ? WHERE query_hash='h2'", (past,)
        )
        self.conn.commit()
        cleanup_expired_cache(self.conn)
        stats = get_cache_stats(self.conn)
        self.assertEqual(stats["total"], 1)
        self.assertEqual(stats["valid"], 1)
        self.assertEqual(stats["expired"], 0)

    def test_sanitize_log_removes_sensitive(self):
        from config import sanitize_log

        # Используем quoted value, чтобы соответствовать паттерну
        sensitive = 'password="12345"'
        sanitized = sanitize_log(sensitive)
        self.assertNotIn("12345", sanitized)
        self.assertIn("password=***", sanitized)


if __name__ == "__main__":
    unittest.main()
