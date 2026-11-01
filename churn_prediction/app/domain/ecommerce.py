"""E-commerce domain schema."""

from __future__ import annotations

from .schema import Feature, Field, FormSchema, Option

YES_NO = (Option("1", "Yes"), Option("0", "No"))

ECOMMERCE = FormSchema(
    domain="ecommerce",
    title="E-commerce Churn Prediction",
    icon="🛒",
    display_name="E-commerce",
    description="Predict churn risk for online retail customers.",
    rows=(
        (
            Field("user_id", "User ID", placeholder="e.g. alex_roy (optional)", required=False),
            Field("date_of_birth", "Date of Birth", kind="date", required=False, ui={"derives": "age"}),
        ),
        (
            Field("age", "Age", kind="number", minimum=10, maximum=100),
            Field(
                "gender",
                "Gender",
                kind="select",
                options=(Option("Female", "Female"), Option("Male", "Male"), Option("Other", "Other")),
            ),
        ),
        (
            Field("tenure", "Tenure (months as customer)", kind="number", minimum=0),
            Field(
                "preferred_login_device",
                "Preferred Login Device",
                kind="select",
                options=(Option("Mobile", "Mobile"), Option("Desktop", "Desktop")),
            ),
        ),
        (
            Field(
                "city_tier",
                "City Type",
                kind="select",
                options=(Option("1", "Rural"), Option("2", "Urban")),
            ),
            Field(
                "warehouse_to_home",
                "Distance: Warehouse to Home (km)",
                kind="number",
                step="0.1",
            ),
        ),
        (
            Field("hours_spent_on_app", "Hours Spent on App (daily avg)", kind="number", step="0.1"),
            Field("number_of_devices_registered", "Number of Devices Registered", kind="number", minimum=1),
        ),
        (
            Field(
                "satisfaction_score",
                "Satisfaction Score (1-5)",
                kind="select",
                options=tuple(Option(str(n), str(n)) for n in range(1, 6)),
            ),
            Field("number_of_address", "Number of Saved Addresses", kind="number", minimum=0),
        ),
        (
            Field("complain", "Has Complained Before?", kind="radio", options=YES_NO),
            Field("order_count", "Total Order Count", kind="number", minimum=0),
        ),
        (
            Field("day_since_last_order", "Days Since Last Order", kind="number", minimum=0),
            Field("cashback_amount", "Cashback Amount ($)", kind="number", step="0.01"),
        ),
    ),
    features=(
        Feature("age"),
        Feature("gender", "Gender"),
        Feature("tenure"),
        Feature("preferred_login_device", "PreferredLoginDevice"),
        Feature("city_tier"),
        Feature("warehouse_to_home"),
        Feature("hours_spent_on_app"),
        Feature("number_of_devices_registered"),
        Feature("satisfaction_score"),
        Feature("number_of_address"),
        Feature("complain"),
        Feature("order_count"),
        Feature("day_since_last_order"),
        Feature("cashback_amount"),
    ),
)
