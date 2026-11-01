"""Form/feature schema primitives.

A schema is the single source of truth for one domain: it describes both the
HTML form (field layout, labels, validation rules) and the ordered feature
vector the model expects. Routes, templates, validation and the JSON API all
derive from the same definition.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, Mapping

FieldKind = Literal["text", "number", "date", "select", "radio"]


@dataclass(frozen=True)
class Option:
    """One choice for a select or radio field."""

    value: str
    label: str


@dataclass(frozen=True)
class Field:
    """A single user-facing input."""

    name: str
    label: str
    kind: FieldKind = "text"
    required: bool = True
    placeholder: str = ""
    options: tuple[Option, ...] = ()
    minimum: float | None = None
    maximum: float | None = None
    step: str | None = None
    # UI behaviour hints consumed by static/js/modules/forms.js
    ui: Mapping[str, str] = field(default_factory=dict)

    def allowed_values(self) -> set[str]:
        return {option.value for option in self.options}


@dataclass(frozen=True)
class Feature:
    """One position in the model's input vector.

    ``encoder`` is the key in the saved encoder bundle, or ``None`` when the
    feature is numeric and used as-is.
    """

    source: str
    encoder: str | None = None


@dataclass(frozen=True)
class FormSchema:
    """Complete description of one prediction domain."""

    domain: str
    title: str
    icon: str
    display_name: str
    description: str
    rows: tuple[tuple[Field, ...], ...]
    features: tuple[Feature, ...]

    @property
    def fields(self) -> tuple[Field, ...]:
        return tuple(field for row in self.rows for field in row)

    @property
    def field_names(self) -> tuple[str, ...]:
        return tuple(field.name for field in self.fields)

    def as_dict(self) -> dict:
        """Serialise the schema for the JSON API."""
        return {
            "domain": self.domain,
            "title": self.title,
            "display_name": self.display_name,
            "description": self.description,
            "fields": [
                {
                    "name": f.name,
                    "label": f.label,
                    "type": f.kind,
                    "required": f.required,
                    "min": f.minimum,
                    "max": f.maximum,
                    "options": [{"value": o.value, "label": o.label} for o in f.options],
                }
                for f in self.fields
            ],
        }
