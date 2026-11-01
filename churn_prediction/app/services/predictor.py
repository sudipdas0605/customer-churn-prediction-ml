"""Prediction service: validation, feature assembly, scoring and logging."""

from __future__ import annotations

import logging
import warnings
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

import numpy as np

from app.domain import get_schema
from app.domain.schema import FormSchema
from app.errors import ModelUnavailableError, ValidationError
from app.services.model_registry import ModelBundle, ModelRegistry
from app.utils.prediction_log import log_prediction
from app.utils.validation import validate

LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class PredictionResult:
    """Outcome of a single scoring request."""

    domain: str
    display_name: str
    user_id: str
    churn: bool
    probability: float

    @property
    def risk_level(self) -> str:
        if self.probability >= 70:
            return "High"
        if self.probability >= 40:
            return "Medium"
        return "Low"

    def to_dict(self) -> dict[str, Any]:
        return {
            "domain": self.domain,
            "domain_label": self.display_name,
            "user_id": self.user_id,
            "churn": self.churn,
            "probability": self.probability,
            "risk_level": self.risk_level,
        }


class PredictorService:
    """Turns raw form/JSON payloads into churn predictions."""

    def __init__(
        self,
        registry: ModelRegistry,
        log_dir: Path,
        *,
        log_pii: bool = False,
    ) -> None:
        self._registry = registry
        self._log_dir = Path(log_dir)
        self._log_pii = log_pii

    def predict(self, domain: str, payload: Mapping[str, Any]) -> PredictionResult:
        schema = get_schema(domain)
        values, errors = validate(schema, payload)
        if errors:
            raise ValidationError(errors)

        bundle = self._registry.get(domain)
        matrix = np.asarray(self._build_row(schema, values, bundle), dtype=float).reshape(1, -1)

        with warnings.catch_warnings():
            # Training used a DataFrame; scoring with a plain array is expected.
            warnings.filterwarnings("ignore", message="X does not have valid feature names")
            scaled = bundle.scaler.transform(matrix)
            prediction = int(bundle.model.predict(scaled)[0])
            probability = float(bundle.model.predict_proba(scaled)[0][1])

        result = PredictionResult(
            domain=domain,
            display_name=schema.display_name,
            user_id=str(values.get("user_id") or "Customer"),
            churn=bool(prediction),
            probability=round(probability * 100, 2),
        )

        try:
            log_prediction(
                domain,
                schema,
                values,
                prediction,
                result.probability,
                log_dir=self._log_dir,
                include_pii=self._log_pii,
            )
        except OSError:
            # Logging must never break a prediction.
            LOGGER.warning("Could not append %s prediction log", domain, exc_info=True)

        return result

    @staticmethod
    def _build_row(schema: FormSchema, values: dict[str, Any], bundle: ModelBundle) -> list[float]:
        row: list[float] = []
        for feature in schema.features:
            raw = values.get(feature.source)
            if feature.encoder is None:
                row.append(float(raw))
                continue

            encoder = bundle.encoders.get(feature.encoder)
            if encoder is None:
                raise ModelUnavailableError(schema.domain)

            try:
                row.append(float(encoder.transform([str(raw)])[0]))
            except ValueError as exc:
                raise ValidationError(
                    {feature.source: "This value is not supported by the model."}
                ) from exc
        return row
