"""
Тесты для песочницы кода (C-08)
"""

import unittest
import os
import sys
from unittest.mock import patch, MagicMock

# Добавляем путь к проекту
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from handlers.sandbox import validate_code, run_code_in_sandbox


class TestSandboxValidation(unittest.TestCase):
    """Тесты валидации кода"""
    
    def test_python_simple_code_allowed(self):
        """Простой Python код должен проходить валидацию"""
        code = "print('Hello, World!')"
        error = validate_code(code, 'python')
        self.assertEqual(error, "")
    
    def test_python_forbidden_import_os(self):
        """Импорт os запрещён"""
        code = "import os; os.system('ls')"
        error = validate_code(code, 'python')
        self.assertIn("запрещённый модуль", error)
    
    def test_python_forbidden_subprocess(self):
        """subprocess запрещён"""
        code = "import subprocess; subprocess.run(['ls'])"
        error = validate_code(code, 'python')
        self.assertTrue(error)  # любая ошибка
    
    def test_python_forbidden_eval(self):
        """eval запрещён"""
        code = "eval('1+1')"
        error = validate_code(code, 'python')
        self.assertIn("eval", error.lower())
    
    def test_python_forbidden_open(self):
        """open запрещён"""
        code = "open('/etc/passwd')"
        error = validate_code(code, 'python')
        self.assertIn("open", error.lower())
    
    def test_python_forbidden_exec(self):
        """exec запрещён"""
        code = "exec('print(1)')"
        error = validate_code(code, 'python')
        self.assertIn("exec", error.lower())
    
    def test_bash_simple_command_allowed(self):
        """Простая bash команда должна проходить"""
        code = "echo Hello"
        error = validate_code(code, 'bash')
        self.assertEqual(error, "")
    
    def test_bash_forbidden_rm_rf(self):
        """rm -rf запрещён"""
        code = "rm -rf /"
        error = validate_code(code, 'bash')
        self.assertIn("удаление", error.lower())
    
    def test_bash_forbidden_cat_etc(self):
        """cat /etc/passwd запрещён"""
        code = "cat /etc/passwd"
        error = validate_code(code, 'bash')
        self.assertTrue(error)  # любая ошибка
    
    def test_bash_forbidden_sudo(self):
        """sudo запрещён"""
        code = "sudo apt update"
        error = validate_code(code, 'bash')
        self.assertIn("sudo", error.lower())
    
    def test_bash_forbidden_chmod(self):
        """chmod запрещён"""
        code = "chmod 777 /tmp/file"
        error = validate_code(code, 'bash')
        self.assertIn("chmod", error.lower())
    
    def test_bash_forbidden_redirect(self):
        """>> перенаправление запрещено"""
        code = "echo test >> /etc/file"
        error = validate_code(code, 'bash')
        self.assertIn("перенаправление", error.lower())


class TestSandboxIntegration(unittest.TestCase):
    """Интеграционные тесты (требуют Docker)"""
    
    @unittest.skipUnless(os.environ.get('RUN_DOCKER_TESTS'), "Docker tests disabled by default")
    def test_python_hello_world(self):
        """Hello world на Python должен выполниться"""
        result = run_code_in_sandbox("print('Hello, World!')", 'python')
        self.assertTrue(result['success'])
        self.assertEqual(result['returncode'], 0)
        self.assertIn('Hello', result['stdout'])
    
    @unittest.skipUnless(os.environ.get('RUN_DOCKER_TESTS'), "Docker tests disabled by default")
    def test_python_syntax_error(self):
        """Код с синтаксической ошибкой должен возвращать ненулевой код"""
        result = run_code_in_sandbox("print('unclosed string", 'python')
        self.assertTrue(result['success'])
        self.assertNotEqual(result['returncode'], 0)
    
    @unittest.skipUnless(os.environ.get('RUN_DOCKER_TESTS'), "Docker tests disabled by default")
    def test_bash_echo(self):
        """Bash echo должен работать"""
        result = run_code_in_sandbox("echo 'Test'", 'bash')
        self.assertTrue(result['success'])
        self.assertEqual(result['returncode'], 0)
        self.assertIn('Test', result['stdout'])
    
    def test_invalid_language(self):
        """Неизвестный язык должен возвращать ошибку валидации"""
        result = run_code_in_sandbox("print('test')", 'unknown')
        self.assertFalse(result['success'])
        self.assertIn("Неподдерживаемый язык", result.get('error', ''))


if __name__ == '__main__':
    unittest.main()
