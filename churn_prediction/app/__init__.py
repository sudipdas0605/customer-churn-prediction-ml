"""ChurnGuard application factory.

Wiring only: configuration in, services registered on ``app.extensions``,
blueprints mounted, error handling installed. Business logic lives in
``app.services`` and field definitions in ``app.domain``.
"""

from __future__ import annotations

import logging
from datetime import datetime

from flask import Flask, jsonify, render_template, request
from werkzeug.exceptions import HTTPException

from app.config import Config, load_config
from app.content import DOMAINS
from app.errors import AppError, ValidationError
from app.routes import api_blueprint, pages_blueprint
from app.services.model_registry import ModelRegistry
from app.services.predictor import PredictorService

LOGGER = logging.getLogger(__name__)


def _is_api_request() -> bool:
    prefix = request.blueprint == "api" or request.path.startswith("/api/")
    return prefix


def _error_payload(code: str, message: str, fields: dict[str, str] | None = None) -> dict:
    error: dict = {"code": code, "message": message}
    if fields:
        error["fields"] = fields
    return {"error": error}


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(AppError)
    def handle_app_error(error: AppError):
        if _is_api_request():
            fields = error.fields if isinstance(error, ValidationError) else None
            return jsonify(_error_payload(error.code, error.message, fields)), error.status_code

        return (
            render_template(
                "errors/error.html",
                status=error.status_code,
                title="Request could not be completed",
                message=error.message,
            ),
            error.status_code,
        )

    @app.errorhandler(HTTPException)
    def handle_http_error(error: HTTPException):
        if _is_api_request():
            code = (error.name or "http_error").lower().replace(" ", "_")
            return jsonify(_error_payload(code, error.description)), error.code or 500

        return (
            render_template(
                "errors/error.html",
                status=error.code or 500,
                title=error.name or "Error",
                message=error.description,
            ),
            error.code or 500,
        )

    @app.errorhandler(Exception)
    def handle_unexpected_error(error: Exception):
        LOGGER.exception("Unhandled error on %s", request.path)
        if app.config.get("DEBUG"):
            raise error
        if _is_api_request():
            return jsonify(_error_payload("internal_error", "Internal server error.")), 500
        return (
            render_template(
                "errors/error.html",
                status=500,
                title="Something went wrong",
                message="An unexpected error occurred. Please try again.",
            ),
            500,
        )

    @app.errorhandler(413)
    def handle_too_large(error):
        if _is_api_request():
            return jsonify(_error_payload("payload_too_large", "Request body is too large.")), 413
        return (
            render_template(
                "errors/error.html",
                status=413,
                title="Payload too large",
                message="The submitted form is larger than allowed.",
            ),
            413,
        )


def register_template_helpers(app: Flask) -> None:
    @app.template_filter("num")
    def format_number(value) -> str:
        """Render ``18.0`` as ``18`` for HTML min/max attributes."""
        if value is None:
            return ""
        number = float(value)
        return str(int(number)) if number.is_integer() else str(number)

    @app.context_processor
    def inject_globals() -> dict:
        return {"nav_domains": DOMAINS, "current_year": datetime.now().year}


def create_app(config: Config | None = None) -> Flask:
    """Create and configure the Flask application."""
    cfg = config or load_config()

    app = Flask(__name__)
    app.config.update(cfg.flask_settings)
    app.json.sort_keys = False

    registry = ModelRegistry(cfg.models_dir)
    app.extensions["model_registry"] = registry
    app.extensions["predictor"] = PredictorService(registry, cfg.log_dir, log_pii=cfg.log_pii)

    app.register_blueprint(pages_blueprint)
    app.register_blueprint(api_blueprint, url_prefix=cfg.api_prefix)

    register_error_handlers(app)
    register_template_helpers(app)

    LOGGER.info("ChurnGuard ready (models: %s)", cfg.models_dir)
    return app
