"""
i18n localization system for CyberTeacher.
Loads language files and provides translated strings.
"""

import json
import os
from typing import Any, Dict, List

LOCALES_DIR = os.path.join(os.path.dirname(__file__), "locales")
DEFAULT_LANG = "ru"

_cache: Dict[str, Dict[str, Any]] = {}


def _load_locale(lang: str) -> Dict[str, Any]:
    """Load a locale file and return its contents."""
    if lang in _cache:
        return _cache[lang]

    path = os.path.join(LOCALES_DIR, f"{lang}.json")
    if not os.path.exists(path):
        path = os.path.join(LOCALES_DIR, f"{DEFAULT_LANG}.json")

    try:
        with open(path, "r", encoding="utf-8") as f:
            data: Dict[str, Any] = json.load(f)
            _cache[lang] = data
            return data
    except (OSError, IOError, json.JSONDecodeError):
        return {}


def get_locale(lang: str) -> Dict[str, Any]:
    """Get locale dict for a language."""
    return _load_locale(lang)


def t(lang: str, key: str, **kwargs: Any) -> str:
    """Translate a key for the given language.

    Supports nested keys via dot notation: 'ui.welcome'
    Supports interpolation: t(lang, 'ui.error', error='something')
    """
    locale = _load_locale(lang)
    keys = key.split(".")
    value: Any = locale

    for k in keys:
        if isinstance(value, dict):
            value = value.get(k)
            if value is None:
                return key
        else:
            return key

    if isinstance(value, str) and kwargs:
        try:
            return value.format(**kwargs)
        except KeyError:
            return value

    return str(value) if value is not None else key


def get_available_languages() -> List[Dict[str, str]]:
    """Return list of available languages with name and code."""
    langs: List[Dict[str, str]] = []
    if not os.path.exists(LOCALES_DIR):
        return langs

    for fname in os.listdir(LOCALES_DIR):
        if fname.endswith(".json"):
            code = fname[:-5]
            data = _load_locale(code)
            langs.append(
                {
                    "code": code,
                    "name": data.get("language_name", code),
                }
            )

    return sorted(langs, key=lambda x: x["code"])
