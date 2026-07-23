"""Form fields and validators."""

from __future__ import annotations

import re
from dataclasses import dataclass
from dataclasses import field as dc_field
from typing import Any, Callable, Dict, List, Optional

ValidatorFn = Callable[[Any, Dict[str, Any]], Optional[str]]


def required(msg: str = "Required") -> ValidatorFn:
    def _v(value: Any, _data: Dict[str, Any]) -> Optional[str]:
        if value is None or value == "" or value == []:
            return msg
        return None

    return _v


def email(msg: str = "Invalid email") -> ValidatorFn:
    pat = re.compile(r"^[^@]+@[^@]+\.[^@]+$")

    def _v(value: Any, _data: Dict[str, Any]) -> Optional[str]:
        if value and not pat.match(str(value)):
            return msg
        return None

    return _v


def min_len(n: int, msg: str | None = None) -> ValidatorFn:
    def _v(value: Any, _data: Dict[str, Any]) -> Optional[str]:
        if value is not None and len(str(value)) < n:
            return msg or f"Min length {n}"
        return None

    return _v


def regex(pattern: str, msg: str = "Invalid format") -> ValidatorFn:
    pat = re.compile(pattern)

    def _v(value: Any, _data: Dict[str, Any]) -> Optional[str]:
        if value and not pat.match(str(value)):
            return msg
        return None

    return _v


def range_(lo: float, hi: float, msg: str | None = None) -> ValidatorFn:
    def _v(value: Any, _data: Dict[str, Any]) -> Optional[str]:
        try:
            v = float(value)
        except (TypeError, ValueError):
            return msg or "Not a number"
        if v < lo or v > hi:
            return msg or f"Must be between {lo} and {hi}"
        return None

    return _v


def one_of(options: List[Any], msg: str = "Invalid choice") -> ValidatorFn:
    def _v(value: Any, _data: Dict[str, Any]) -> Optional[str]:
        if value not in options:
            return msg
        return None

    return _v


def is_true(msg: str = "Must be checked") -> ValidatorFn:
    def _v(value: Any, _data: Dict[str, Any]) -> Optional[str]:
        if not value:
            return msg
        return None

    return _v


@dataclass
class Field:
    name: str
    validators: List[ValidatorFn] = dc_field(default_factory=list)
    value: Any = None

    def validate(self, data: Dict[str, Any]) -> Optional[str]:
        val = data.get(self.name, self.value)
        for v in self.validators:
            err = v(val, data)
            if err:
                return err
        return None


def field(name: str, *validators: ValidatorFn) -> Field:
    return Field(name=name, validators=list(validators))


@dataclass
class Form:
    fields: List[Field] = dc_field(default_factory=list)
    cross_validators: List[ValidatorFn] = dc_field(default_factory=list)
    errors: Dict[str, str] = dc_field(default_factory=dict)
    step: int = 0
    steps: List[List[str]] = dc_field(default_factory=list)

    def add(self, f: Field) -> "Form":
        self.fields.append(f)
        return self

    def add_cross(self, fn: ValidatorFn) -> "Form":
        self.cross_validators.append(fn)
        return self

    def wizard(self, *step_fields: List[str]) -> "Form":
        self.steps = list(step_fields)
        return self

    def validate(self, data: Dict[str, Any]) -> bool:
        self.errors.clear()
        active = self._active_fields()
        for f in self.fields:
            if f.name not in active:
                continue
            err = f.validate(data)
            if err:
                self.errors[f.name] = err
        for cv in self.cross_validators:
            err = cv(None, data)
            if err:
                self.errors["_form"] = err
        return len(self.errors) == 0

    def next_step(self) -> bool:
        if self.step < len(self.steps) - 1:
            self.step += 1
            return True
        return False

    def _active_fields(self) -> set[str]:
        if not self.steps:
            return {f.name for f in self.fields}
        if self.step < len(self.steps):
            return set(self.steps[self.step])
        return set()
