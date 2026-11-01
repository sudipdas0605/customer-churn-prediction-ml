"""Schema-driven input validation.

The same rules protect the HTML form and the JSON API, so a field can never
be valid in one surface and invalid in the other.
"""

from __future__ import annotations

from datetime import date
from typing import Any, Mapping

from app.domain.schema import Field, FormSchema

MAX_TEXT_LENGTH = 128


def _coerce(field: Field, raw: Any) -> tuple[Any, str | None]:
    """Return ``(value, error)`` for a single field."""
    if isinstance(raw, str):
        raw = raw.strip()
    elif raw is None:
        raw = ""

    if raw == "":
        if field.required:
            return None, "This field is required."
        return "", None

    if field.kind == "number":
        try:
            number = float(raw)
        except (TypeError, ValueError):
            return None, "Enter a valid number."
        if field.minimum is not None and number < field.minimum:
            return None, f"Must be at least {field.minimum:g}."
        if field.maximum is not None and number > field.maximum:
            return None, f"Must be at most {field.maximum:g}."
        return number, None

    if field.kind == "date":
        try:
            date.fromisoformat(str(raw))
        except ValueError:
            return None, "Enter a valid date."
        return str(raw), None

    if field.kind in {"select", "radio"}:
        text = str(raw)
        if text not in field.allowed_values():
            return None, "Choose a valid option."
        return text, None

    text = str(raw)
    if len(text) > MAX_TEXT_LENGTH:
        return None, f"Must be {MAX_TEXT_LENGTH} characters or fewer."
    return text, None


def validate(schema: FormSchema, data: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, str]]:
    """Validate *data* against *schema*.

    Returns a ``(values, errors)`` pair. ``values`` only contains known fields
    and is safe to feed to the model; ``errors`` maps field names to messages.
    """
    values: dict[str, Any] = {}
    errors: dict[str, str] = {}

    for field in schema.fields:
        value, error = _coerce(field, data.get(field.name))
        if error:
            errors[field.name] = error
        else:
            values[field.name] = value

    return values, errors
