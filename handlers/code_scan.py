"""Code scan for secrets in GitHub/GitLab repositories"""

import contextlib
import os
import re
import shutil
import subprocess
import tempfile
from typing import Any

from rich.console import Console

console = Console()

# Patterns for common secrets
SECRET_PATTERNS = [
    # AWS keys
    r"AKIA[0-9A-Z]{16}",
    # Slack token
    r"xox[baprs]-[0-9a-zA-Z-]+",
    # GitHub token
    r"ghp_[0-9a-zA-Z]{36}",
    # OpenAI key
    r"sk-[a-zA-Z0-9]{48}",
    # Generic password assignments
    r"(?:password|passwd|pwd|secret|token|api_key|apikey)\s*[:=]\s*[\"']?([^\s\"'`]+)",
]


def _clone_repo(url: str, branch: str = "main") -> str | None:
    """Clone repo to temp dir, return path or None on failure."""
    if not shutil.which("git"):
        return None
    tmpdir = tempfile.mkdtemp(prefix="cyberteacher_scan_")
    try:
        subprocess.run(
            ["git", "clone", "--depth", "1", "-b", branch, url, tmpdir],
            check=True,
            capture_output=True,
            text=True,
        )
        return tmpdir
    except subprocess.CalledProcessError:
        return None


def _scan_directory(path: str) -> list[tuple[str, int, str, str]]:
    """Scan files for secrets, return list of (file, line, content, match)."""
    matches = []
    for root, _, files in os.walk(path):
        for fname in files:
            fpath = os.path.join(root, fname)
            try:
                with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()
                for i, line in enumerate(lines, start=1):
                    for pat in SECRET_PATTERNS:
                        for m in re.finditer(pat, line, re.IGNORECASE):
                            matches.append(
                                (
                                    os.path.relpath(fpath, path),
                                    i,
                                    line.strip(),
                                    m.group(),
                                )
                            )
            except Exception:
                continue
    return matches


def handle_code_scan(action: str) -> tuple[bool, Any | None, Any | None, bool]:
    """Обработка /scan <repo_url> [branch]"""
    parts = action.split()
    if len(parts) < 2:
        console.print("[cyan]Использование:[/cyan] /scan <repo_url> [branch]")
        console.print("[dim]Пример: /scan https://github.com/user/repo.git main[/dim]")
        return True, None, None, True

    url = parts[1]
    branch = parts[2] if len(parts) > 2 else "main"

    console.print(f"[bold]Клонирую {url} (branch: {branch})...[/bold]")
    tmpdir = _clone_repo(url, branch)
    if tmpdir is None:
        console.print(
            "[red]Не удалось клонировать репозиторий. Убедитесь, что git установлен и репозиторий доступен.[/red]"
        )
        return True, None, None, True

    try:
        console.print("[bold]Сканирую файлы на наличие секретов...[/bold]")
        matches = _scan_directory(tmpdir)
        if matches:
            console.print(
                f"[yellow]⚠️ Найдено {len(matches)} потенциальных секретов:[/yellow]"
            )
            for file, line, content, secret in matches[:50]:
                console.print(
                    f"  [cyan]{file}[/cyan]:{line} | [red]{secret}[/red] (context: {content[:80]})"
                )
            if len(matches) > 50:
                console.print(f"[dim]...и ещё {len(matches) - 50}[/dim]")
        else:
            console.print("[green]✅ Секреты не обнаружены[/green]")
    finally:
        # Cleanup
        with contextlib.suppress(Exception):
            shutil.rmtree(tmpdir)

    return True, None, None, True
