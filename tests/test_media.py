"""Тесты для модуля Video/Podcasts Player (M-16)."""

import unittest
from unittest.mock import patch

from handlers.media import (
    MEDIA_RESOURCES,
    _play_resource,
    _show_notes,
    handle_media,
)


class TestMediaPlayer(unittest.TestCase):
    """Тесты медиа-плеера."""

    def test_display_media(self):
        """Отображение списка ресурсов."""
        with patch("handlers.media.console.print"):
            _, result, _, action_taken = handle_media("")
            self.assertTrue(action_taken)

    def test_play_valid_resource(self):
        """Воспроизведение существующего ресурса."""
        with patch("handlers.media.console.print"):
            success = _play_resource("yt_sql_injection")
            self.assertTrue(success)

    def test_play_invalid_resource(self):
        """Воспроизведение несуществующего ресурса."""
        with patch("handlers.media.console.print"):
            success = _play_resource("nonexistent")
            self.assertFalse(success)

    def test_show_notes_valid(self):
        """Показ конспекта существующего ресурса."""
        with patch("handlers.media.console.print"):
            success = _show_notes("podcast_darknet")
            self.assertTrue(success)

    def test_show_notes_invalid(self):
        """Показ конспекта несуществующего ресурса."""
        with patch("handlers.media.console.print"):
            success = _show_notes("nonexistent")
            self.assertFalse(success)

    def test_help_command(self):
        """Вызов справки /media help."""
        with patch("handlers.media.console.print"):
            _, result, _, action_taken = handle_media("help")
            self.assertTrue(action_taken)

    def test_unknown_subcommand(self):
        """Неизвестная подкоманда."""
        with patch("handlers.media.console.print"):
            _, result, _, action_taken = handle_media("unknown")
            self.assertTrue(action_taken)

    def test_media_structure(self):
        """Проверка структуры ресурсов."""
        self.assertGreater(len(MEDIA_RESOURCES), 0)
        for mid, res in MEDIA_RESOURCES.items():
            self.assertIn("title", res)
            self.assertIn("type", res)
            self.assertIn("url", res)
            self.assertIn("duration", res)
            self.assertIn("topic", res)
            self.assertIn("summary", res)
            self.assertIn("key_points", res)
            self.assertIn("xp", res)


if __name__ == "__main__":
    unittest.main()
