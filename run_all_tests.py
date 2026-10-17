#!/usr/bin/env python3
"""
Universal test runner for CyberTeacher.
"""

import datetime
import importlib
import json
import os
import sys
import time
import traceback
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.resolve()
TESTS_DIR = PROJECT_ROOT / "tests"
OUTPUT_DIR = PROJECT_ROOT / "test_reports"
OUTPUT_MD = OUTPUT_DIR / "test_report.md"
OUTPUT_JSON = OUTPUT_DIR / "test_report.json"

OUTPUT_DIR.mkdir(exist_ok=True)

class CollectingTestResult(unittest.TextTestResult):
    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)
        self.results = []
        self.start_time = None

    def startTest(self, test):
        self.start_time = time.time()
        super().startTest(test)

    def stopTest(self, test):
        duration = time.time() - self.start_time
        super().stopTest(test)

    def addSuccess(self, test):
        self.results.append((str(test), "PASS", "", 0))
        super().addSuccess(test)

    def addFailure(self, test, err):
        msg = self._exc_info_to_string(err, test)
        self.results.append((str(test), "FAIL", msg, 0))
        super().addFailure(test, err)

    def addError(self, test, err):
        msg = self._exc_info_to_string(err, test)
        self.results.append((str(test), "ERROR", msg, 0))
        super().addError(test, err)

    def addSkip(self, test, reason):
        self.results.append((str(test), "SKIP", reason, 0))
        super().addSkip(test, reason)

def discover_test_files():
    if not TESTS_DIR.exists():
        print(f"[!] Tests directory not found: {TESTS_DIR}")
        return []
    return list(TESTS_DIR.rglob("test_*.py"))

def run_test_file(test_file_path):
    rel_path = test_file_path.relative_to(PROJECT_ROOT)
    module_name = str(rel_path).replace(os.sep, ".")[:-3]

    # Default result in case of import error
    default_result = {
        "file": str(rel_path),
        "status": "IMPORT_ERROR",
        "message": "",
        "tests": [],
        "totals": {"total": 0, "failures": 0, "errors": 1, "skipped": 0}
    }

    try:
        module = importlib.import_module(module_name)
    except Exception as e:
        default_result["message"] = traceback.format_exc()
        return default_result

    loader = unittest.defaultTestLoader
    suite = loader.loadTestsFromModule(module)
    stream = sys.stderr
    result = CollectingTestResult(stream, descriptions=True, verbosity=1)
    suite.run(result)

    summary = {
        "file": str(rel_path),
        "status": "OK",
        "message": "",
        "tests": result.results,
        "totals": {
            "total": result.testsRun,
            "failures": len(result.failures),
            "errors": len(result.errors),
            "skipped": len(result.skipped),
        }
    }
    return summary

def run_all_tests():
    print(f"[*] Searching for test files in {TESTS_DIR}")
    test_files = discover_test_files()
    if not test_files:
        print("[!] No test files found.")
        return

    print(f"[*] Found {len(test_files)} test files.")
    all_summaries = []
    grand_total = {"total": 0, "failures": 0, "errors": 0, "skipped": 0}

    for i, tf in enumerate(test_files, 1):
        print(f"[{i}/{len(test_files)}] Running {tf.name} ...")
        summary = run_test_file(tf)
        all_summaries.append(summary)
        for k in grand_total.keys():
            grand_total[k] += summary["totals"][k]

    # Markdown report
    md_lines = []
    md_lines.append("# CyberTeacher Test Report")
    md_lines.append(f"**Date:** {datetime.datetime.now().isoformat()}")
    md_lines.append(f"**Total test files:** {len(test_files)}")
    md_lines.append(f"**Total test cases:** {grand_total['total']}")
    md_lines.append(f"**Failures:** {grand_total['failures']}")
    md_lines.append(f"**Errors:** {grand_total['errors']}")
    md_lines.append(f"**Skipped:** {grand_total['skipped']}")
    md_lines.append("")
    md_lines.append("## Summary per file")
    md_lines.append("| File | Total | Failures | Errors | Skipped | Status |")
    md_lines.append("|------|-------|----------|--------|---------|--------|")
    for summ in all_summaries:
        t = summ["totals"]
        status = summ.get("status", "OK")
        md_lines.append(f"| {summ['file']} | {t['total']} | {t['failures']} | {t['errors']} | {t['skipped']} | {status} |")
    md_lines.append("")
    md_lines.append("## Detailed failures and errors")
    for summ in all_summaries:
        if summ["status"] == "IMPORT_ERROR":
            md_lines.append(f"### IMPORT ERROR: {summ['file']}")
            md_lines.append(f"```\n{summ['message'][:2000]}\n```")
            md_lines.append("")
            continue
        if summ["totals"]["failures"] == 0 and summ["totals"]["errors"] == 0:
            continue
        md_lines.append(f"### {summ['file']}")
        for test_name, status, msg, _ in summ["tests"]:
            if status in ("FAIL", "ERROR"):
                md_lines.append(f"**{status}**: `{test_name}`")
                md_lines.append(f"```\n{msg[:1000]}\n```")
                md_lines.append("")

    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    json_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "grand_total": grand_total,
        "files": all_summaries,
    }
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)

    print(f"\n[✓] Report written to {OUTPUT_MD}")
    print(f"[✓] JSON report written to {OUTPUT_JSON}")
    print("\n=== GRAND TOTAL ===")
    print(f"Tests run: {grand_total['total']}")
    print(f"Failures: {grand_total['failures']}")
    print(f"Errors:   {grand_total['errors']}")
    print(f"Skipped:  {grand_total['skipped']}")
    if grand_total['failures'] == 0 and grand_total['errors'] == 0:
        print("[✓] All tests passed!")
    else:
        print("[!] Some tests failed. See report for details.")

if __name__ == "__main__":
    os.environ["DOTENV_IGNORE"] = "1"
    run_all_tests()