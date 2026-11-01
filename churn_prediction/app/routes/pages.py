"""HTML page routes (thin controllers only)."""

from __future__ import annotations

from flask import Blueprint, current_app, render_template, request

from app.content import (
    CONTACT_EMAILS,
    CONTACT_PHONE,
    CONTACT_STEPS,
    DETECTIONS,
    DOMAINS,
    STEPS,
)
from app.domain import get_schema
from app.errors import ValidationError
from app.services.predictor import PredictorService

bp = Blueprint("pages", __name__)


def _predictor() -> PredictorService:
    return current_app.extensions["predictor"]


@bp.get("/")
def index():
    return render_template(
        "index.html",
        active_page="home",
        show_footer_geo=True,
        steps=STEPS,
        domains=DOMAINS,
        detections=DETECTIONS,
    )


@bp.get("/form/<domain>")
def form(domain: str):
    schema = get_schema(domain)
    return render_template(
        "form.html",
        schema=schema,
        values={},
        errors={},
        active_page=domain,
    )


@bp.post("/predict/<domain>")
def predict(domain: str):
    schema = get_schema(domain)
    try:
        result = _predictor().predict(domain, request.form)
    except ValidationError as error:
        return (
            render_template(
                "form.html",
                schema=schema,
                values=request.form,
                errors=error.fields,
                active_page=domain,
                error_message=error.message,
            ),
            error.status_code,
        )

    return render_template("result.html", result=result, active_page=domain)


@bp.get("/contact")
def contact():
    return render_template(
        "contact.html",
        active_page="contact",
        phone=CONTACT_PHONE,
        emails=CONTACT_EMAILS,
        steps=CONTACT_STEPS,
    )
