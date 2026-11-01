"""Application-wide exception types.

Each error carries an HTTP status, a machine-readable ``code`` and a
human-readable ``message`` so the HTML and JSON surfaces can share one
handler.
"""

from __future__ import annotations


class AppError(Exception):
    """Base class for expected, handled application errors."""

    status_code = 500
    code = "internal_error"
    message = "Something went wrong."

    def __init__(self, message: str | None = None) -> None:
        self.message = message or self.message
        super().__init__(self.message)


class ValidationError(AppError):
    """Submitted input failed validation."""

    status_code = 422
    code = "validation_error"
    message = "Please correct the highlighted fields."

    def __init__(self, fields: dict[str, str], message: str | None = None) -> None:
        self.fields = fields
        super().__init__(message)


class UnknownDomainError(AppError):
    """A domain that has no registered model was requested."""

    status_code = 404
    code = "unknown_domain"

    def __init__(self, domain: str) -> None:
        super().__init__(f"No model is available for domain '{domain}'.")


class ModelUnavailableError(AppError):
    """Model artefacts are missing or could not be loaded."""

    status_code = 503
    code = "model_unavailable"

    def __init__(self, domain: str) -> None:
        super().__init__(f"The '{domain}' model is currently unavailable.")
