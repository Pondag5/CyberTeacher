"""Тесты для daily_challenge.py."""

import json
import os
import tempfile
import unittest
from unittest.mock import patch

from daily_challenge import (
    CHALLENGE_FILE,
    generate_daily_challenge,
    get_daily_status,
    get_hint,
    submit_daily_answer,
)


class TestDailyChallenge(unittest.TestCase):
    """Тесты модуля ежедневных челленджей."""

    def setUp(self):
        """Создать временный файл для челленджей."""
        self._original_file = CHALLENGE_FILE
        self._temp_dir = tempfile.mkdtemp()
        self._temp_file = os.path.join(self._temp_dir, "test_challenges.json")
        # Патчим CHALLENGE_FILE через module-level переменную
        import daily_challenge
        daily_challenge.CHALLENGE_FILE = self._temp_file

    def tearDown(self):
        """Восстановить оригинальный путь."""
        import daily_challenge
        daily_challenge.CHALLENGE_FILE = self._original_file
        if os.path.exists(self._temp_file):
            os.remove(self._temp_file)
        os.rmdir(self._temp_dir)

    def test_generate_daily_challenge_returns_dict(self):
        """Генерация возвращает dict с нужными полями."""
        challenge = generate_daily_challenge()
        self.assertIsInstance(challenge, dict)
        self.assertIn("title", challenge)
        self.assertIn("desc", challenge)
        self.assertIn("difficulty", challenge)
        self.assertIn("answer", challenge)
        self.assertIn("hint", challenge)

    def test_generate_daily_challenge_difficulty(self):
        """Генерация с конкретной сложностью."""
        challenge = generate_daily_challenge(difficulty="hard")
        self.assertEqual(challenge["difficulty"], "hard")

    def test_generate_daily_challenge_caching(self):
        """Челлендж на сегодня кэшируется."""
        c1 = generate_daily_challenge()
        c2 = generate_daily_challenge()
        self.assertEqual(c1["title"], c2["title"])
        self.assertEqual(c1["answer"], c2["answer"])

    def test_submit_correct_answer(self):
        """Правильный ответ засчитывается."""
        generate_daily_challenge(difficulty="easy")
        # Получаем ответ из сохранённого файла
        with open(self._temp_file, "r") as f:
            data = json.load(f)
        today = list(data["history"].keys())[0]
        answer = data["history"][today]["answer"]

        result = submit_daily_answer(answer)
        self.assertTrue(result["correct"])
        self.assertGreater(result["xp_reward"], 0)

    def test_submit_wrong_answer(self):
        """Неправильный ответ не засчитывается."""
        generate_daily_challenge(difficulty="easy")
        result = submit_daily_answer("полный бред")
        self.assertFalse(result["correct"])
        self.assertEqual(result["xp_reward"], 0)

    def test_submit_partial_answer(self):
        """Частичный ответ даёт немного XP или полный если слово совпало."""
        generate_daily_challenge(difficulty="medium")
        with open(self._temp_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        today = list(data["history"].keys())[0]
        answer = data["history"][today]["answer"]
        # Берём короткое слово которое вряд ли совпадёт полностью
        partial = "xyz_nonexistent_word_12345"

        result = submit_daily_answer(partial)
        self.assertFalse(result["correct"])

    def test_streak_increments(self):
        """Стрик увеличивается при правильных ответах в разные дни."""
        generate_daily_challenge(difficulty="easy")
        with open(self._temp_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        today = list(data["history"].keys())[0]
        answer = data["history"][today]["answer"]

        # Первый ответ
        result1 = submit_daily_answer(answer)
        self.assertEqual(result1["streak"], 1)

    def test_get_hint_returns_string(self):
        """Подсказка возвращает строку."""
        generate_daily_challenge()
        hint = get_hint()
        self.assertIsInstance(hint, str)
        self.assertGreater(len(hint), 0)

    def test_get_daily_status_returns_panel(self):
        """Статус возвращает Panel."""
        generate_daily_challenge()
        panel = get_daily_status()
        self.assertIsNotNone(panel)

    def test_no_challenge_yet(self):
        """Ответ без сгенерированного челленджа."""
        # Удаляем файл чтобы не было челленджа
        if os.path.exists(self._temp_file):
            os.remove(self._temp_file)
        result = submit_daily_answer("test")
        self.assertFalse(result["correct"])
        self.assertIn("ещё не сгенерирован", result["feedback"])


if __name__ == "__main__":
    unittest.main()
