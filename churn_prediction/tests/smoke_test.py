"""Smoke test for the refactored application (no pytest required).

Run from the project root::

    python tests/smoke_test.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app import create_app  # noqa: E402

BASELINE = {
    "banking": {
        "user_id": "Baseline",
        "age": 35,
        "gender": "Male",
        "geography": "Germany",
        "credit_score": 650,
        "tenure": 5,
        "balance": 75000,
        "num_of_products": 2,
        "estimated_salary": 60000,
        "has_credit_card": 1,
        "is_active_member": 1,
        "card_type": "GOLD",
        "satisfaction_score": 4,
        "points_earned": 500,
    },
    "telecom": {
        "user_id": "Baseline",
        "age": 40,
        "gender": "Female",
        "senior_citizen": "No",
        "partner": "Yes",
        "dependents": "No",
        "tenure_months": 24,
        "phone_service": "Yes",
        "multiple_lines": "Yes",
        "internet_service": "Fiber optic",
        "online_security": "No",
        "online_backup": "Yes",
        "device_protection": "No",
        "tech_support": "No",
        "streaming_tv": "Yes",
        "streaming_movies": "No",
        "contract": "One year",
        "paperless_billing": "Yes",
        "payment_method": "Electronic check",
        "monthly_charges": 70.5,
        "total_charges": 1700.25,
    },
    "ecommerce": {
        "user_id": "Baseline",
        "age": 30,
        "gender": "Female",
        "tenure": 12,
        "preferred_login_device": "Mobile",
        "city_tier": 1,
        "warehouse_to_home": 10,
        "hours_spent_on_app": 3.5,
        "number_of_devices_registered": 3,
        "satisfaction_score": 4,
        "number_of_address": 2,
        "complain": 1,
        "order_count": 5,
        "day_since_last_order": 10,
        "cashback_amount": 150.75,
    },
}

EXPECTED_PROBABILITY = {"banking": 11.62, "telecom": 44.0, "ecommerce": 82.0}

failures: list[str] = []


def check(name: str, condition: bool, detail: str = "") -> None:
    if condition:
        print(f"  PASS  {name}")
        return
    failures.append(name)
    print(f"  FAIL  {name} {detail}")


def main() -> int:
    app = create_app()
    app.config.update(TESTING=True)
    client = app.test_client()

    print("Pages")
    for path in ["/", "/form/banking", "/form/telecom", "/form/ecommerce", "/contact"]:
        response = client.get(path)
        check(f"GET {path}", response.status_code == 200, f"-> {response.status_code}")

    print("Predictions (HTML)")
    for domain, payload in BASELINE.items():
        response = client.post(f"/predict/{domain}", data=payload)
        html = response.get_data(as_text=True)
        expected = EXPECTED_PROBABILITY[domain]
        check(f"{domain} status", response.status_code == 200, f"-> {response.status_code}")
        check(f"{domain} probability", f"{expected}%" in html, "(value changed)")

    print("Validation")
    broken = dict(BASELINE["banking"])
    broken.pop("age")
    response = client.post("/predict/banking", data=broken)
    check("missing field -> 422", response.status_code == 422, f"-> {response.status_code}")
    check("field error rendered", "This field is required." in response.get_data(as_text=True))

    bad = dict(BASELINE["banking"])
    bad["age"] = 5
    response = client.post("/predict/banking", data=bad)
    check("out-of-range -> 422", response.status_code == 422, f"-> {response.status_code}")

    bad = dict(BASELINE["banking"])
    bad["geography"] = "Atlantis"
    response = client.post("/predict/banking", data=bad)
    check("unknown option -> 422", response.status_code == 422, f"-> {response.status_code}")

    print("JSON API")
    response = client.get("/api/v1/health")
    check("health 200", response.status_code == 200)
    check("health models available", response.get_json()["models"] == {"banking": True, "telecom": True, "ecommerce": True})

    response = client.get("/api/v1/domains")
    check("domains 200", response.status_code == 200 and len(response.get_json()["domains"]) == 3)

    response = client.post("/api/v1/predict/banking", json=BASELINE["banking"])
    body = response.get_json()
    check("api predict 200", response.status_code == 200, f"-> {response.status_code}")
    check("api probability", body["probability"] == EXPECTED_PROBABILITY["banking"], str(body))
    check("api risk level", body["risk_level"] == "Low", str(body))

    response = client.post("/api/v1/predict/telecom", json={"age": 5})
    body = response.get_json()
    check("api validation 422", response.status_code == 422, f"-> {response.status_code}")
    check("api error envelope", body["error"]["code"] == "validation_error", json.dumps(body))
    check("api error fields", "gender" in body["error"]["fields"], json.dumps(body))

    response = client.post("/api/v1/predict/unknown", json={})
    check("unknown domain 404", response.status_code == 404, f"-> {response.status_code}")
    check("unknown domain code", response.get_json()["error"]["code"] == "unknown_domain")

    print()
    if failures:
        print(f"{len(failures)} check(s) failed: {', '.join(failures)}")
        return 1
    print("All checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
