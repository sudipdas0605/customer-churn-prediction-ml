"""Banking domain schema."""

from __future__ import annotations

from .schema import Feature, Field, FormSchema, Option

GENDER_OPTIONS = (Option("Female", "Female"), Option("Male", "Male"))
YES_NO = (Option("1", "Yes"), Option("0", "No"))

BANKING = FormSchema(
    domain="banking",
    title="Banking Churn Prediction",
    icon="🏦",
    display_name="Banking",
    description="Predict churn risk for retail banking customers.",
    rows=(
        (
            Field("user_id", "User ID", placeholder="e.g. john_smith (optional)", required=False),
            Field("date_of_birth", "Date of Birth", kind="date", required=False, ui={"derives": "age"}),
        ),
        (
            Field("age", "Age", kind="number", minimum=18, maximum=100),
            Field("gender", "Gender", kind="select", options=GENDER_OPTIONS),
        ),
        (
            Field(
                "geography",
                "Geography",
                kind="select",
                options=(Option("France", "France"), Option("Germany", "Germany"), Option("Spain", "Spain")),
            ),
            Field("credit_score", "Credit Score", kind="number", minimum=300, maximum=900),
        ),
        (
            Field("tenure", "Tenure (years with bank)", kind="number", minimum=0, maximum=20),
            Field("balance", "Account Balance", kind="number", step="0.01"),
        ),
        (
            Field(
                "num_of_products",
                "Number of Products",
                kind="select",
                options=tuple(Option(str(n), str(n)) for n in range(1, 5)),
            ),
            Field("estimated_salary", "Estimated Salary", kind="number", step="0.01"),
        ),
        (
            Field("has_credit_card", "Has Credit Card?", kind="radio", options=YES_NO),
            Field("is_active_member", "Is Active Member?", kind="radio", options=YES_NO),
        ),
        (
            Field(
                "card_type",
                "Card Type",
                kind="select",
                options=(
                    Option("SILVER", "Silver"),
                    Option("GOLD", "Gold"),
                    Option("PLATINUM", "Platinum"),
                    Option("DIAMOND", "Diamond"),
                ),
                ui={"locked_when": "has_credit_card=0", "locked_value": "SILVER"},
            ),
            Field(
                "satisfaction_score",
                "Satisfaction Score (1-5)",
                kind="select",
                options=tuple(Option(str(n), str(n)) for n in range(1, 6)),
            ),
        ),
        (
            Field("points_earned", "Reward Points Earned", kind="number", minimum=0),
        ),
    ),
    features=(
        Feature("credit_score"),
        Feature("geography", "Geography"),
        Feature("gender", "Gender"),
        Feature("age"),
        Feature("tenure"),
        Feature("balance"),
        Feature("num_of_products"),
        Feature("has_credit_card"),
        Feature("is_active_member"),
        Feature("estimated_salary"),
        Feature("satisfaction_score"),
        Feature("card_type", "Card Type"),
        Feature("points_earned"),
    ),
)
