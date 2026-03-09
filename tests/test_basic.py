"""Тесты для CyberTeacher"""
import unittest
import sys
import os

# Добавляем корень проекта в путь
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestQuiz(unittest.TestCase):
    def test_generate_quiz(self):
        from question_generation import generate_open_quiz
        quiz = generate_open_quiz()
        self.assertIn('question', quiz)
        self.assertIn('answer', quiz)
        self.assertIn('key_points', quiz)
        self.assertTrue(len(quiz['question']) > 0)

    def test_check_answer(self):
        from question_generation import check_open_answer
        result = check_open_answer("Что такое SQLi?", "внедрение sql", ["внедрение", "sql"])
        self.assertIn('score', result)
        self.assertIn('feedback', result)

class TestNews(unittest.TestCase):
    def test_fetch_news(self):
        from news_fetcher import fetch_news
        news = fetch_news(force=True)
        self.assertIsInstance(news, list)

class TestCache(unittest.TestCase):
    def test_ollama_cache(self):
        from ollama_client import OllamaClient
        client = OllamaClient()
        # Первый вызов - кэш пуст
        r1 = client.invoke("тест")
        # Второй вызов - должен быть из кэша
        r2 = client.invoke("тест")
        self.assertEqual(r1, r2)
        self.assertGreater(len(client._cache), 0)

if __name__ == '__main__':
    unittest.main()
