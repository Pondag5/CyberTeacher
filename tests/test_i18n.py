"""
Tests for i18n localization system.
"""

import unittest
from unittest.mock import patch

from i18n import get_available_languages, get_locale, t


class TestI18n(unittest.TestCase):
    """Tests for i18n localization system."""

    def test_get_locale_ru(self):
        locale = get_locale("ru")
        self.assertIn("ui", locale)
        self.assertEqual(locale["language_name"], "Русский")

    def test_get_locale_en(self):
        locale = get_locale("en")
        self.assertIn("ui", locale)
        self.assertEqual(locale["language_name"], "English")

    def test_get_locale_fallback(self):
        locale = get_locale("nonexistent")
        self.assertIn("ui", locale)
        self.assertEqual(locale["language_name"], "Русский")

    def test_t_simple_key(self):
        result = t("ru", "ui.welcome")
        self.assertIn("Добро пожаловать", result)

    def test_t_english_key(self):
        result = t("en", "ui.welcome")
        self.assertIn("Welcome", result)

    def test_t_with_interpolation(self):
        result = t("ru", "ui.error", error="test error")
        self.assertIn("test error", result)

    def test_t_unknown_key_returns_key(self):
        result = t("ru", "nonexistent.key")
        self.assertEqual(result, "nonexistent.key")

    def test_get_available_languages(self):
        langs = get_available_languages()
        self.assertGreaterEqual(len(langs), 2)
        codes = [lang["code"] for lang in langs]
        self.assertIn("ru", codes)
        self.assertIn("en", codes)

    def test_t_nested_key(self):
        result = t("ru", "ui.health.title")
        self.assertIsNotNone(result)
        self.assertNotEqual(result, "ui.health.title")

    def test_t_english_nested_key(self):
        result = t("en", "ui.profile.name_empty")
        self.assertIn("cannot be empty", result)


if __name__ == "__main__":
    unittest.main()
