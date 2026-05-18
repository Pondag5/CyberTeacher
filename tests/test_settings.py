"""
Tests for Pydantic Settings configuration.
"""

import os
import unittest
from pathlib import Path

from settings import Settings, get_settings, reset_settings


class TestSettings(unittest.TestCase):
    """Tests for Settings class."""

    def setUp(self):
        reset_settings()

    def test_default_values(self):
        s = Settings()
        self.assertIn(s.llm_provider, ["ollama", "groq", "openrouter", "huggingface"])
        self.assertEqual(s.ollama_model, "qwen2.5:7b")
        self.assertEqual(s.model_temperature, 0.3)
        self.assertEqual(s.max_tokens, 2000)
        self.assertTrue(s.socratic_enabled)
        self.assertTrue(s.thinking_enabled)

    def test_model_name_ollama(self):
        s = Settings(llm_provider="ollama", ollama_model="qwen2.5:7b")
        self.assertEqual(s.model_name, "qwen2.5:7b")

    def test_model_name_openrouter(self):
        s = Settings(llm_provider="openrouter", openrouter_model="llama-3.3-70b")
        self.assertEqual(s.model_name, "llama-3.3-70b")

    def test_model_name_huggingface(self):
        s = Settings(llm_provider="huggingface", hf_model="mixtral-8x7b")
        self.assertEqual(s.model_name, "mixtral-8x7b")

    def test_ensure_dirs_creates_directories(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            s = Settings(
                persist_dir=Path(tmpdir) / "embeddings",
                db_file=Path(tmpdir) / "memory" / "chat.db",
                knowledge_dir=Path(tmpdir) / "kb",
                state_file=Path(tmpdir) / "memory" / "state.json",
                achievements_file=Path(tmpdir) / "data" / "ach.json",
                response_cache_file=Path(tmpdir) / "memory" / "cache.json",
            )
            s.ensure_dirs()
            self.assertTrue((Path(tmpdir) / "embeddings").exists())
            self.assertTrue((Path(tmpdir) / "memory").exists())
            self.assertTrue((Path(tmpdir) / "kb").exists())
            self.assertTrue((Path(tmpdir) / "data").exists())

    def test_temperature_validation(self):
        s = Settings(model_temperature=0.0)
        self.assertEqual(s.model_temperature, 0.0)
        s = Settings(model_temperature=2.0)
        self.assertEqual(s.model_temperature, 2.0)

    def test_max_tokens_positive(self):
        s = Settings(max_tokens=500)
        self.assertEqual(s.max_tokens, 500)

    def test_get_settings_singleton(self):
        reset_settings()
        s1 = get_settings()
        s2 = get_settings()
        self.assertIs(s1, s2)


if __name__ == "__main__":
    unittest.main()
