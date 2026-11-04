"""Logging configuration for CyberTeacher.

Sets up file-based logging with 7-day rotation for both CLI and API.
Log files: logs/cli/cyberteacher_cli.log, logs/api/cyberteacher_api.log
"""

import logging
import logging.handlers
import os
from datetime import timedelta


def setup_logging(log_dir: str = "logs") -> None:
    """Configure logging with 7-day rotation for CLI and API."""
    os.makedirs(os.path.join(log_dir, "cli"), exist_ok=True)
    os.makedirs(os.path.join(log_dir, "api"), exist_ok=True)

    # ── CLI logger ──
    cli_handler = logging.handlers.TimedRotatingFileHandler(
        os.path.join(log_dir, "cli", "cyberteacher_cli.log"),
        when="midnight",
        interval=7,
        backupCount=4,
        encoding="utf-8",
    )
    cli_handler.setLevel(logging.DEBUG)
    cli_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )

    cli_logger = logging.getLogger("cyberteacher.cli")
    cli_logger.setLevel(logging.DEBUG)
    cli_logger.addHandler(cli_handler)

    # ── API logger ──
    api_handler = logging.handlers.TimedRotatingFileHandler(
        os.path.join(log_dir, "api", "cyberteacher_api.log"),
        when="midnight",
        interval=7,
        backupCount=4,
        encoding="utf-8",
    )
    api_handler.setLevel(logging.DEBUG)
    api_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )

    api_logger = logging.getLogger("cyberteacher.api")
    api_logger.setLevel(logging.DEBUG)
    api_logger.addHandler(api_handler)

    # ── Root logger (for uncaught errors) ──
    root_handler = logging.handlers.TimedRotatingFileHandler(
        os.path.join(log_dir, "cyberteacher_errors.log"),
        when="midnight",
        interval=7,
        backupCount=4,
        encoding="utf-8",
    )
    root_handler.setLevel(logging.WARNING)
    root_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )

    root = logging.getLogger()
    root.addHandler(root_handler)

    # ── Suppress noisy libraries ──
    for name in [
        "sentence_transformers",
        "transformers",
        "huggingface_hub",
        "httpx",
        "httpcore",
        "urllib3",
        "filelock",
        "torch",
        "tqdm",
        "asyncio",
        "uvicorn.access",
        "starlette",
    ]:
        logging.getLogger(name).setLevel(logging.WARNING)

    cli_logger.info("CLI logging initialized → logs/cli/")
    api_logger.info("API logging initialized → logs/api/")
