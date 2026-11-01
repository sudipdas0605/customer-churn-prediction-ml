"""Domain registry.

Importing this package exposes :func:`get_schema`, the only lookup point used
by routes, templates and services.
"""

from __future__ import annotations

from app.errors import UnknownDomainError

from .banking import BANKING
from .ecommerce import ECOMMERCE
from .schema import Feature, Field, FormSchema, Option
from .telecom import TELECOM

SCHEMAS: dict[str, FormSchema] = {
    schema.domain: schema for schema in (BANKING, TELECOM, ECOMMERCE)
}


def get_schema(domain: str) -> FormSchema:
    """Return the schema for *domain* or raise :class:`UnknownDomainError`."""
    try:
        return SCHEMAS[domain]
    except KeyError as exc:
        raise UnknownDomainError(domain) from exc


def all_schemas() -> tuple[FormSchema, ...]:
    """Return every registered schema in a stable order."""
    return tuple(SCHEMAS.values())


__all__ = [
    "SCHEMAS",
    "FormSchema",
    "Field",
    "Feature",
    "Option",
    "get_schema",
    "all_schemas",
]
