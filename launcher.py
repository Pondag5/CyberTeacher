#!/usr/bin/env python3
"""CyberTeacher Launcher v6.0 — Cyberpunk GUI панель управления проектом."""

import json
import os
import subprocess
import sys
import threading
import tkinter as tk
import urllib.error
import urllib.request
import webbrowser
from datetime import datetime
from pathlib import Path
from tkinter import messagebox, scrolledtext, ttk

# === CONSTANTS ===
PROJECT_DIR = Path(__file__).parent.resolve()
API_HOST = "127.0.0.1"
API_PORT = 8000
PWA_URL = f"http://localhost:{API_PORT}"
PGADMIN_URL = "http://localhost:5050"
MCP_SCRIPT = str(PROJECT_DIR / "mcp_server_faiss.py")

C = {
    "bg": "#0a0e17",
    "bg2": "#111827",
    "bg3": "#1a2332",
    "bg4": "#0d1117",
    "green": "#00ff88",
    "cyan": "#00d4ff",
    "magenta": "#ff00ff",
    "yellow": "#ffd700",
    "red": "#ff4444",
    "text": "#e2e8f0",
    "text2": "#94a3b8",
    "text3": "#64748b",
    "border": "#1e293b",
    "db": "#0d47a1",
    "db_h": "#1565c0",
    "app": "#1b5e20",
    "app_h": "#2e7d32",
    "dkr": "#e65100",
    "dkr_h": "#f57c00",
    "pwa": "#4a148c",
    "pwa_h": "#7b1fa2",
    "tool": "#b8860b",
    "tool_h": "#daa520",
    "mcp": "#00695c",
    "mcp_h": "#00897b",
    "svc": "#37474f",
    "svc_h": "#546e7a",
}


class CyberLauncher:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("CyberTeacher Launcher v6.0")
        self.root.geometry("1280x780")
        self.root.minsize(960, 660)
        self.root.configure(bg=C["bg"])
        self._setup_icon()
        self._processes: dict[str, subprocess.Popen] = {}
        self._build_ui()
        self._update_poller()

    # ---- ICON ----
    def _setup_icon(self):
        p = PROJECT_DIR / "static" / "icon-192.png"
        if p.exists():
            try:
                self.root.iconphoto(True, tk.PhotoImage(file=str(p)))
            except (tk.TclError, OSError):
                pass

    # ---- BUILD UI ----
    def _build_ui(self):
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=0)
        self.root.rowconfigure(1, weight=1)

        # ── Header ──
        self._build_header()

        # ── Main: left (output) + right (buttons) ──
        main = tk.Frame(self.root, bg=C["bg"])
        main.grid(row=1, column=0, sticky="nsew")
        main.columnconfigure(0, weight=2)
        main.columnconfigure(1, weight=3)
        main.rowconfigure(0, weight=1)

        self._build_output(main)
        self._build_right_panel(main)

    def _load_env(self):
        """Load current provider/model from .env."""
        self._env_provider = "ollama"
        self._env_model = "?"
        env_path = PROJECT_DIR / ".env"
        if env_path.exists():
            for line in env_path.read_text(encoding="utf-8").splitlines():
                if "=" in line and not line.strip().startswith("#"):
                    k, _, v = line.partition("=")
                    k = k.strip()
                    v = v.strip()
                    if k == "LLM_PROVIDER":
                        self._env_provider = v.lower()
                    elif k in (
                        "OLLAMA_MODEL",
                        "LMSTUDIO_MODEL",
                        "GROQ_MODEL",
                        "OPENROUTER_MODEL",
                    ):
                        self._env_model = v
        if self._env_model == "?":
            model_map = {
                "ollama": "qwen2.5:7b",
                "lmstudio": "local-model",
                "groq": "mixtral-8x7b-32768",
                "openrouter": "mistralai/mixtral-8x7b-instruct",
                "huggingface": "mistralai/Mistral-7B-Instruct-v0.2",
                "mock": "mock-llm",
            }
            self._env_model = model_map.get(self._env_provider, "?")

    def _build_header(self):
        h = tk.Frame(self.root, bg=C["bg2"], height=52)
        h.grid(row=0, column=0, sticky="ew", padx=0, pady=(0, 2))
        h.columnconfigure(3, weight=1)

        tk.Label(
            h,
            text="CYBERTEACHER",
            font=("Consolas", 16, "bold"),
            fg=C["cyan"],
            bg=C["bg2"],
        ).grid(row=0, column=0, padx=(16, 4), pady=8)
        tk.Label(
            h, text="LAUNCHER v6.0", font=("Consolas", 10), fg=C["text3"], bg=C["bg2"]
        ).grid(row=0, column=1, sticky="w", pady=8)
        self._load_env()
        self._provider_indicator = tk.Label(
            h,
            text=f"⚡ {self._env_provider.upper()} / {self._env_model}",
            font=("Consolas", 8),
            fg=C["yellow"],
            bg=C["bg2"],
        )
        self._provider_indicator.grid(row=0, column=2, padx=(4, 4), pady=8)
        tk.Label(
            h,
            text=datetime.now().strftime("%Y-%m-%d"),
            font=("Consolas", 8),
            fg=C["text3"],
            bg=C["bg2"],
        ).grid(row=0, column=4, padx=16, pady=8)

    def _build_output(self, parent):
        f = tk.Frame(parent, bg=C["bg2"])
        f.grid(row=0, column=0, sticky="nsew", padx=(8, 4), pady=4)
        f.rowconfigure(0, weight=0)
        f.rowconfigure(1, weight=1)
        f.columnconfigure(0, weight=1)

        tk.Label(
            f,
            text="⬡ CONSOLE OUTPUT",
            font=("Consolas", 9, "bold"),
            fg=C["text2"],
            bg=C["bg2"],
        ).grid(row=0, column=0, sticky="w", padx=8, pady=(6, 0))

        self.output = scrolledtext.ScrolledText(
            f,
            font=("Consolas", 9),
            bg=C["bg4"],
            fg=C["green"],
            insertbackground=C["green"],
            relief=tk.FLAT,
            state=tk.DISABLED,
        )
        self.output.grid(row=1, column=0, sticky="nsew", padx=6, pady=6)
        self.output.tag_config("ok", foreground=C["green"])
        self.output.tag_config("err", foreground=C["red"])
        self.output.tag_config("info", foreground=C["cyan"])
        self.output.tag_config("warn", foreground=C["yellow"])
        self.output.tag_config("dim", foreground=C["text3"])
        self.output.tag_config("bold", foreground=C["magenta"])

        # Clear button
        btn_clr = tk.Button(
            f,
            text="✕ CLEAR",
            font=("Consolas", 7),
            fg=C["text3"],
            bg=C["bg3"],
            relief=tk.FLAT,
            cursor="hand2",
            command=self._clear_output,
        )
        btn_clr.place(relx=1.0, x=-8, y=4, anchor="ne")

    def _clear_output(self):
        self.output.config(state=tk.NORMAL)
        self.output.delete("1.0", tk.END)
        self.output.config(state=tk.DISABLED)

    def _build_right_panel(self, parent):
        f = tk.Frame(parent, bg=C["bg"])
        f.grid(row=0, column=1, sticky="nsew", padx=(4, 8), pady=4)
        f.rowconfigure(0, weight=0)  # indicators
        f.rowconfigure(1, weight=1)  # buttons grid
        f.columnconfigure(0, weight=1)

        # ── Status indicators ──
        sf = tk.Frame(f, bg=C["bg2"], height=34)
        sf.grid(row=0, column=0, sticky="ew", pady=(0, 6))
        sf.columnconfigure(4, weight=1)

        self.indicators: dict[str, tk.Label] = {}
        labels = [("API", "api"), ("Postgres", "pg"), ("Docker", "dkr"), ("MCP", "mcp")]
        for i, (label, key) in enumerate(labels):
            dot = tk.Label(
                sf, text="●", font=("Consolas", 10), fg=C["text3"], bg=C["bg2"]
            )
            dot.grid(row=0, column=i * 2, padx=(12, 2))
            lbl = tk.Label(
                sf, text=label, font=("Consolas", 8), fg=C["text2"], bg=C["bg2"]
            )
            lbl.grid(row=0, column=i * 2 + 1, padx=(0, 4))
            self.indicators[key] = dot

        # ── Buttons grid (4 columns, N rows) ──
        bf = tk.Frame(f, bg=C["bg"])
        bf.grid(row=1, column=0, sticky="nsew")
        for i in range(4):
            bf.columnconfigure(i, weight=1)
        for i in range(2):
            bf.rowconfigure(i, weight=1)

        sections = [
            # (title, base, hover, col, row, btns)
            (
                "🖥 SERVER",
                C["app"],
                C["app_h"],
                0,
                0,
                [
                    ("Start API", self._cmd_start_api),
                    ("Stop API", self._cmd_stop_api),
                    ("Restart API", self._cmd_restart_api),
                    ("Start CLI", self._cmd_start_cli),
                    ("Start MCP", self._cmd_start_mcp),
                    ("Stop MCP", self._cmd_stop_mcp),
                ],
            ),
            (
                "🗄 DATABASE",
                C["db"],
                C["db_h"],
                1,
                0,
                [
                    ("Start PostgreSQL", self._cmd_start_postgres),
                    ("Stop PostgreSQL", self._cmd_stop_postgres),
                    ("DB Status", self._cmd_pg_status),
                    ("Run Migrations", self._cmd_migrations),
                    ("Open pgAdmin", self._cmd_open_pgadmin),
                    ("SQLite Info", self._cmd_sqlite_info),
                ],
            ),
            (
                "🐳 DOCKER",
                C["dkr"],
                C["dkr_h"],
                2,
                0,
                [
                    ("Start Labs", self._cmd_start_labs),
                    ("Stop Labs", self._cmd_stop_labs),
                    ("Lab Status", self._cmd_lab_status),
                    ("Prune Docker", self._cmd_docker_prune),
                    ("Docker Info", self._cmd_docker_info),
                ],
            ),
            (
                "🔗 PWA LINKS",
                C["pwa"],
                C["pwa_h"],
                3,
                0,
                [
                    ("🌐 Open PWA", self._cmd_open_pwa),
                    ("📊 Dashboard", lambda: self._open_tab("dashboard")),
                    ("🎯 CTF / Flags", lambda: self._open_tab("ctf")),
                    ("🧪 Labs", lambda: self._open_tab("labs")),
                    ("📋 Writeups", lambda: self._open_tab("writeups")),
                    ("🛡 Recon", lambda: self._open_tab("recon")),
                ],
            ),
            (
                "🛠 TOOLS",
                C["tool"],
                C["tool_h"],
                0,
                1,
                [
                    ("Run Tests", self._cmd_run_tests),
                    ("Reindex KB (FAISS)", self._cmd_reindex_kb),
                    ("KB Status", self._cmd_kb_status),
                    ("View Logs", self._cmd_view_logs),
                    ("System Info", self._cmd_system_info),
                    ("Env Config", self._cmd_env_config),
                    ("⚙ Provider Settings", self._open_provider_settings),
                ],
            ),
            (
                "⏳ SERVICES",
                C["svc"],
                C["svc_h"],
                1,
                1,
                [
                    ("FAISS MCP Test", self._cmd_mcp_test),
                    ("Check Dependencies", self._cmd_deps),
                    ("Memory Cleanup", self._cmd_mem_cleanup),
                    ("Clear Output", self._clear_output),
                ],
            ),
        ]

        for title, base, hover, col, row, btns in sections:
            self._add_section(bf, title, base, hover, col, row, btns)

        self._log("Launcher v6.0 ready.", "info")

    def _add_section(self, parent, title, base, hover, col, row, btns):
        f = tk.LabelFrame(
            parent,
            text=title,
            font=("Consolas", 9, "bold"),
            fg=C["cyan"],
            bg=C["bg2"],
            borderwidth=1,
            relief=tk.GROOVE,
            padx=6,
            pady=4,
        )
        f.grid(
            row=row,
            column=col,
            sticky="nsew",
            padx=3,
            pady=3,
        )
        for text, cmd in btns:
            self._cyber_btn(f, text, cmd, base, hover).pack(fill=tk.X, pady=1)

    def _cyber_btn(self, parent, text, command, base, hover) -> tk.Button:
        btn = tk.Button(
            parent,
            text=text,
            font=("Consolas", 8),
            anchor="w",
            fg=C["text"],
            bg=base,
            activebackground=hover,
            activeforeground=C["text"],
            relief=tk.FLAT,
            bd=1,
            cursor="hand2",
            padx=8,
            pady=4,
        )

        def on_enter(_):
            btn.config(bg=hover)

        def on_leave(_):
            btn.config(bg=base)

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        btn.config(command=lambda: self._run_action(text, command))
        return btn

    # ── LOGGING ──
    def _log(self, text, tag=""):
        self.output.config(state=tk.NORMAL)
        ts = datetime.now().strftime("%H:%M:%S")
        self.output.insert(tk.END, f"[{ts}] {text}\n", tag or "")
        self.output.see(tk.END)
        self.output.config(state=tk.DISABLED)

    def _run_action(self, label, func):
        self._log(f"── {label} ──", "info")

        def worker():
            try:
                func()
            except Exception as e:
                self.root.after(0, lambda err=e: self._log(f"Error: {err}", "err"))

        threading.Thread(target=worker, daemon=True).start()

    def _open_tab(self, tab_id):
        webbrowser.open(f"{PWA_URL}/?tab={tab_id}")
        self._log(f"PWA → /?tab={tab_id}", "ok")

    # ── POLLER ──
    def _update_poller(self):
        statuses = [
            ("api", self._check_api),
            ("pg", self._check_postgres),
            ("dkr", self._check_docker),
            ("mcp", self._check_mcp),
        ]
        for key, fn in statuses:
            ok = fn()
            self.indicators[key].config(fg=C["green"] if ok else C["red"])
        self._refresh_provider_indicator()
        self.root.after(5000, self._update_poller)

    def _refresh_provider_indicator(self):
        """Refresh provider/model display from .env file."""
        self._load_env()
        self._provider_indicator.config(
            text=f"⚡ {self._env_provider.upper()} / {self._env_model}"
        )

    # ── CHECKS ──
    def _check_api(self):
        try:
            req = urllib.request.Request(
                f"http://{API_HOST}:{API_PORT}/api/health", method="GET"
            )
            with urllib.request.urlopen(req, timeout=2) as r:
                return r.status == 200
        except (OSError, ValueError):
            return False

    def _check_postgres(self):
        try:
            r = subprocess.run(
                [
                    "docker",
                    "compose",
                    "-f",
                    str(PROJECT_DIR / "docker-compose.yml"),
                    "ps",
                    "postgres",
                ],
                capture_output=True,
                text=True,
                timeout=10,
                creationflags=subprocess.CREATE_NO_WINDOW
                if sys.platform == "win32"
                else 0,
            )
            return "Up" in r.stdout
        except (subprocess.TimeoutExpired, OSError):
            return False

    def _check_docker(self):
        try:
            r = subprocess.run(
                ["docker", "info"],
                capture_output=True,
                text=True,
                timeout=5,
                creationflags=subprocess.CREATE_NO_WINDOW
                if sys.platform == "win32"
                else 0,
            )
            return r.returncode == 0
        except (subprocess.TimeoutExpired, OSError):
            return False

    def _check_mcp(self):
        proc = self._processes.get("mcp")
        return proc is not None and proc.poll() is None

    # ── COMMANDS ──
    def _run_cmd(self, cmd, success_msg, cwd=None):
        try:
            r = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,
                cwd=cwd or str(PROJECT_DIR),
                creationflags=subprocess.CREATE_NO_WINDOW
                if sys.platform == "win32"
                else 0,
            )
            if r.stdout.strip():
                for line in r.stdout.strip().splitlines():
                    self._log(line, "ok")
            if r.stderr.strip():
                for line in r.stderr.strip().splitlines():
                    self._log(line, "warn" if "warn" in line.lower() else "err")
            if r.returncode == 0:
                self._log(success_msg, "ok")
            else:
                self._log(f"Exit code: {r.returncode}", "err")
        except subprocess.TimeoutExpired:
            self._log("Timeout (60s)", "err")
        except FileNotFoundError:
            self._log(f"Command not found: {cmd[0]}", "err")
        except Exception as e:
            self._log(f"Error: {e}", "err")

    def _run_dc(self, args, msg):
        self._run_cmd(
            [
                "docker",
                "compose",
                "-f",
                str(PROJECT_DIR / "docker-compose.yml"),
                *args.split(),
            ],
            msg,
        )

    # Server
    def _cmd_start_api(self):
        if self._check_api():
            self._log("API already running.", "warn")
            return
        cmd = [
            sys.executable,
            "-m",
            "uvicorn",
            "api_server:app",
            "--host",
            API_HOST,
            "--port",
            str(API_PORT),
            "--log-level",
            "info",
        ]
        try:
            kw = (
                {"creationflags": subprocess.CREATE_NEW_CONSOLE}
                if sys.platform == "win32"
                else {}
            )
            self._processes["api"] = subprocess.Popen(cmd, cwd=str(PROJECT_DIR), **kw)
            self._log(f"API → http://{API_HOST}:{API_PORT}", "ok")
        except Exception as e:
            self._log(f"API start failed: {e}", "err")

    def _cmd_stop_api(self):
        proc = self._processes.pop("api", None)
        if proc and proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(5)
            except subprocess.TimeoutExpired:
                proc.kill()
            self._log("API stopped.", "ok")
        else:
            self._log("API process not tracked. Kill manually.", "warn")

    def _cmd_restart_api(self):
        self._cmd_stop_api()
        self.root.after(1000, self._cmd_start_api)

    def _cmd_start_cli(self):
        cmd = [sys.executable, "main.py"]
        try:
            kw = (
                {"creationflags": subprocess.CREATE_NEW_CONSOLE}
                if sys.platform == "win32"
                else {}
            )
            subprocess.Popen(cmd, cwd=str(PROJECT_DIR), **kw)
            self._log("CLI launched in new terminal.", "ok")
        except Exception as e:
            self._log(f"CLI launch failed: {e}", "err")

    def _cmd_start_mcp(self):
        if self._check_mcp():
            self._log("MCP already running.", "warn")
            return
        cmd = [sys.executable, MCP_SCRIPT]
        try:
            kw = (
                {"creationflags": subprocess.CREATE_NEW_CONSOLE}
                if sys.platform == "win32"
                else {}
            )
            self._processes["mcp"] = subprocess.Popen(cmd, cwd=str(PROJECT_DIR), **kw)
            self._log("MCP server started.", "ok")
        except Exception as e:
            self._log(f"MCP start failed: {e}", "err")

    def _cmd_stop_mcp(self):
        proc = self._processes.pop("mcp", None)
        if proc and proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(5)
            except subprocess.TimeoutExpired:
                proc.kill()
            self._log("MCP stopped.", "ok")
        else:
            self._log("MCP process not tracked.", "warn")

    # Database
    def _cmd_start_postgres(self):
        self._run_dc("up -d postgres", "PostgreSQL started.")

    def _cmd_stop_postgres(self):
        self._run_dc("down", "PostgreSQL stopped.")

    def _cmd_pg_status(self):
        ok = self._check_postgres()
        self._log(
            f"PostgreSQL: {'RUNNING' if ok else 'STOPPED'}", "ok" if ok else "warn"
        )

    def _cmd_migrations(self):
        self._run_cmd(
            [sys.executable, "-m", "alembic", "upgrade", "head"], "Migrations applied."
        )

    def _cmd_open_pgadmin(self):
        webbrowser.open(PGADMIN_URL)
        self._log(f"pgAdmin: {PGADMIN_URL}", "ok")

    def _cmd_sqlite_info(self):
        db = PROJECT_DIR / "memory" / "cyberteacher.db"
        if db.exists():
            kb = db.stat().st_size / 1024
            self._log(f"SQLite DB: {kb:.1f} KB", "ok")
        else:
            self._log("SQLite DB not found.", "warn")

    # Docker
    def _cmd_start_labs(self):
        self._run_dc("up -d", "Docker labs started.")

    def _cmd_stop_labs(self):
        self._run_dc("down", "Docker labs stopped.")

    def _cmd_lab_status(self):
        self._run_cmd(
            ["docker", "ps", "--format", "table {{.Names}}\t{{.Status}}\t{{.Ports}}"],
            "Status fetched.",
        )

    def _cmd_docker_prune(self):
        self._run_cmd(
            ["docker", "container", "prune", "-f"], "Stopped containers pruned."
        )

    def _cmd_docker_info(self):
        self._run_cmd(["docker", "info", "--format", "{{json .}}"], "")
        self._log("Docker info fetched (see output above).", "dim")

    # Tools
    def _cmd_run_tests(self):
        self._run_cmd(
            [sys.executable, "-m", "pytest", "tests/", "-x", "--tb=short", "-q"],
            "Tests complete.",
        )

    def _cmd_reindex_kb(self):
        self._log("Reindexing FAISS...", "info")
        self._run_cmd([sys.executable, "index_project.py"], "FAISS reindex complete.")

    def _cmd_kb_status(self):
        self._run_cmd(
            [
                sys.executable,
                "-c",
                """
print('{"status": "removed"}')
""",
            ],
            "KB status fetched.",
        )

    def _cmd_view_logs(self):
        log = PROJECT_DIR / "cyberteacher.log"
        if not log.exists():
            self._log("No log file.", "warn")
            return
        try:
            lines = log.read_text(encoding="utf-8").splitlines()
            last = lines[-60:] if len(lines) > 60 else lines
            self._log(f"─── Last {len(last)} lines ───", "info")
            for line in last:
                tag = (
                    "err"
                    if "ERROR" in line
                    else ("warn" if "WARNING" in line else "dim")
                )
                self._log(line, tag)
        except Exception as e:
            self._log(f"Log read error: {e}", "err")

    def _cmd_system_info(self):
        self._log("=== SYSTEM INFO ===", "bold")
        self._log(f"Python: {sys.version.split()[0]}", "ok")
        self._log(f"Platform: {sys.platform}", "ok")
        self._log(f"Project: {PROJECT_DIR}", "ok")
        self._log(
            f"Docker: {'OK' if self._check_docker() else 'N/A'}",
            "ok" if self._check_docker() else "err",
        )
        self._log(
            f"API: {'OK' if self._check_api() else 'N/A'}",
            "ok" if self._check_api() else "err",
        )
        self._log(
            f"MCP: {'OK' if self._check_mcp() else 'N/A'}",
            "ok" if self._check_mcp() else "err",
        )
        db = PROJECT_DIR / "memory" / "cyberteacher.db"
        if db.exists():
            self._log(f"SQLite: {db.stat().st_size / 1024:.1f} KB", "ok")
        mem = PROJECT_DIR / "memory"
        if mem.exists():
            mem_kb = sum(f.stat().st_size for f in mem.rglob("*") if f.is_file()) / 1024
            self._log(f"Memory dir: {mem_kb:.1f} KB", "dim")

    def _cmd_env_config(self):
        env = PROJECT_DIR / ".env"
        cfg = PROJECT_DIR / "config.py"
        self._log("=== ENV / CONFIG ===", "bold")
        if env.exists():
            for line in env.read_text(encoding="utf-8").splitlines():
                if line.strip() and not line.startswith("#"):
                    k, _, v = line.partition("=")
                    val = v[:30] + "..." if len(v) > 30 else v
                    self._log(f"  {k.strip()}={val}", "dim")
        else:
            self._log("  No .env file", "warn")
        if cfg.exists():
            for line in cfg.read_text(encoding="utf-8").splitlines():
                if "LLM_PROVIDER" in line or "PROVIDER" in line or "FALLBACK" in line:
                    self._log(f"  {line.strip()}", "dim")

    def _cmd_mcp_test(self):
        self._run_cmd(
            [
                sys.executable,
                "-c",
                """
import urllib.request, json
try:
    req = urllib.request.Request("http://localhost:8000/api/health")
    with urllib.request.urlopen(req, timeout=3) as r:
        print(f"FAISS MCP health: {r.status}")
except Exception as e:
    print(f"FAISS MCP not reachable: {e}")
""",
            ],
            "MCP test done.",
        )

    def _cmd_deps(self):
        self._log("=== DEPENDENCIES ===", "bold")
        for mod in [
            "fastapi",
            "uvicorn",
            "rich",
            "chromadb",
            "sqlalchemy",
            "langchain",
            "faiss",
            "pydantic",
            "requests",
            "yaml",
        ]:
            try:
                __import__(mod.replace("-", "_"))
                self._log(f"  {mod}: OK", "ok")
            except ImportError:
                self._log(f"  {mod}: MISSING", "err")

    def _cmd_mem_cleanup(self):
        import shutil

        mem = PROJECT_DIR / "memory"
        count = 0
        for f in mem.rglob("*"):
            if f.is_file() and f.suffix in (".json", ".pickle", ".db"):
                try:
                    if f.stat().st_mtime < (datetime.now().timestamp() - 86400 * 7):
                        f.unlink()
                        count += 1
                except (OSError, IOError):
                    pass
        self._log(f"Cleaned {count} stale files from memory/", "ok")

    def _cmd_open_pwa(self):
        webbrowser.open(PWA_URL)
        self._log(f"PWA opened: {PWA_URL}", "ok")

    # ── PROVIDER SETTINGS ──
    def _open_provider_settings(self):
        win = tk.Toplevel(self.root)
        win.title("Provider Settings")
        win.geometry("680x780")
        win.minsize(580, 640)
        win.configure(bg=C["bg"])
        win.transient(self.root)
        win.grab_set()

        f = tk.Frame(win, bg=C["bg"], padx=16, pady=12)
        f.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            f,
            text="⚙ PROVIDER CONFIGURATION",
            font=("Consolas", 13, "bold"),
            fg=C["cyan"],
            bg=C["bg"],
        ).pack(anchor="w", pady=(0, 6))

        # Load current env values
        env_path = PROJECT_DIR / ".env"
        env_vars = {}
        if env_path.exists():
            for line in env_path.read_text(encoding="utf-8").splitlines():
                if "=" in line and not line.strip().startswith("#"):
                    k, _, v = line.partition("=")
                    env_vars[k.strip()] = v.strip()

        current_provider = env_vars.get("LLM_PROVIDER", "ollama")

        # ── Active provider selector ──
        prov_frame = tk.Frame(f, bg=C["bg2"], pady=6)
        prov_frame.pack(fill=tk.X, pady=(0, 8))
        tk.Label(
            prov_frame,
            text="Активный провайдер:",
            font=("Consolas", 8, "bold"),
            fg=C["text2"],
            bg=C["bg2"],
        ).pack(side=tk.LEFT, padx=(8, 8))

        provider_btns: dict[str, tk.Button] = {}
        provider_names = [
            ("ollama", "Ollama"),
            ("lmstudio", "LM Studio"),
            ("groq", "Groq"),
            ("openrouter", "OpenRouter"),
            ("huggingface", "HF"),
            ("mock", "Mock"),
        ]

        def set_active_provider(pid):
            for pid2, btn in provider_btns.items():
                btn.config(
                    bg=C["app"] if pid2 == pid else C["bg3"],
                    fg=C["text"] if pid2 == pid else C["text2"],
                )
            provider_active.set(pid)

        provider_active = tk.StringVar(value=current_provider)
        for pid, plabel in provider_names:
            is_active = pid == current_provider
            btn = tk.Button(
                prov_frame,
                text=plabel,
                font=("Consolas", 8, "bold"),
                fg=C["text"] if is_active else C["text2"],
                bg=C["app"] if is_active else C["bg3"],
                activebackground=C["app_h"],
                activeforeground=C["text"],
                relief=tk.FLAT,
                cursor="hand2",
                padx=10,
                pady=2,
                command=lambda p=pid: set_active_provider(p),
            )
            btn.pack(side=tk.LEFT, padx=2)
            provider_btns[pid] = btn

        # ── Scrollable provider configs + model list ──
        canvas = tk.Canvas(f, bg=C["bg"], highlightthickness=0)
        scroll = ttk.Scrollbar(f, orient="vertical", command=canvas.yview)
        scroll_inner = tk.Frame(canvas, bg=C["bg"])
        scroll_inner.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scroll_inner, anchor="nw")
        canvas.configure(yscrollcommand=scroll.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        def _on_mousewheel(e):
            canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Data structures
        entries: dict[str, tk.Entry] = {}
        status_labels: dict[str, tk.Label] = {}
        model_labels: dict[str, tk.Label] = {}
        model_lists: dict[str, list[str]] = {}  # fetched models per provider
        select_btns: dict[str, tk.Button] = {}
        selected_models: dict[str, tk.StringVar] = {}

        providers_config = [
            (
                "ollama",
                "Ollama (локальные модели)",
                [
                    ("Base URL", "OLLAMA_BASE_URL", "http://localhost:11434"),
                ],
                ["OLLAMA_MODEL", "qwen2.5:7b"],
            ),
            (
                "lmstudio",
                "LM Studio (OpenAI-совместимый API)",
                [
                    ("Base URL", "LMSTUDIO_BASE_URL", "http://localhost:1234/v1"),
                ],
                ["LMSTUDIO_MODEL", "local-model"],
            ),
            (
                "groq",
                "Groq Cloud (бесплатно, быстро)",
                [
                    ("API Key", "GROQ_API_KEY", "*"),
                ],
                ["GROQ_MODEL", "mixtral-8x7b-32768"],
            ),
            (
                "openrouter",
                "OpenRouter (100+ моделей)",
                [
                    ("API Key", "OPENROUTER_API_KEY", "*"),
                    ("Base URL", "OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
                ],
                ["OPENROUTER_MODEL", "mistralai/mixtral-8x7b-instruct"],
            ),
            (
                "huggingface",
                "HuggingFace Inference API",
                [
                    ("API Key", "HUGGINGFACE_API_KEY", "*"),
                ],
                ["HUGGINGFACE_MODEL", "mistralai/Mistral-7B-Instruct-v0.2"],
            ),
        ]

        for provider_id, provider_label, fields, model_info in providers_config:
            model_env_key, model_default = model_info
            sf = tk.LabelFrame(
                scroll_inner,
                text=f"  {provider_label}  ",
                font=("Consolas", 10, "bold"),
                fg=C["yellow"],
                bg=C["bg2"],
                borderwidth=1,
                relief=tk.GROOVE,
                padx=10,
                pady=6,
            )
            sf.pack(fill=tk.X, pady=(3, 6))

            # API key / URL fields
            for field_label, env_key, default_val in fields:
                row = tk.Frame(sf, bg=C["bg2"])
                row.pack(fill=tk.X, pady=2)
                tk.Label(
                    row,
                    text=field_label,
                    font=("Consolas", 8),
                    fg=C["text2"],
                    bg=C["bg2"],
                    width=12,
                    anchor="w",
                ).pack(side=tk.LEFT)
                is_pw = env_key.endswith("_API_KEY") or env_key.endswith("_TOKEN")
                show = "*" if is_pw else ""
                ent = tk.Entry(
                    row,
                    font=("Consolas", 8),
                    bg=C["bg4"],
                    fg=C["green"],
                    insertbackground=C["green"],
                    relief=tk.FLAT,
                    bd=2,
                    highlightthickness=1,
                    highlightbackground=C["border"],
                    show=show,
                )
                ent.pack(side=tk.LEFT, padx=(4, 4), fill=tk.X, expand=True)
                existing = env_vars.get(env_key, "")
                if not existing and default_val != "*":
                    existing = default_val
                ent.insert(0, existing)
                entries[env_key] = ent

            # Model selector row
            model_row = tk.Frame(sf, bg=C["bg2"])
            model_row.pack(fill=tk.X, pady=(4, 2))

            cur_model = env_vars.get(model_env_key, model_default)
            selected_models[provider_id] = tk.StringVar(value=cur_model)

            tk.Label(
                model_row,
                text="Модель:",
                font=("Consolas", 8),
                fg=C["text2"],
                bg=C["bg2"],
                width=12,
                anchor="w",
            ).pack(side=tk.LEFT)

            model_lbl = tk.Label(
                model_row,
                text=cur_model,
                font=("Consolas", 8, "bold"),
                fg=C["green"],
                bg=C["bg2"],
                anchor="w",
            )
            model_lbl.pack(side=tk.LEFT, padx=(2, 8), fill=tk.X, expand=True)
            model_labels[provider_id] = model_lbl

            # Test + Select Model buttons
            btn_row = tk.Frame(sf, bg=C["bg2"])
            btn_row.pack(fill=tk.X, pady=(0, 2))

            test_btn = tk.Button(
                btn_row,
                text="🔌 Test",
                font=("Consolas", 7),
                fg=C["text"],
                bg=C["bg3"],
                activebackground=C["app_h"],
                relief=tk.FLAT,
                cursor="hand2",
                padx=8,
            )
            test_btn.pack(side=tk.LEFT, padx=(0, 4))

            status_lbl = tk.Label(
                btn_row, text="", font=("Consolas", 7), fg=C["text3"], bg=C["bg2"]
            )
            status_lbl.pack(side=tk.LEFT, padx=(0, 8))
            status_labels[provider_id] = status_lbl

            select_btn = tk.Button(
                btn_row,
                text="📋 Select Model",
                font=("Consolas", 7),
                fg=C["text"],
                bg=C["app"],
                activebackground=C["app_h"],
                relief=tk.FLAT,
                cursor="hand2",
                padx=8,
                state=tk.DISABLED,
            )
            select_btn.pack(side=tk.LEFT)
            select_btns[provider_id] = select_btn

            def make_tester(pid, fields_list):
                def test():
                    self._test_and_fetch_models(
                        pid,
                        fields_list,
                        entries,
                        status_labels,
                        model_lists,
                        select_btns,
                    )

                return test

            test_btn.config(command=make_tester(provider_id, fields))

            def make_selector(pid):
                def select():
                    self._open_model_selector(
                        pid,
                        model_lists,
                        model_labels,
                        selected_models,
                        entries,
                        model_env_key,
                    )

                return select

            select_btn.config(command=make_selector(provider_id))

        # ── Global settings: Temperature + Max Tokens ──
        glob_frame = tk.LabelFrame(
            scroll_inner,
            text="  Global Settings  ",
            font=("Consolas", 10, "bold"),
            fg=C["cyan"],
            bg=C["bg2"],
            borderwidth=1,
            relief=tk.GROOVE,
            padx=10,
            pady=6,
        )
        glob_frame.pack(fill=tk.X, pady=(4, 0))

        # Temperature
        temp_row = tk.Frame(glob_frame, bg=C["bg2"])
        temp_row.pack(fill=tk.X, pady=2)
        tk.Label(
            temp_row,
            text="Temperature:",
            font=("Consolas", 8),
            fg=C["text2"],
            bg=C["bg2"],
            width=14,
            anchor="w",
        ).pack(side=tk.LEFT)
        temp_val = env_vars.get("MODEL_TEMPERATURE", env_vars.get("TEMPERATURE", "0.7"))
        temp_entry = tk.Entry(
            temp_row,
            font=("Consolas", 8),
            bg=C["bg4"],
            fg=C["green"],
            insertbackground=C["green"],
            relief=tk.FLAT,
            bd=2,
            highlightthickness=1,
            highlightbackground=C["border"],
            width=8,
        )
        temp_entry.insert(0, temp_val)
        temp_entry.pack(side=tk.LEFT, padx=(4, 8))
        entries["TEMPERATURE"] = temp_entry

        tk.Label(
            temp_row,
            text="(0.0 — 2.0)",
            font=("Consolas", 7),
            fg=C["text3"],
            bg=C["bg2"],
        ).pack(side=tk.LEFT)

        # Max Tokens
        tok_row = tk.Frame(glob_frame, bg=C["bg2"])
        tok_row.pack(fill=tk.X, pady=2)
        tk.Label(
            tok_row,
            text="Max Tokens:",
            font=("Consolas", 8),
            fg=C["text2"],
            bg=C["bg2"],
            width=14,
            anchor="w",
        ).pack(side=tk.LEFT)
        tok_val = env_vars.get("MAX_TOKENS", "2048")
        tok_entry = tk.Entry(
            tok_row,
            font=("Consolas", 8),
            bg=C["bg4"],
            fg=C["green"],
            insertbackground=C["green"],
            relief=tk.FLAT,
            bd=2,
            highlightthickness=1,
            highlightbackground=C["border"],
            width=8,
        )
        tok_entry.insert(0, tok_val)
        tok_entry.pack(side=tk.LEFT, padx=(4, 8))
        entries["MAX_TOKENS"] = tok_entry

        # ── Bottom buttons ──
        btm = tk.Frame(f, bg=C["bg"])
        btm.pack(fill=tk.X, pady=(6, 0))

        status_msg = tk.Label(
            btm, text="", font=("Consolas", 7), fg=C["green"], bg=C["bg"]
        )
        status_msg.pack(side=tk.TOP, anchor="w", pady=(0, 4))

        btn_row_bottom = tk.Frame(btm, bg=C["bg"])
        btn_row_bottom.pack(fill=tk.X)

        def save():
            self._save_provider_env_v2(
                entries, env_path, provider_active, selected_models, status_msg, win
            )

        tk.Button(
            btn_row_bottom,
            text="💾 Save to .env",
            font=("Consolas", 9, "bold"),
            fg=C["text"],
            bg=C["app"],
            activebackground=C["app_h"],
            relief=tk.FLAT,
            cursor="hand2",
            padx=16,
            pady=6,
            command=save,
        ).pack(side=tk.LEFT, padx=(0, 8))

        tk.Button(
            btn_row_bottom,
            text="Close",
            font=("Consolas", 9),
            fg=C["text3"],
            bg=C["bg3"],
            activebackground=C["svc_h"],
            relief=tk.FLAT,
            cursor="hand2",
            padx=16,
            pady=6,
            command=win.destroy,
        ).pack(side=tk.LEFT)

        win.protocol(
            "WM_DELETE_WINDOW",
            lambda: (canvas.unbind_all("<MouseWheel>"), win.destroy()),
        )

    def _test_and_fetch_models(
        self,
        provider_id,
        fields,
        entries,
        status_labels,
        model_lists,
        select_btns,
    ):
        status_labels[provider_id].config(text="⏳ testing...", fg=C["yellow"])
        self.root.update_idletasks()

        try:
            models: list[str] = []
            if provider_id == "ollama":
                base = (
                    entries.get("OLLAMA_BASE_URL", tk.Entry()).get().strip()
                    or "http://localhost:11434"
                )
                req = urllib.request.Request(
                    f"{base.rstrip('/')}/api/tags", method="GET"
                )
                with urllib.request.urlopen(req, timeout=5) as r:
                    data = json.loads(r.read())
                    models = sorted([m["name"] for m in data.get("models", [])])

            elif provider_id == "lmstudio":
                base = (
                    entries.get("LMSTUDIO_BASE_URL", tk.Entry()).get().strip()
                    or "http://localhost:1234/v1"
                )
                req = urllib.request.Request(f"{base.rstrip('/')}/models", method="GET")
                with urllib.request.urlopen(req, timeout=5) as r:
                    data = json.loads(r.read())
                    models = sorted([m["id"] for m in data.get("data", [])])

            elif provider_id == "openrouter":
                key = entries.get("OPENROUTER_API_KEY", tk.Entry()).get().strip()
                if not key:
                    status_labels[provider_id].config(
                        text="⚠ No API key", fg=C["yellow"]
                    )
                    return
                base = (
                    entries.get("OPENROUTER_BASE_URL", tk.Entry()).get().strip()
                    or "https://openrouter.ai/api/v1"
                )
                req = urllib.request.Request(f"{base.rstrip('/')}/models")
                req.add_header("Authorization", f"Bearer {key}")
                with urllib.request.urlopen(req, timeout=5) as r:
                    data = json.loads(r.read())
                    models = sorted([m["id"] for m in data.get("data", [])])

            elif provider_id == "groq":
                key = entries.get("GROQ_API_KEY", tk.Entry()).get().strip()
                if not key:
                    status_labels[provider_id].config(
                        text="⚠ No API key", fg=C["yellow"]
                    )
                    return
                req = urllib.request.Request("https://api.groq.com/openai/v1/models")
                req.add_header("Authorization", f"Bearer {key}")
                with urllib.request.urlopen(req, timeout=5) as r:
                    data = json.loads(r.read())
                    models = sorted([m["id"] for m in data.get("data", [])])

            elif provider_id == "huggingface":
                key = entries.get("HUGGINGFACE_API_KEY", tk.Entry()).get().strip()
                if not key:
                    status_labels[provider_id].config(
                        text="⚠ No API key", fg=C["yellow"]
                    )
                    return
                # HF API doesn't list models for Inference API, use known list
                models = [
                    "mistralai/Mistral-7B-Instruct-v0.2",
                    "mistralai/Mixtral-8x7B-Instruct-v0.1",
                    "meta-llama/Llama-2-70b-chat-hf",
                    "meta-llama/Meta-Llama-3-8B-Instruct",
                    "google/gemma-2-9b-it",
                ]

            if models:
                model_lists[provider_id] = models
                select_btns[provider_id].config(state=tk.NORMAL)
                status_labels[provider_id].config(
                    text=f"✅ {len(models)} моделей. Выберите →", fg=C["green"]
                )
            else:
                status_labels[provider_id].config(
                    text="✅ Подключено (0 моделей)", fg=C["green"]
                )

        except urllib.error.HTTPError as e:
            status_labels[provider_id].config(text=f"❌ HTTP {e.code}", fg=C["red"])
        except urllib.error.URLError as e:
            status_labels[provider_id].config(text=f"❌ {e.reason}", fg=C["red"])
        except Exception as e:
            status_labels[provider_id].config(text=f"❌ {e}", fg=C["red"])

    def _open_model_selector(
        self,
        provider_id,
        model_lists,
        model_labels,
        selected_models,
        entries,
        model_env_key,
    ):
        models = model_lists.get(provider_id, [])
        if not models:
            return

        win = tk.Toplevel()
        win.title(f"Select Model — {provider_id}")
        win.geometry("480x400")
        win.configure(bg=C["bg"])
        win.transient(self.root)
        win.grab_set()

        tk.Label(
            win,
            text=f"Доступные модели ({provider_id}):",
            font=("Consolas", 10, "bold"),
            fg=C["cyan"],
            bg=C["bg"],
        ).pack(pady=(8, 4))

        f = tk.Frame(win, bg=C["bg2"])
        f.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)

        scrollbar = tk.Scrollbar(f)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        lb = tk.Listbox(
            f,
            font=("Consolas", 9),
            bg=C["bg4"],
            fg=C["green"],
            selectbackground=C["app_h"],
            selectforeground=C["text"],
            relief=tk.FLAT,
            borderwidth=0,
            highlightthickness=0,
            yscrollcommand=scrollbar.set,
        )
        lb.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=lb.yview)

        for m in models:
            lb.insert(tk.END, m)

        # Pre-select current model if in list
        cur = selected_models[provider_id].get()
        for i, m in enumerate(models):
            if m == cur:
                lb.selection_set(i)
                break

        def confirm():
            sel = lb.curselection()
            if not sel:
                return
            model_name = models[sel[0]]
            selected_models[provider_id].set(model_name)
            model_labels[provider_id].config(text=model_name)
            # Also update the entries dict for saving
            if model_env_key not in entries:
                ent = tk.Entry()
                ent.insert(0, model_name)
                entries[model_env_key] = ent
            else:
                entries[model_env_key].delete(0, tk.END)
                entries[model_env_key].insert(0, model_name)
            win.destroy()

        tk.Button(
            win,
            text="✅ Select",
            font=("Consolas", 9, "bold"),
            fg=C["text"],
            bg=C["app"],
            activebackground=C["app_h"],
            relief=tk.FLAT,
            cursor="hand2",
            padx=16,
            pady=6,
            command=confirm,
        ).pack(pady=(4, 8))

    def _save_provider_env_v2(
        self, entries, env_path, provider_active, selected_models, status_msg, win
    ):
        """Save all provider settings to .env file."""
        lines = []
        if env_path.exists():
            lines = env_path.read_text(encoding="utf-8").splitlines()

        managed_keys = {
            "OPENROUTER_API_KEY",
            "OPENROUTER_BASE_URL",
            "GROQ_API_KEY",
            "HUGGINGFACE_API_KEY",
            "OLLAMA_BASE_URL",
            "LMSTUDIO_BASE_URL",
            "OLLAMA_MODEL",
            "LMSTUDIO_MODEL",
            "GROQ_MODEL",
            "OPENROUTER_MODEL",
            "HUGGINGFACE_MODEL",
            "LLM_PROVIDER",
            "TEMPERATURE",
            "MAX_TOKENS",
        }

        lines = [
            l for l in lines if not any(l.startswith(k + "=") for k in managed_keys)
        ]

        # Save field entries
        for env_key, entry in entries.items():
            val = entry.get().strip()
            if env_key in managed_keys and val:
                lines.append(f"{env_key}={val}")

        # Save active provider
        active = provider_active.get()
        lines.append(f"LLM_PROVIDER={active}")

        # Save model selections that aren't already in entries
        model_map = {
            "ollama": "OLLAMA_MODEL",
            "lmstudio": "LMSTUDIO_MODEL",
            "groq": "GROQ_MODEL",
            "openrouter": "OPENROUTER_MODEL",
            "huggingface": "HUGGINGFACE_MODEL",
        }
        for pid, env_key in model_map.items():
            if env_key not in entries and pid in selected_models:
                val = selected_models[pid].get().strip()
                if val:
                    lines.append(f"{env_key}={val}")

        # Also save OLLAMA_BASE_URL as OLLAMA_URL for backward compat
        base_url = entries.get("OLLAMA_BASE_URL", tk.Entry()).get().strip()
        if base_url:
            lines = [l for l in lines if not l.startswith("OLLAMA_URL=")]
            lines.append(f"OLLAMA_URL={base_url}")

        # Save temperature also as MODEL_TEMPERATURE
        temp = entries.get("TEMPERATURE", tk.Entry()).get().strip()
        if temp:
            lines = [l for l in lines if not l.startswith("MODEL_TEMPERATURE=")]
            lines.append(f"MODEL_TEMPERATURE={temp}")

        env_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

        status_msg.config(
            text="✅ Saved to .env. Restart API to apply changes.", fg=C["green"]
        )
        self._log(f"Provider config saved: active={active}", "ok")

        # Offer restart API
        if self._check_api():

            def ask_restart():
                if tk.messagebox.askyesno(
                    "Restart API?",
                    "API сервер запущен. Перезапустить чтобы применить настройки?",
                    parent=win,
                ):
                    self._cmd_restart_api()
                    status_msg.config(text="✅ Saved. API перезапущен.", fg=C["green"])

            win.after(300, ask_restart)


def main():
    root = tk.Tk()
    CyberLauncher(root)
    root.mainloop()


if __name__ == "__main__":
    main()
