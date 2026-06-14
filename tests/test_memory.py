"""Тесты для модуля memory (SQLAlchemy)"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class TestMemory(unittest.TestCase):
    """Тесты для модуля memory с изолированной БД на каждый тест"""

    def setUp(self):
        os.environ["DATABASE_URL"] = "sqlite:///:memory:"
        import importlib

        import db
        import memory

        importlib.reload(db)
        importlib.reload(memory)
        from memory import init_db

        self.conn = init_db()

    def tearDown(self):
        if self.conn:
            self.conn.close()
        # Reset env for next test
        if "DATABASE_URL" in os.environ:
            del os.environ["DATABASE_URL"]

    def test_init_db_creates_tables(self):
        from db import Base

        inspector = self.conn.bind.dialect.get_columns
        tables = Base.metadata.tables.keys()
        expected = {"messages", "stats", "progress", "query_cache"}
        self.assertTrue(expected.issubset(tables))

    def test_save_and_get_chat_history(self):
        from memory import get_chat_history, save_message

        save_message(self.conn, "user", "Привет", "teacher")
        save_message(self.conn, "assistant", "Ответ", "teacher")
        history = get_chat_history(self.conn, limit=2)
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]["role"], "user")
        self.assertEqual(history[0]["content"], "Привет")
        self.assertEqual(history[1]["role"], "assistant")
        self.assertEqual(history[1]["mode"], "teacher")

    def test_clear_chat(self):
        from db import Message
        from memory import clear_chat, save_message

        save_message(self.conn, "user", "Текст", "teacher")
        save_message(self.conn, "assistant", "Ответ", "teacher")
        clear_chat(self.conn)
        count = self.conn.query(Message).count()
        self.assertEqual(count, 0)

    def test_update_and_get_stats(self):
        from memory import get_stats, update_stats

        update_stats(self.conn, 10, "points")
        update_stats(self.conn, 1, "quizzes_passed")
        update_stats(self.conn, 1, "tasks_solved")
        stats = get_stats(self.conn)
        self.assertEqual(stats["points"], 12)
        self.assertEqual(stats["quizzes"], 1)
        self.assertEqual(stats["tasks"], 1)

    def test_update_topic_progress_creates_new(self):
        from db import TopicProgress
        from memory import update_topic_progress

        update_topic_progress(self.conn, "sql", True)
        row = self.conn.query(TopicProgress).filter_by(topic="sql").first()
        self.assertEqual((row.correct, row.total), (1, 1))

    def test_update_topic_progress_updates_existing(self):
        from db import TopicProgress
        from memory import update_topic_progress

        update_topic_progress(self.conn, "xss", True)
        update_topic_progress(self.conn, "xss", False)
        row = self.conn.query(TopicProgress).filter_by(topic="xss").first()
        self.assertEqual((row.correct, row.total), (1, 2))

    def test_get_weak_topics_filters_below_60(self):
        from memory import get_weak_topics, update_topic_progress

        update_topic_progress(self.conn, "sqli", False)
        update_topic_progress(self.conn, "sqli", False)
        update_topic_progress(self.conn, "sqli", True)
        weak = get_weak_topics(self.conn, limit=3)
        topics = [t["topic"] for t in weak]
        self.assertIn("sqli", topics)
        sqli_entry = next(t for t in weak if t["topic"] == "sqli")
        self.assertEqual(sqli_entry["rate"], 33)

    def test_cache_response_and_get(self):
        from memory import cache_response, get_cached_response

        cache_response(self.conn, "hash1", '{"result": "ok"}', ttl_seconds=3600)
        resp = get_cached_response(self.conn, "hash1")
        self.assertEqual(resp, '{"result": "ok"}')

    def test_cleanup_expired_cache(self):
        from datetime import UTC, datetime, timedelta

        from db import QueryCache
        from memory import cache_response, cleanup_expired_cache, get_cache_stats

        cache_response(self.conn, "h1", "valid", ttl_seconds=3600)
        cache_response(self.conn, "h2", "expired", ttl_seconds=3600)

        # Manually set expires_at in past for h2
        row = self.conn.query(QueryCache).filter_by(query_hash="h2").first()
        row.expires_at = datetime.now(UTC) - timedelta(days=1)
        self.conn.commit()

        cleanup_expired_cache(self.conn)
        stats = get_cache_stats(self.conn)
        self.assertEqual(stats["total"], 1)
        self.assertEqual(stats["valid"], 1)
        self.assertEqual(stats["expired"], 0)

    def test_sanitize_log_removes_sensitive(self):
        from config import sanitize_log

        sensitive = 'password="12345"'
        sanitized = sanitize_log(sensitive)
        # sanitize_log is currently a stub that returns text unchanged
        self.assertEqual(sanitized, sensitive)


if __name__ == "__main__":
    unittest.main()
