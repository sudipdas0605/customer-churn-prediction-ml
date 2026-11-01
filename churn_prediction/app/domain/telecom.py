"""Telecom domain schema."""

from __future__ import annotations

from .schema import Feature, Field, FormSchema, Option

YES_NO = (Option("Yes", "Yes"), Option("No", "No"))
SERVICE = (
    Option("No", "No"),
    Option("Yes", "Yes"),
    Option("No internet service", "No internet service"),
)
MONTHLY_CHARGES = Field("monthly_charges", "Monthly Charges ($)", kind="number", step="0.01")

TELECOM = FormSchema(
    domain="telecom",
    title="Telecom Churn Prediction",
    icon="📡",
    display_name="Telecom",
    description="Predict churn risk for telecom subscribers.",
    rows=(
        (
            Field("user_id", "User ID", placeholder="e.g. priya_sharma (optional)", required=False),
            Field("date_of_birth", "Date of Birth", kind="date", required=False, ui={"derives": "age"}),
        ),
        (
            Field("age", "Age", kind="number", minimum=18, maximum=100),
            Field("gender", "Gender", kind="select", options=(Option("Female", "Female"), Option("Male", "Male"))),
            Field(
                "senior_citizen",
                "Senior Citizen?",
                kind="radio",
                options=YES_NO,
                ui={"auto_check_from": "age", "threshold": "50"},
            ),
        ),
        (
            Field("partner", "Has Partner?", kind="radio", options=YES_NO),
            Field("dependents", "Has Dependents?", kind="radio", options=YES_NO),
        ),
        (
            Field("tenure_months", "Tenure (months)", kind="number", minimum=0, maximum=100),
            Field("phone_service", "Phone Service?", kind="select", options=YES_NO),
        ),
        (
            Field(
                "multiple_lines",
                "Multiple Lines",
                kind="select",
                options=(
                    Option("No", "No"),
                    Option("Yes", "Yes"),
                    Option("No phone service", "No phone service"),
                ),
            ),
            Field(
                "internet_service",
                "Internet Service",
                kind="select",
                options=(
                    Option("DSL", "DSL"),
                    Option("Fiber optic", "Fiber optic"),
                    Option("No", "No"),
                ),
            ),
        ),
        (
            Field("online_security", "Online Security", kind="select", options=SERVICE),
            Field("online_backup", "Online Backup", kind="select", options=SERVICE),
        ),
        (
            Field("device_protection", "Device Protection", kind="select", options=SERVICE),
            Field("tech_support", "Tech Support", kind="select", options=SERVICE),
        ),
        (
            Field("streaming_tv", "Streaming TV", kind="select", options=SERVICE),
            Field("streaming_movies", "Streaming Movies", kind="select", options=SERVICE),
        ),
        (
            Field(
                "contract",
                "Contract Type",
                kind="select",
                options=(
                    Option("Month-to-month", "Month-to-month"),
                    Option("One year", "One year"),
                    Option("Two year", "Two year"),
                ),
            ),
            Field("paperless_billing", "Paperless Billing?", kind="select", options=YES_NO),
        ),
        (
            Field(
                "payment_method",
                "Payment Method",
                kind="select",
                options=(
                    Option("Bank transfer (automatic)", "Bank transfer (automatic)"),
                    Option("Credit card (automatic)", "Credit card (automatic)"),
                    Option("Electronic check", "Electronic check"),
                    Option("Mailed check", "Mailed check"),
                ),
            ),
            MONTHLY_CHARGES,
        ),
        (
            Field("total_charges", "Total Charges ($)", kind="number", step="0.01"),
        ),
    ),
    features=(
        Feature("gender", "Gender"),
        Feature("senior_citizen", "Senior Citizen"),
        Feature("partner", "Partner"),
        Feature("dependents", "Dependents"),
        Feature("tenure_months"),
        Feature("phone_service", "Phone Service"),
        Feature("multiple_lines", "Multiple Lines"),
        Feature("internet_service", "Internet Service"),
        Feature("online_security", "Online Security"),
        Feature("online_backup", "Online Backup"),
        Feature("device_protection", "Device Protection"),
        Feature("tech_support", "Tech Support"),
        Feature("streaming_tv", "Streaming TV"),
        Feature("streaming_movies", "Streaming Movies"),
        Feature("contract", "Contract"),
        Feature("paperless_billing", "Paperless Billing"),
        Feature("payment_method", "Payment Method"),
        Feature("monthly_charges"),
        Feature("total_charges"),
    ),
)
