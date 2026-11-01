"""Versioned JSON API.

The API mirrors the HTML flows: ``POST /api/v1/predict/<domain>`` accepts a
JSON object (or form data) and returns a JSON prediction. Schemas are
discoverable via ``GET /api/v1/domains``.
"""

from __future__ import annotations

from collections.abc import Mapping

from flask import Blueprint, current_app, jsonify, request

from app.domain import all_schemas, get_schema
from app.errors import ValidationError
from app.services.model_registry import ModelRegistry
from app.services.predictor import PredictorService

bp = Blueprint("api", __name__)

API_VERSION = "1.0"


def _registry() -> ModelRegistry:
    return current_app.extensions["model_registry"]


def _predictor() -> PredictorService:
    return current_app.extensions["predictor"]


@bp.get("/health")
def health():
    models = {schema.domain: _registry().is_available(schema.domain) for schema in all_schemas()}
    return jsonify(
        {
            "status": "ok" if all(models.values()) else "degraded",
            "version": API_VERSION,
            "models": models,
        }
    )


@bp.get("/domains")
def list_domains():
    return jsonify({"version": API_VERSION, "domains": [schema.as_dict() for schema in all_schemas()]})


@bp.get("/domains/<domain>")
def domain_detail(domain: str):
    return jsonify(get_schema(domain).as_dict())


@bp.post("/predict/<domain>")
def predict(domain: str):
    payload = request.get_json(silent=True)
    if payload is None:
        payload = request.form.to_dict()

    if not isinstance(payload, Mapping):
        raise ValidationError({"_body": "Request body must be a JSON object."})

    result = _predictor().predict(domain, payload)
    return jsonify(result.to_dict())
