"""FAISS Auto-Reindex Watcher — переиндексация при изменении файлов проекта."""

import os
import sys
import time
import threading
import subprocess
from pathlib import Path
from typing import Set, Optional
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


PROJECT_ROOT = Path(__file__).parent.resolve()
EXCLUDE_DIRS = {
    "__pycache__", ".git", ".mypy_cache", ".ruff_cache", "book_new",
    "venv", "env", "node_modules", "test_reports", "backups",
    "embeddings", ".context", "chroma_db", "cves", "tests",
    ".pytest_cache", "mypy_output.txt", "project_dump.txt",
}
EXTENSIONS = {".py", ".md", ".txt", ".json", ".yaml", ".yml", ".html", ".css", ".js", ".toml", ".ini", ".cfg", ".rst"}


def should_index(file_path: Path) -> bool:
    """Проверить, нужно ли индексировать файл."""
    if file_path.suffix not in EXTENSIONS:
        return False
    rel = file_path.relative_to(PROJECT_ROOT)
    return not any(excl in rel.parts for excl in EXCLUDE_DIRS)


class ReindexHandler(FileSystemEventHandler):
    def __init__(self, debounce_seconds: float = 2.0):
        self.debounce_seconds = debounce_seconds
        self._pending: Set[Path] = set()
        self._timer: Optional[threading.Timer] = None
        self._lock = threading.Lock()
        self._reindexing = False

    def on_any_event(self, event):
        if event.is_directory:
            return
        path = Path(event.src_path)
        if not should_index(path):
            return
        with self._lock:
            self._pending.add(path)
            if self._timer:
                self._timer.cancel()
            self._timer = threading.Timer(self.debounce_seconds, self._run_reindex)
            self._timer.start()

    def _run_reindex(self):
        with self._lock:
            if self._reindexing:
                return
            self._reindexing = True
            pending = list(self._pending)
            self._pending.clear()

        print(f"\n[FAISS Watcher] Detected changes in {len(pending)} files, reindexing...")
        for p in pending[:10]:
            print(f"  - {p.relative_to(PROJECT_ROOT)}")
        if len(pending) > 10:
            print(f"  ... and {len(pending) - 10} more")

        try:
            # Run index_project.py as subprocess
            result = subprocess.run(
                [sys.executable, "index_project.py"],
                cwd=PROJECT_ROOT,
                capture_output=True,
                text=True,
                timeout=300,
            )
            if result.returncode == 0:
                print("[FAISS Watcher] ✅ Reindex complete")
                # Print last few lines of output
                lines = result.stdout.strip().split('\n')
                for line in lines[-5:]:
                    if line.strip():
                        print(f"  {line}")
            else:
                print(f"[FAISS Watcher] ❌ Reindex failed: {result.stderr[:500]}")
        except subprocess.TimeoutExpired:
            print("[FAISS Watcher] ❌ Reindex timeout (5 min)")
        except Exception as e:
            print(f"[FAISS Watcher] ❌ Error: {e}")
        finally:
            with self._lock:
                self._reindexing = False


def run_watcher():
    """Запуск watcher'а в фоновом режиме."""
    print("[FAISS Watcher] Starting...")
    print(f"[FAISS Watcher] Watching: {PROJECT_ROOT}")
    print(f"[FAISS Watcher] Extensions: {', '.join(sorted(EXTENSIONS))}")
    print(f"[FAISS Watcher] Excluded dirs: {', '.join(sorted(EXCLUDE_DIRS))}")
    print("[FAISS Watcher] Press Ctrl+C to stop\n")

    handler = ReindexHandler(debounce_seconds=2.0)
    observer = Observer()
    observer.schedule(handler, str(PROJECT_ROOT), recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[FAISS Watcher] Stopping...")
        observer.stop()
    observer.join()
    print("[FAISS Watcher] Stopped.")


if __name__ == "__main__":
    run_watcher()