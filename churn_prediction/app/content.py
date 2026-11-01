"""Static page content.

Keeping copy out of templates means the marketing/editorial text can change
without touching markup logic, and the same collections feed navigation,
cards and the footer.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DomainCard:
    key: str
    label: str
    icon: str
    blurb: str
    footer_label: str
    deco_kind: str
    deco_style: str
    deco_size: str


@dataclass(frozen=True)
class Step:
    title: str
    body: str
    deco_kind: str
    deco_style: str
    deco_size: str


@dataclass(frozen=True)
class Detection:
    title: str
    body: str


@dataclass(frozen=True)
class ContactEmail:
    label: str
    address: str
    note: str


DOMAINS: tuple[DomainCard, ...] = (
    DomainCard(
        key="banking",
        label="Banking",
        icon="🏦",
        blurb="See which bank customers might be heading for the exit — based on their account activity and profile trends.",
        footer_label="Banking Model",
        deco_kind="dot",
        deco_style="top:8px; right:8px;",
        deco_size="6px",
    ),
    DomainCard(
        key="telecom",
        label="Telecom",
        icon="📡",
        blurb="Find out which subscribers are thinking of switching providers — using their service usage patterns.",
        footer_label="Telecom Intelligence",
        deco_kind="square",
        deco_style="bottom:8px; left:8px;",
        deco_size="12px",
    ),
    DomainCard(
        key="ecommerce",
        label="E-commerce",
        icon="🛒",
        blurb="Spot online shoppers who might stop buying from you — based on how they browse and shop.",
        footer_label="E-commerce Engine",
        deco_kind="circle-sm",
        deco_style="top:8px; left:8px;",
        deco_size="18px",
    ),
)

STEPS: tuple[Step, ...] = (
    Step(
        title="Select Business Type",
        body=(
            "Tell us what kind of business you run — whether it's a bank, a phone company, or an "
            "online store. Each domain has a purpose-built machine learning model trained on "
            "industry-specific customer data to deliver accurate churn risk predictions."
        ),
        deco_kind="dot",
        deco_style="bottom:8px; left:8px;",
        deco_size="6px",
    ),
    Step(
        title="Stream Telemetry",
        body=(
            "Fill in the relevant customer details such as account balance, contract type, tenure, "
            "usage patterns or purchase behavior. The form adapts to the selected domain so you "
            "only provide the information the model actually needs."
        ),
        deco_kind="corner",
        deco_style="top:10px; right:10px;",
        deco_size="12px",
    ),
    Step(
        title="Instant Risk Scoring",
        body=(
            "The trained model instantly generates a churn probability score and classifies the "
            "customer into Low, Medium or High risk. Use the result to prioritize retention "
            "outreach and reduce customer loss before it happens."
        ),
        deco_kind="square",
        deco_style="bottom:8px; right:8px;",
        deco_size="14px",
    ),
)

DETECTIONS: tuple[Detection, ...] = (
    Detection(
        title="Engagement Level",
        body=(
            "The model checks how actively the customer uses the product or service — login "
            "frequency, app usage, transaction activity — and flags declining engagement as a "
            "churn signal."
        ),
    ),
    Detection(
        title="Account & Financial Behavior",
        body=(
            "Changes in balance, spending patterns, payment behavior and product usage are "
            "analyzed to detect financial disengagement that often precedes churn."
        ),
    ),
    Detection(
        title="Tenure & Loyalty Trends",
        body=(
            "How long the customer has stayed, their contract type and recent changes in loyalty "
            "indicators help the model assess the strength of the customer relationship."
        ),
    ),
    Detection(
        title="Satisfaction & Complaint Signals",
        body=(
            "Satisfaction scores, complaint history and support interactions are weighed to "
            "capture dissatisfaction that may not show up in usage data alone."
        ),
    ),
    Detection(
        title="Usage Pattern Shifts",
        body=(
            "The model identifies shifts in how the customer interacts with the service — reduced "
            "feature usage, slower purchase frequency or shorter session times — that signal "
            "growing disinterest."
        ),
    ),
    Detection(
        title="Risk Score Classification",
        body=(
            "All signals are combined into a single churn probability score, and the customer is "
            "classified as Low, Medium or High risk — so your team knows exactly where to focus "
            "first."
        ),
    ),
)

CONTACT_STEPS: tuple[tuple[str, str], ...] = (
    (
        "Choose Your Channel",
        "Select General Help, Banking Core, Telecom CDR, or E-Commerce stream to route directly "
        "to specialist engineers.",
    ),
    (
        "Have Account ID Ready",
        "Providing your Tenant ID or API key prefix accelerates triage, trace analysis, and model "
        "telemetry debugging.",
    ),
    (
        "Connect Instantly",
        "Connect via the phone hotline or send a message to the dedicated support email address.",
    ),
)

CONTACT_PHONE = {
    "label": "Help Line",
    "number": "+91 XXXXX-XXXXX",
    "tel": "+91 XXXXX-XXXXX",
    "badge": "Available 24/7/365",
}

CONTACT_EMAILS: tuple[ContactEmail, ...] = (
    ContactEmail("Primary Email", "X123@gmail.com", "For any kind of support"),
    ContactEmail("Alternate Email", "X456@gmail.com", "For any kind of support"),
)
