"""Тесты для config"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class TestConfig(unittest.TestCase):
    def test_lazy_loader_llm(self):
        """Тест что LazyLoader.get_llm() возвращает объект с методом invoke"""
        from config import LazyLoader

        llm = LazyLoader.get_llm()
        self.assertTrue(hasattr(llm, "invoke"))
        self.assertTrue(callable(llm.invoke))

    def test_teacher_prompt_exists(self):
        """Тест что файл teacher_prompt.txt существует и не пустой"""
        path = "./config/teacher_prompt.txt"
        self.assertTrue(os.path.exists(path))
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertGreater(len(content), 0)


if __name__ == "__main__":
    unittest.main()
