"""Тесты для модуля memory"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class TestMemory(unittest.TestCase):
    def test_get_stats(self):
        """Тест get_stats возвращает корректные ключи"""
        from memory import get_stats, init_db

        conn = init_db()
        stats = get_stats(conn)
        self.assertIsInstance(stats, dict)
        self.assertIn("points", stats)
        self.assertIn("quizzes", stats)
        self.assertIn("tasks", stats)
        conn.close()

    def test_init_db(self):
        """Тест инициализации БД - таблицы создаются"""
        from memory import init_db

        conn = init_db()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        self.assertIn("messages", tables)
        self.assertIn("stats", tables)
        conn.close()


if __name__ == "__main__":
    unittest.main()
