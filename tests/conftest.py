"""Global pytest configuration for test cleanup."""

import shutil
import tempfile
from typing import Generator

import pytest


# Global temp dir for tests that need it
_test_temp_dirs = []


def pytest_configure(config):
    """Store temp dirs for cleanup."""
    pass


def pytest_unconfigure(config):
    """Clean up after all tests."""
    from db import dispose_engine
    dispose_engine()
    for temp_dir in _test_temp_dirs:
        shutil.rmtree(temp_dir, ignore_errors=True)


def pytest_sessionstart(session):
    """Initialize before test session."""
    pass


def pytest_sessionfinish(session, exitstatus):
    """Final cleanup after all tests."""
    from db import dispose_engine
    dispose_engine()


@pytest.fixture(autouse=True)
def _isolate_modules():
    """Isolate module state between tests."""
    yield


def get_test_temp_dir() -> str:
    """Create a temporary directory that will be cleaned up after the session."""
    temp_dir = tempfile.mkdtemp(prefix="cyberteacher_test_")
    _test_temp_dirs.append(temp_dir)
    return temp_dir