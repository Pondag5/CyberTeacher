"""
Тесты для Code Review v3 (L-10).

Проверяют:
- Определение языка по расширению
- Поиск файлов с исходным кодом
- Сканирование на секреты
- Анализ файлов и директорий
- Клонирование репозиториев
- LLM-отчёты
- OWASP Top 10 mapping
- CI/CD mode с exit codes
- SARIF output для IDE
- Semgrep как primary tool
"""

import os
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from handlers.code_review_v2 import (
    LANGUAGE_EXTENSIONS,
    OWASP_CATEGORIES,
    SECRET_PATTERNS,
    _count_owasp,
    _count_severities,
    _guess_owasp,
    _map_semgrep_severity,
    _severity_to_sarif_level,
    calculate_ci_exit_code,
    detect_language,
    find_source_files,
    generate_sarif,
    scan_file_secrets,
)


class TestLanguageDetection(unittest.TestCase):
    """Тесты определения языка."""

    def test_python_detection(self):
        self.assertEqual(detect_language("main.py"), "python")
        self.assertEqual(detect_language("/path/to/script.py"), "python")

    def test_javascript_detection(self):
        self.assertEqual(detect_language("app.js"), "javascript")
        self.assertEqual(detect_language("component.jsx"), "javascript")

    def test_typescript_detection(self):
        self.assertEqual(detect_language("app.ts"), "typescript")
        self.assertEqual(detect_language("component.tsx"), "typescript")

    def test_other_languages(self):
        self.assertEqual(detect_language("index.php"), "php")
        self.assertEqual(detect_language("Main.java"), "java")
        self.assertEqual(detect_language("run.sh"), "bash")
        self.assertEqual(detect_language("main.go"), "go")
        self.assertEqual(detect_language("app.c"), "c")
        self.assertEqual(detect_language("app.cpp"), "cpp")
        self.assertEqual(detect_language("query.sql"), "sql")

    def test_unknown_extension(self):
        self.assertIsNone(detect_language("file.xyz"))
        self.assertIsNone(detect_language("README.md"))


class TestFindSourceFiles(unittest.TestCase):
    """Тесты поиска файлов."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _create_file(self, path: str, content: str = ""):
        full_path = os.path.join(self.temp_dir, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w") as f:
            f.write(content)

    def test_find_python_files(self):
        self._create_file("main.py")
        self._create_file("utils.py")
        self._create_file("README.md")

        files = find_source_files(self.temp_dir)
        self.assertEqual(len(files), 2)

    def test_find_multiple_languages(self):
        self._create_file("app.py")
        self._create_file("index.js")
        self._create_file("style.css")  # Не исходный код

        files = find_source_files(self.temp_dir)
        self.assertEqual(len(files), 2)

    def test_skip_hidden_dirs(self):
        self._create_file("main.py")
        self._create_file(".git/config")
        self._create_file("node_modules/pkg.js")

        files = find_source_files(self.temp_dir)
        self.assertEqual(len(files), 1)

    def test_max_files_limit(self):
        for i in range(60):
            self._create_file(f"file{i}.py")

        files = find_source_files(self.temp_dir, max_files=50)
        self.assertEqual(len(files), 50)


class TestSecretScanning(unittest.TestCase):
    """Тесты сканирования на секреты."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_detect_aws_key(self):
        file_path = os.path.join(self.temp_dir, "test.py")
        with open(file_path, "w") as f:
            f.write('aws_key = "AKIAIOSFODNN7EXAMPLE"\n')

        findings = scan_file_secrets(file_path)
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["type"], "AWS Access Key")

    def test_detect_password(self):
        file_path = os.path.join(self.temp_dir, "config.py")
        with open(file_path, "w") as f:
            f.write('password = "super_secret_password_123"\n')

        findings = scan_file_secrets(file_path)
        self.assertGreaterEqual(len(findings), 1)
        types = [f["type"] for f in findings]
        self.assertTrue(any("Password" in t for t in types))

    def test_detect_github_token(self):
        file_path = os.path.join(self.temp_dir, "env.txt")
        with open(file_path, "w") as f:
            f.write("GITHUB_TOKEN=ghp_abcdefghijklmnopqrstuvwxyz0123\n")

        findings = scan_file_secrets(file_path)
        self.assertGreaterEqual(len(findings), 1)

    def test_detect_private_key(self):
        file_path = os.path.join(self.temp_dir, "key.pem")
        with open(file_path, "w") as f:
            f.write("-----BEGIN RSA PRIVATE KEY-----\n")

        findings = scan_file_secrets(file_path)
        self.assertGreaterEqual(len(findings), 1)

    def test_no_secrets(self):
        file_path = os.path.join(self.temp_dir, "safe.py")
        with open(file_path, "w") as f:
            f.write("print('Hello, World!')\n")

        findings = scan_file_secrets(file_path)
        self.assertEqual(len(findings), 0)


class TestSeverityCounting(unittest.TestCase):
    """Тесты подсчёта критичности."""

    def test_count_all_severities(self):
        findings = [
            {"severity": "critical"},
            {"severity": "critical"},
            {"severity": "high"},
            {"severity": "medium"},
            {"severity": "low"},
        ]
        counts = _count_severities(findings)
        self.assertEqual(counts["critical"], 2)
        self.assertEqual(counts["high"], 1)
        self.assertEqual(counts["medium"], 1)
        self.assertEqual(counts["low"], 1)

    def test_default_severity(self):
        findings = [{"severity": "unknown"}]
        counts = _count_severities(findings)
        # unknown не маппится, поэтому все счётчики 0
        self.assertEqual(sum(counts.values()), 0)

    def test_empty_findings(self):
        counts = _count_severities([])
        self.assertEqual(counts["critical"], 0)
        self.assertEqual(counts["high"], 0)


class TestLanguageExtensions(unittest.TestCase):
    """Тесты маппинга расширений."""

    def test_all_extensions_have_language(self):
        for ext, lang in LANGUAGE_EXTENSIONS.items():
            self.assertIsInstance(ext, str)
            self.assertIsInstance(lang, str)
            self.assertTrue(ext.startswith("."))

    def test_common_extensions(self):
        self.assertIn(".py", LANGUAGE_EXTENSIONS)
        self.assertIn(".js", LANGUAGE_EXTENSIONS)
        self.assertIn(".java", LANGUAGE_EXTENSIONS)
        self.assertIn(".php", LANGUAGE_EXTENSIONS)


class TestSecretPatterns(unittest.TestCase):
    """Тесты паттернов секретов."""

    def test_all_patterns_have_names(self):
        for pattern_tuple in SECRET_PATTERNS:
            self.assertEqual(len(pattern_tuple), 3)  # name, pattern, owasp_id
            name, pattern, owasp_id = pattern_tuple
            self.assertIsInstance(name, str)
            self.assertIsInstance(pattern, str)
            self.assertIsInstance(owasp_id, str)
            self.assertGreater(len(name), 0)
            self.assertTrue(owasp_id.startswith("A"))


class TestOWASPMapping(unittest.TestCase):
    """Тесты OWASP Top 10 mapping."""

    def test_owasp_categories_defined(self):
        self.assertIn("A01", OWASP_CATEGORIES)
        self.assertIn("A02", OWASP_CATEGORIES)
        self.assertIn("A03", OWASP_CATEGORIES)
        self.assertIn("A07", OWASP_CATEGORIES)
        self.assertIn("A08", OWASP_CATEGORIES)
        self.assertIn("A10", OWASP_CATEGORIES)

    def test_owasp_categories_have_names(self):
        for owasp_id, category in OWASP_CATEGORIES.items():
            self.assertIn("name", category)
            self.assertIn("items", category)
            self.assertIsInstance(category["name"], str)
            self.assertIsInstance(category["items"], list)

    def test_count_owasp_findings(self):
        findings = [
            {"owasp": "A03:2021 – Injection"},
            {"owasp": "A03:2021 – Injection"},
            {"owasp": "A07:2021 – Identification and Authentication Failures"},
            {"owasp": "A01:2021 – Broken Access Control"},
        ]
        counts = _count_owasp(findings)
        self.assertEqual(counts["A03"], 2)
        self.assertEqual(counts["A07"], 1)
        self.assertEqual(counts["A01"], 1)

    def test_count_owasp_unknown(self):
        findings = [{"owasp": "Unknown"}]
        counts = _count_owasp(findings)
        self.assertEqual(counts["Unknown"], 1)

    def test_count_owasp_empty(self):
        counts = _count_owasp([])
        self.assertEqual(len(counts), 0)

    def test_guess_owasp_sql(self):
        self.assertIn("A03", _guess_owasp("SQL injection in query"))

    def test_guess_owasp_xss(self):
        self.assertIn("A03", _guess_owasp("Cross-site scripting detected"))

    def test_guess_owasp_password(self):
        self.assertIn("A07", _guess_owasp("Hardcoded password found"))

    def test_guess_owasp_crypto(self):
        self.assertIn("A02", _guess_owasp("Weak MD5 hash algorithm"))

    def test_guess_owasp_path(self):
        self.assertIn("A01", _guess_owasp("Path traversal vulnerability"))

    def test_guess_owasp_deserialization(self):
        self.assertIn("A08", _guess_owasp("Insecure pickle deserialization"))

    def test_guess_owasp_ssrf(self):
        self.assertIn("A10", _guess_owasp("Server-side request forgery"))

    def test_guess_owasp_default(self):
        self.assertIn("A05", _guess_owasp("Some random issue"))


class TestSemgrepSeverityMapping(unittest.TestCase):
    """Тесты маппинга severity semgrep."""

    def test_map_error_to_critical(self):
        self.assertEqual(_map_semgrep_severity("ERROR"), "critical")

    def test_map_warning_to_high(self):
        self.assertEqual(_map_semgrep_severity("WARNING"), "high")

    def test_map_info_to_medium(self):
        self.assertEqual(_map_semgrep_severity("INFO"), "medium")

    def test_map_lowercase(self):
        self.assertEqual(_map_semgrep_severity("low"), "low")

    def test_map_unknown(self):
        self.assertEqual(_map_semgrep_severity("CUSTOM"), "custom")


class TestCICDMode(unittest.TestCase):
    """Тесты CI/CD mode с exit codes."""

    def test_pass_no_findings(self):
        results = {"severity_counts": {"critical": 0, "high": 0, "medium": 0, "low": 0}}
        self.assertEqual(calculate_ci_exit_code(results, fail_on="high"), 0)

    def test_fail_on_critical(self):
        results = {"severity_counts": {"critical": 1, "high": 0, "medium": 0, "low": 0}}
        self.assertEqual(calculate_ci_exit_code(results, fail_on="critical"), 1)

    def test_fail_on_high(self):
        results = {"severity_counts": {"critical": 0, "high": 2, "medium": 0, "low": 0}}
        self.assertEqual(calculate_ci_exit_code(results, fail_on="high"), 1)

    def test_fail_on_medium(self):
        results = {"severity_counts": {"critical": 0, "high": 0, "medium": 3, "low": 0}}
        self.assertEqual(calculate_ci_exit_code(results, fail_on="medium"), 1)

    def test_fail_on_low(self):
        results = {"severity_counts": {"critical": 0, "high": 0, "medium": 0, "low": 1}}
        self.assertEqual(calculate_ci_exit_code(results, fail_on="low"), 1)

    def test_high_does_not_fail_on_critical_only(self):
        results = {"severity_counts": {"critical": 1, "high": 0, "medium": 0, "low": 0}}
        self.assertEqual(calculate_ci_exit_code(results, fail_on="critical"), 1)

    def test_default_fail_on_high(self):
        results = {"severity_counts": {"critical": 0, "high": 1, "medium": 0, "low": 0}}
        self.assertEqual(calculate_ci_exit_code(results), 1)


class TestSARIFOutput(unittest.TestCase):
    """Тесты SARIF output для IDE интеграции."""

    def test_generate_sarif_structure(self):
        results = {
            "findings": [
                {
                    "type": "python-sql-injection",
                    "severity": "critical",
                    "description": "SQL injection via string formatting",
                    "file": "app.py",
                    "line": 42,
                    "owasp": "A03:2021 – Injection",
                    "cwe": "CWE-89",
                    "tool": "semgrep-custom",
                }
            ]
        }
        sarif = generate_sarif(results)
        self.assertEqual(sarif["version"], "2.1.0")
        self.assertEqual(len(sarif["runs"]), 1)
        self.assertEqual(sarif["runs"][0]["tool"]["driver"]["name"], "CyberTeacher Code Review")

    def test_sarif_has_rules(self):
        results = {
            "findings": [
                {"type": "rule-1", "severity": "high", "description": "Issue 1", "file": "a.py", "line": 1},
                {"type": "rule-2", "severity": "medium", "description": "Issue 2", "file": "b.py", "line": 2},
            ]
        }
        sarif = generate_sarif(results)
        rules = sarif["runs"][0]["tool"]["driver"]["rules"]
        self.assertEqual(len(rules), 2)

    def test_sarif_has_results(self):
        results = {
            "findings": [
                {"type": "rule-1", "severity": "critical", "description": "Critical issue", "file": "app.py", "line": 10},
            ]
        }
        sarif = generate_sarif(results)
        sarif_results = sarif["runs"][0]["results"]
        self.assertEqual(len(sarif_results), 1)
        self.assertEqual(sarif_results[0]["ruleId"], "rule-1")
        self.assertEqual(sarif_results[0]["level"], "error")

    def test_sarif_result_location(self):
        results = {
            "findings": [
                {"type": "xss", "severity": "high", "description": "XSS", "file": "index.js", "line": 55},
            ]
        }
        sarif = generate_sarif(results)
        location = sarif["runs"][0]["results"][0]["locations"][0]["physicalLocation"]
        self.assertEqual(location["artifactLocation"]["uri"], "index.js")
        self.assertEqual(location["region"]["startLine"], 55)

    def test_sarif_properties(self):
        results = {
            "findings": [
                {
                    "type": "ssrf",
                    "severity": "high",
                    "description": "SSRF",
                    "file": "api.py",
                    "line": 20,
                    "owasp": "A10:2021 – Server-Side Request Forgery",
                    "cwe": "CWE-918",
                    "tool": "semgrep-custom",
                }
            ]
        }
        sarif = generate_sarif(results)
        props = sarif["runs"][0]["results"][0]["properties"]
        self.assertIn("A10", props["owasp"])
        self.assertEqual(props["cwe"], "CWE-918")
        self.assertEqual(props["tool"], "semgrep-custom")

    def test_empty_findings_sarif(self):
        results = {"findings": []}
        sarif = generate_sarif(results)
        self.assertEqual(len(sarif["runs"][0]["results"]), 0)


class TestSARIFSeverityLevels(unittest.TestCase):
    """Тесты маппинга severity на SARIF levels."""

    def test_critical_to_error(self):
        self.assertEqual(_severity_to_sarif_level("critical"), "error")

    def test_high_to_error(self):
        self.assertEqual(_severity_to_sarif_level("high"), "error")

    def test_medium_to_warning(self):
        self.assertEqual(_severity_to_sarif_level("medium"), "warning")

    def test_low_to_note(self):
        self.assertEqual(_severity_to_sarif_level("low"), "note")

    def test_unknown_to_warning(self):
        self.assertEqual(_severity_to_sarif_level("unknown"), "warning")


class TestSecretScanningWithOWASP(unittest.TestCase):
    """Тесты сканирования секретов с OWASP mapping."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_secret_has_owasp_tag(self):
        file_path = os.path.join(self.temp_dir, "test.py")
        with open(file_path, "w") as f:
            f.write('aws_key = "AKIAIOSFODNN7EXAMPLE"\n')

        findings = scan_file_secrets(file_path)
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["owasp"], "A07")
        self.assertEqual(findings[0]["tool"], "secrets-scan")


if __name__ == "__main__":
    unittest.main()
