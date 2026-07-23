"""Internationalization."""

from __future__ import annotations

from typing import Any, Dict

_catalogs: Dict[str, Dict[str, str]] = {"en": {}}
_locale = "en"


def set_locale(locale: str) -> None:
    global _locale
    _locale = locale


def get_locale() -> str:
    return _locale


def load_catalog(locale: str, messages: Dict[str, str]) -> None:
    _catalogs[locale] = messages


def t(key: str, **kwargs: Any) -> str:
    msg = _catalogs.get(_locale, {}).get(key, key)
    if kwargs:
        try:
            return msg.format(**kwargs)
        except (KeyError, ValueError):
            return msg
    return msg


def translate(key: str, **kwargs: Any) -> str:
    return t(key, **kwargs)
