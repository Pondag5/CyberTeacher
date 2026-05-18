"""Тесты для модуля Voice STT (M-11)."""

import unittest
from unittest.mock import patch

from handlers.voice import (
    SIMULATED_PHRASES,
    STT_AVAILABLE,
    _handle_voice_listen,
    handle_voice,
)


class TestVoiceSTT(unittest.TestCase):
    """Тесты распознавания речи."""

    def test_voice_listen(self):
        """Команда /voice listen."""
        with patch("handlers.voice.console.print"):
            success, text, _ = handle_voice("voice listen")
            self.assertTrue(success)
            self.assertIn(text, SIMULATED_PHRASES)

    def test_handle_voice_listen(self):
        """Функция _handle_voice_listen."""
        with patch("handlers.voice.console.print"):
            success, text, _ = _handle_voice_listen()
            self.assertTrue(success)
            self.assertIn(text, SIMULATED_PHRASES)

    def test_voice_status_includes_stt(self):
        """Статус голоса включает STT."""
        with patch("handlers.voice.console.print"):
            success, text, _ = handle_voice("voice status")
            self.assertTrue(success)
            self.assertIn("STT", text)

    def test_stt_available_flag(self):
        """Флаг STT_AVAILABLE определён."""
        self.assertIsInstance(STT_AVAILABLE, bool)

    def test_simulated_phrases_exist(self):
        """Фразы для симуляции существуют."""
        self.assertGreater(len(SIMULATED_PHRASES), 0)
        for phrase in SIMULATED_PHRASES:
            self.assertIsInstance(phrase, str)
            self.assertGreater(len(phrase), 0)


if __name__ == "__main__":
    unittest.main()
