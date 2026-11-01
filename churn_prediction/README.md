# ChurnGuard

Customer churn prediction for three domains — **Banking**, **Telecom** and
**E-commerce** — built with Flask, Jinja2, vanilla JavaScript and custom CSS.

---

## 1. Project structure

```
churn_prediction/
├── run.py                     # dev entry point (python run.py)
├── requirements.txt
├── .env.example               # copy to .env and edit
├── app/
│   ├── __init__.py            # create_app() factory, error handlers, template helpers
│   ├── config.py              # environment-driven configuration
│   ├── content.py             # static page copy (steps, cards, contact details)
│   ├── errors.py              # AppError / ValidationError / UnknownDomainError / ModelUnavailableError
│   ├── domain/                # field definitions — single source of truth
│   │   ├── schema.py          #   Field / Feature / FormSchema dataclasses
│   │   ├── banking.py
│   │   ├── telecom.py
│   │   └── ecommerce.py
│   ├── routes/
│   │   ├── pages.py           # HTML routes (thin controllers)
│   │   └── api.py             # /api/v1 JSON API
│   ├── services/
│   │   ├── model_registry.py  # lazy, cached, thread-safe model loading
│   │   └── predictor.py       # validation → features → score → log
│   ├── utils/
│   │   ├── validation.py      # schema-driven validation
│   │   └── prediction_log.py  # append-only CSV logging
│   ├── templates/
│   │   ├── base.html          # shared layout
│   │   ├── partials/          # navbar.html, footer.html
│   │   ├── macros/            # forms.html, geo.html
│   │   ├── index.html
│   │   ├── form.html          # generic predictor form (all domains)
│   │   ├── result.html
│   │   ├── contact.html
│   │   └── errors/error.html
│   └── static/
│       ├── css/style.css
│       └── js/
│           ├── main.js        # module entry point
│           └── modules/       # nav.js, forms.js, result.js, state.js
├── data/
│   ├── raw/                   # original datasets
│   └── logs/                  # generated prediction logs
├── models/                    # *.pkl artefacts (model, scaler, encoders per domain)
├── notebooks/                 # EDA / training notebooks
└── tests/smoke_test.py        # no-dependency smoke test
```

### How the layers fit together

| Layer | Responsibility | Depends on |
|-------|----------------|------------|
| `domain/` | What each domain needs (fields, options, feature order) | `errors` |
| `services/` | Loading artefacts, validating, scoring, logging | `domain`, `utils` |
| `routes/` | HTTP only: parse request, call a service, pick a template | `services`, `domain` |
| `templates/` | Presentation; no business rules | route context |
| `static/js/` | UI behaviour (derived fields, locks, animation) | DOM data attributes |

---

## 2. Quick start

```powershell
cd "C:\Users\Sudip Das\churn_prediction"
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt

Copy-Item .env.example .env    # optional, defaults work out of the box
python run.py                  # or: .\run.ps1
```

Open <http://127.0.0.1:5000>.

> The old `python app/app.py` entry point no longer exists — start the app
> from the project root with `python run.py`.

---

## 3. Configuration

All settings come from environment variables (a `.env` file is read
automatically). See `.env.example`.

| Variable | Default | Purpose |
|----------|---------|---------|
| `SECRET_KEY` | `dev-only-change-me` | Flask session signing |
| `DEBUG` | `true` | Debug + auto-reload (set `false` in production) |
| `HOST` | `127.0.0.1` | Bind address |
| `PORT` | `5000` | Bind port |
| `MODELS_DIR` | `models` | Folder with `.pkl` artefacts |
| `LOG_DIR` | `data/logs` | Folder for prediction CSVs |
| `LOG_PII` | `false` | Keep `user_id` / `date_of_birth` in logs |
| `MAX_CONTENT_LENGTH` | `1048576` | Maximum request body size (bytes) |

---

## 4. JSON API (v1)

Base URL: `/api/v1`

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Service status and per-domain model availability |
| `GET` | `/domains` | All domain schemas (field names, types, options) |
| `GET` | `/domains/<domain>` | One domain schema |
| `POST` | `/predict/<domain>` | Score a customer |

Example:

```bash
curl -X POST http://127.0.0.1:5000/api/v1/predict/banking \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "john_smith",
    "age": 35, "gender": "Male", "geography": "Germany",
    "credit_score": 650, "tenure": 5, "balance": 75000,
    "num_of_products": 2, "estimated_salary": 60000,
    "has_credit_card": 1, "is_active_member": 1,
    "card_type": "GOLD", "satisfaction_score": 4, "points_earned": 500
  }'
```

Response:

```json
{
  "domain": "banking",
  "domain_label": "Banking",
  "user_id": "john_smith",
  "churn": false,
  "probability": 11.62,
  "risk_level": "Low"
}
```

Error responses use a consistent envelope:

```json
{"error": {"code": "validation_error", "message": "Please correct the highlighted fields.",
           "fields": {"age": "Must be at least 18."}}}
```

| Status | Code | Meaning |
|--------|------|---------|
| 404 | `unknown_domain` | No model registered for that domain |
| 413 | `payload_too_large` | Body exceeds `MAX_CONTENT_LENGTH` |
| 422 | `validation_error` | Missing / invalid fields |
| 503 | `model_unavailable` | `.pkl` artefacts missing or unreadable |

---

## 5. HTML routes

| Path | Method | Page |
|------|--------|------|
| `/` | GET | Home |
| `/form/<domain>` | GET | Prediction form |
| `/predict/<domain>` | POST | Validate + score, render result (422 re-renders the form with field errors) |
| `/contact` | GET | Contact details |

---

## 6. Adding a new domain

1. Create `app/domain/<name>.py` with a `FormSchema` (rows + ordered features).
2. Register it in `app/domain/__init__.py` (`SCHEMAS`).
3. Drop `<name>_model.pkl`, `<name>_scaler.pkl`, `<name>_encoders.pkl` into `models/`.
4. Add a `DomainCard` entry in `app/content.py` for the home page / navbar.

No route, template or validation code needs to change — the form, API and
logging are all schema-driven.

---

## 7. Prediction logging

Each prediction appends one row to `data/logs/<domain>_logs.csv`.

* Columns are derived from the schema, so the header is deterministic.
* If an existing file has a different header it is **archived** as
  `<domain>_logs_YYYYmmdd-HHMMSS.csv` instead of being corrupted.
* `user_id` and `date_of_birth` are blanked unless `LOG_PII=true`.
* Logging failures are logged and never break a prediction.

---

## 8. Tests

```powershell
python tests/smoke_test.py
```

The smoke test uses Flask's test client (no pytest required) and verifies:

* every page returns `200`;
* the three domains produce the expected predictions for a fixed payload;
* validation errors return `422` with field messages;
* unknown domains return `404`;
* the JSON API returns the documented envelope.

---

## 9. Notes on behaviour changes made during cleanup

* **Card type + no credit card**: the old UI disabled the `Card Type` select,
  which meant the browser did not submit it and the server returned `500`.
  The field is now visually locked, forced to `SILVER`, and still submitted.
* **`Content-Type: application/json` errors** are returned for API paths and
  HTML pages for browser paths, from one shared handler.
* **Duplicates removed**: the three form templates are now one schema-driven
  `form.html`; the navbar/footer live in partials; the unused contact-form
  POST route and email sender (removed from the UI earlier) were deleted.
