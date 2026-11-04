#!/usr/bin/env python3
"""Check imports: src/ modules and root shims, then run pytest."""
import sys
import os
import subprocess

ROOT = r"M:\Cyber_Teacher\Cyber_Teacher"
sys.path.insert(0, ROOT)
os.chdir(ROOT)

print("=" * 60)
print("1. Импорт ключевых модулей из src/")
print("=" * 60)

src_imports = [
    ("src.core.config", "config"),
    ("src.core.state", "state"),
    ("src.knowledge.knowledge", "knowledge"),
    ("src.handlers.core", "handlers.core"),
    ("src.api.api_server", "api_server"),
    ("src.cli.main", "main"),
]

for mod_path, label in src_imports:
    try:
        mod = __import__(mod_path, fromlist=["*"])
        print(f"  OK  {mod_path}")
    except Exception as e:
        print(f"  FAIL {mod_path}: {type(e).__name__}: {e}")

print()
print("=" * 60)
print("2. Импорт через корневые шимы (config, state, knowledge, handlers.core, api_server, main)")
print("=" * 60)

shim_imports = [
    ("config", "config"),
    ("state", "state"),
    ("knowledge", "knowledge"),
    ("api_server", "api_server"),
    ("main", "main"),
]

for mod_path, label in shim_imports:
    try:
        mod = __import__(mod_path, fromlist=["*"])
        print(f"  OK  {mod_path}")
    except Exception as e:
        print(f"  FAIL {mod_path}: {type(e).__name__}: {e}")

print()
print("=" * 60)
print("3. Запуск pytest tests/")
print("=" * 60)

venv_py = os.path.join(ROOT, ".venv", "Scripts", "python.exe")
if not os.path.exists(venv_py):
    venv_py = os.path.join(ROOT, ".venv", "bin", "python")
if not os.path.exists(venv_py):
    venv_py = sys.executable

out_file = os.path.join(ROOT, "_pytest_out.txt")
cmd = [venv_py, "-m", "pytest", "tests/", "-v", "--tb=short", "-x"]
print(f"Команда: {' '.join(cmd)}")

with open(out_file, "w", encoding="utf-8", errors="replace") as f:
    result = subprocess.run(cmd, cwd=ROOT, stdout=f, stderr=subprocess.STDOUT, text=True)

print(f"Exit code: {result.returncode}")
print(f"Выходные данные записаны в {out_file}")

# Read and show summary
with open(out_file, "r", encoding="utf-8", errors="replace") as f:
    lines = f.readlines()

# Show last 60 lines
print()
print("--- Последние 60 строк вывода pytest ---")
for line in lines[-60:]:
    print(line, end="")

# Count
passed = failed = errors = 0
for line in lines:
    if " passed" in line:
        try:
            passed = int(line.split(" passed")[0].strip().split()[-1])
        except:
            pass
    if " failed" in line:
        try:
            failed = int(line.split(" failed")[0].strip().split()[-1])
        except:
            pass
    if " error" in line:
        try:
            errors = int(line.split(" error")[0].strip().split()[-1])
        except:
            pass

print()
print(f"ИТОГ: {passed} passed, {failed} failed, {errors} errors")