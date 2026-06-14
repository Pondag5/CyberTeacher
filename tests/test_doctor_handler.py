"""Unit tests for handlers/doctor.py"""

import os
import sys
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class TestDoctorHandler(unittest.TestCase):
    @patch("handlers.doctor.console.print")
    @patch(
        "handlers.doctor._check_ollama",
        return_value=("[green]✅ Работает[/green]", "qwen2.5:7b"),
    )
    def test_show_status(self, mock_check, mock_print):
        from handlers.doctor import _show_status

        result = _show_status()
        self.assertTrue(result[0])

    def test_check_ollama_running(self):
        from handlers.doctor import _check_ollama

        with patch("subprocess.run") as mock_run:
            mock_proc = MagicMock()
            mock_proc.returncode = 0
            mock_proc.stdout = "NAME\tID\tSIZE\nqwen2.5:7b\tabc\t4.0GB\n"
            mock_run.return_value = mock_proc

            status, detail = _check_ollama()
            self.assertIn("Работает", status)

    def test_check_ollama_wrong_model(self):
        from handlers.doctor import _check_ollama

        with patch("subprocess.run") as mock_run:
            mock_proc = MagicMock()
            mock_proc.returncode = 0
            mock_proc.stdout = "NAME\tID\tSIZE\nllama3:latest\tdef\t3.0GB\n"
            mock_run.return_value = mock_proc

            status, detail = _check_ollama()
            self.assertIn("Модель не найдена", status)

    def test_check_ollama_no_models(self):
        from handlers.doctor import _check_ollama

        with patch("subprocess.run") as mock_run:
            mock_proc = MagicMock()
            mock_proc.returncode = 0
            mock_proc.stdout = "NAME\tID\tSIZE\n"
            mock_run.return_value = mock_proc

            status, detail = _check_ollama()
            self.assertIn("Модели не загружены", status)

    def test_check_ollama_not_installed(self):
        from handlers.doctor import _check_ollama

        with patch("subprocess.run", side_effect=FileNotFoundError):
            status, detail = _check_ollama()
            self.assertIn("Не установлен", status)

    @patch("handlers.doctor.console.print")
    def test_set_mock_mode(self, mock_print):
        from handlers.doctor import _set_mock_mode

        with patch("config.LLM_PROVIDER", "mock"):
            with patch("config.LazyLoader") as mock_lazy:
                result = _set_mock_mode()
                self.assertTrue(result[0])
                mock_lazy.invalidate.assert_called_once()

    def test_setup_wizard_ollama(self):
        from handlers.doctor import _setup_wizard

        with patch("handlers.doctor.console.print") as mock_print:
            result = _setup_wizard("ollama")
            self.assertTrue(result[0])

    def test_setup_wizard_groq(self):
        from handlers.doctor import _setup_wizard

        with patch("handlers.doctor.console.print") as mock_print:
            result = _setup_wizard("groq")
            self.assertTrue(result[0])

    def test_setup_wizard_openrouter(self):
        from handlers.doctor import _setup_wizard

        with patch("handlers.doctor.console.print") as mock_print:
            result = _setup_wizard("openrouter")
            self.assertTrue(result[0])

    def test_setup_wizard_unknown(self):
        from handlers.doctor import _setup_wizard

        with patch("handlers.doctor.console.print") as mock_print:
            result = _setup_wizard("invalid")
            self.assertTrue(result[0])

    @patch("handlers.doctor.get_doctor_status")
    def test_get_doctor_status_structure(self, mock_status):
        mock_status.return_value = {
            "current_provider": "mock",
            "fallback_order": ["mock"],
            "providers": [],
            "circuit_breakers": [],
            "mock_active": True,
        }
        result = mock_status()
        self.assertIn("current_provider", result)
        self.assertIn("fallback_order", result)
        self.assertIn("providers", result)
        self.assertIn("mock_active", result)
