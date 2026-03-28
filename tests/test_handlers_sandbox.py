"""Unit tests for handlers/sandbox.py"""

import unittest
from unittest.mock import MagicMock, patch
from rich.panel import Panel


class TestSandboxFunctions(unittest.TestCase):
    """Tests for sandbox handler functions"""

    def test_validate_code_unsupported_language(self):
        from handlers.sandbox import validate_code

        error = validate_code("print('hello')", "java")
        self.assertIn("Неподдерживаемый язык", error)

    def test_validate_code_python_forbidden_import(self):
        from handlers.sandbox import validate_code

        code = "import os; os.system('ls')"
        error = validate_code(code, "python")
        self.assertIn("запрещённый модуль", error)

    def test_validate_code_python_forbidden_exec(self):
        from handlers.sandbox import validate_code

        code = "exec('print(1)')"
        error = validate_code(code, "python")
        self.assertIn("exec()", error)

    def test_validate_code_python_forbidden_open(self):
        from handlers.sandbox import validate_code

        code = "open('/etc/passwd')"
        error = validate_code(code, "python")
        self.assertIn("open()", error)

    def test_validate_code_python_forbidden_subprocess(self):
        from handlers.sandbox import validate_code

        code = "import subprocess; subprocess.run(['ls'])"
        error = validate_code(code, "python")
        self.assertTrue(error)  # non-empty error

    def test_validate_code_bash_forbidden_rm(self):
        from handlers.sandbox import validate_code

        code = "rm -rf /"
        error = validate_code(code, "bash")
        self.assertIn("удаление файлов", error)

    def test_validate_code_bash_forbidden_sudo(self):
        from handlers.sandbox import validate_code

        code = "sudo apt-get install"
        error = validate_code(code, "bash")
        self.assertIn("sudo", error)

    def test_validate_code_bash_forbidden_etc(self):
        from handlers.sandbox import validate_code

        code = "cat /etc/passwd"
        error = validate_code(code, "bash")
        self.assertIn("/etc", error)

    def test_validate_code_safe_python(self):
        from handlers.sandbox import validate_code

        code = "print('Hello, World!')"
        error = validate_code(code, "python")
        self.assertEqual(error, "")

    def test_validate_code_safe_bash(self):
        from handlers.sandbox import validate_code

        code = "echo 'Hello'"
        error = validate_code(code, "bash")
        self.assertEqual(error, "")

    @patch("handlers.sandbox.console.print")
    def test_handle_sandbox_no_args(self, mock_print):
        from handlers.sandbox import handle_sandbox

        result = handle_sandbox("")
        self.assertEqual(result, (True, None, None, True))
        mock_print.assert_any_call(
            "[red]Использование: /sandbox <python|bash> <код>[/red]"
        )

    @patch("handlers.sandbox.console.print")
    @patch("handlers.sandbox.validate_code", return_value="error msg")
    def test_handle_sandbox_validation_fails(self, mock_validate, mock_print):
        from handlers.sandbox import handle_sandbox

        result = handle_sandbox("python print(1)")
        self.assertEqual(result, (True, None, None, True))
        mock_print.assert_any_call("[red]❌ Ошибка: error msg[/red]")

    @patch("handlers.sandbox.console.print")
    @patch("handlers.sandbox.run_code_in_sandbox")
    def test_handle_sandbox_successful_execution(self, mock_run, mock_print):
        from handlers.sandbox import handle_sandbox

        mock_run.return_value = {
            "success": True,
            "returncode": 0,
            "stdout": "Hello",
            "stderr": "",
            "container": "sandbox_abc123",
        }
        result = handle_sandbox("python print('Hello')")
        self.assertEqual(result, (True, None, None, True))
        mock_print.assert_any_call("[green]✅ Код выполнен успешно[/green]")
        # Check that Panel for STDOUT was printed
        panel_call = next(
            call
            for call in mock_print.call_args_list
            if isinstance(call.args[0], Panel)
        )
        self.assertEqual(panel_call.args[0].title, "STDOUT")

    @patch("handlers.sandbox.console.print")
    @patch("handlers.sandbox.run_code_in_sandbox")
    def test_handle_sandbox_execution_with_error(self, mock_run, mock_print):
        from handlers.sandbox import handle_sandbox

        mock_run.return_value = {
            "success": True,
            "returncode": 1,
            "stdout": "",
            "stderr": "SyntaxError",
            "container": "sandbox_xyz",
        }
        result = handle_sandbox("python bad_code")
        self.assertEqual(result, (True, None, None, True))
        mock_print.assert_any_call("[yellow]⚠️ Код завершился с кодом 1[/yellow]")
        # Check that Panel for STDERR was printed
        panel_call = next(
            call
            for call in mock_print.call_args_list
            if isinstance(call.args[0], Panel)
        )
        self.assertEqual(panel_call.args[0].title, "STDERR")

    @patch("handlers.sandbox.console.print")
    @patch("handlers.sandbox.run_code_in_sandbox")
    def test_handle_sandbox_no_output(self, mock_run, mock_print):
        from handlers.sandbox import handle_sandbox

        mock_run.return_value = {
            "success": True,
            "returncode": 0,
            "stdout": "",
            "stderr": "",
            "container": "sandbox_none",
        }
        result = handle_sandbox("bash echo 'test'")
        self.assertEqual(result, (True, None, None, True))
        mock_print.assert_any_call("[dim](нет вывода)[/dim]")


if __name__ == "__main__":
    unittest.main()
