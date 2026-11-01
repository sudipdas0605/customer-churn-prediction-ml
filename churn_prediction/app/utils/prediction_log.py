"""Append-only CSV prediction logging.

Each domain writes to ``<log_dir>/<domain>_logs.csv``. Columns are derived
from the domain schema so the header is always deterministic; if an existing
file has a different header it is archived instead of being silently
corrupted.

Personally identifiable fields (``user_id``, ``date_of_birth``) are blanked
unless ``LOG_PII=true`` — they are not needed for model analysis.
"""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from typing import Any

from app.domain.schema import FormSchema

PII_FIELDS = ("user_id", "date_of_birth")
RESULT_COLUMNS = ("predicted_churn", "churn_probability", "actual_outcome", "timestamp")


def _columns_for(schema: FormSchema) -> list[str]:
    return [*schema.field_names, *RESULT_COLUMNS]


def _format(value: Any) -> str:
    if isinstance(value, float):
        return f"{value:g}"
    return "" if value is None else str(value)


def _claim_file(path: Path, columns: list[str]) -> None:
    """Ensure *path* exists with the expected header, archiving stale files."""
    if path.exists() and path.stat().st_size > 0:
        with path.open(newline="", encoding="utf-8") as handle:
            existing = next(csv.reader(handle), [])
        if existing == columns:
            return
        archive = path.with_name(f"{path.stem}_{datetime.now():%Y%m%d-%H%M%S}{path.suffix}")
        path.replace(archive)

    with path.open("w", newline="", encoding="utf-8") as handle:
        csv.writer(handle).writerow(columns)


def log_prediction(
    domain: str,
    schema: FormSchema,
    values: dict[str, Any],
    prediction: int,
    probability: float,
    *,
    log_dir: Path,
    include_pii: bool = False,
) -> Path:
    """Append one prediction row and return the log file path."""
    log_dir.mkdir(parents=True, exist_ok=True)
    path = log_dir / f"{domain}_logs.csv"
    columns = _columns_for(schema)
    _claim_file(path, columns)

    row: dict[str, Any] = {name: values.get(name, "") for name in schema.field_names}
    if not include_pii:
        for name in PII_FIELDS:
            if name in row:
                row[name] = ""
    row.update(
        predicted_churn=prediction,
        churn_probability=f"{probability:.2f}",
        actual_outcome="",
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )

    with path.open("a", newline="", encoding="utf-8") as handle:
        csv.DictWriter(handle, fieldnames=columns).writerow(
            {column: _format(row.get(column, "")) for column in columns}
        )

    return path
