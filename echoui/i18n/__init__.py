"""Internationalization — t, plural, formatting."""

from __future__ import annotations

from typing import Any, Dict

_catalogs: Dict[str, Dict[str, str]] = {"en": {}}
_plural_rules: Dict[str, Dict[str, Dict[str, str]]] = {"en": {}}
_locale = "en"


def set_locale(locale: str) -> None:
    global _locale
    _locale = locale


def get_locale() -> str:
    return _locale


def load_catalog(locale: str, messages: Dict[str, str]) -> None:
    _catalogs[locale] = messages


def load_plural(locale: str, key: str, forms: Dict[str, str]) -> None:
    _plural_rules.setdefault(locale, {})[key] = forms


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


def plural(key: str, count: int, **forms: str) -> str:
    loc = _plural_rules.get(_locale, {}).get(key, forms)
    if count == 1:
        msg = loc.get("one", forms.get("one", key))
    else:
        msg = loc.get("other", forms.get("other", forms.get("one", key)))
    return msg.replace("{n}", str(count))


def format_number(value: float, *, decimals: int = 0) -> str:
    return f"{value:,.{decimals}f}"


def format_currency(value: float, symbol: str = "$") -> str:
    return f"{symbol}{format_number(value, decimals=2)}"


def format_date(value: str) -> str:
    return value
