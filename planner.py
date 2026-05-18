from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any


YEARS = 5


@dataclass(frozen=True)
class CountryProfile:
    name: str
    currency_code: str
    currency_locale: str
    usd_to_local: float
    local_rounding: int
    labor_multiplier: float
    employer_oncost: float
    facility_multiplier: float
    market_multiplier: float
    funding_buffer: float


@dataclass(frozen=True)
class RoleTemplate:
    title: str
    department: str
    reports_to: str | None
    start_year: int
    share: float
    base_salary: int
    rationale: str
    scarcity_premium: float = 0.0
    band_spread: float = 0.12


@dataclass(frozen=True)
class IndustryProfile:
    name: str
    narrative: str
    salary_multiplier: float
    gross_margin: float
    revenue_per_head: int
    revenue_ramp: tuple[float, ...]
    headcount_plan: tuple[int, ...]
    tools_per_employee: int
    facility_per_employee: int
    compliance_per_employee: int
    capex_plan: tuple[int, ...]
    sales_marketing_ratio: float
    roles: tuple[RoleTemplate, ...]


@dataclass(frozen=True)
class LeannessProfile:
    name: str
    description: str
    headcount_multiplier: float
    salary_multiplier: float
    band_spread_delta: float
    revenue_multiplier: float
    tools_multiplier: float
    facilities_multiplier: float
    compliance_multiplier: float
    sales_marketing_multiplier: float
    general_admin_multiplier: float
    capex_multiplier: float
    funding_buffer_multiplier: float


def role(
    title: str,
    department: str,
    reports_to: str | None,
    start_year: int,
    share: float,
    base_salary: int,
    rationale: str,
    scarcity_premium: float = 0.0,
    band_spread: float = 0.12,
) -> RoleTemplate:
    return RoleTemplate(
        title=title,
        department=department,
        reports_to=reports_to,
        start_year=start_year,
        share=share,
        base_salary=base_salary,
        rationale=rationale,
        scarcity_premium=scarcity_premium,
        band_spread=band_spread,
    )


COUNTRY_ALIASES = {
    "us": "united states",
    "usa": "united states",
    "united states of america": "united states",
    "uk": "united kingdom",
    "uae": "united arab emirates",
}


COUNTRIES = {
    "united states": CountryProfile(
        name="United States",
        currency_code="USD",
        currency_locale="en-US",
        usd_to_local=1.00,
        local_rounding=100,
        labor_multiplier=1.00,
        employer_oncost=0.22,
        facility_multiplier=1.00,
        market_multiplier=1.08,
        funding_buffer=1.15,
    ),
    "india": CountryProfile(
        name="India",
        currency_code="INR",
        currency_locale="en-IN",
        usd_to_local=83.00,
        local_rounding=1000,
        labor_multiplier=0.42,
        employer_oncost=0.18,
        facility_multiplier=0.46,
        market_multiplier=0.88,
        funding_buffer=1.10,
    ),
    "united kingdom": CountryProfile(
        name="United Kingdom",
        currency_code="GBP",
        currency_locale="en-GB",
        usd_to_local=0.79,
        local_rounding=100,
        labor_multiplier=0.88,
        employer_oncost=0.20,
        facility_multiplier=0.92,
        market_multiplier=0.96,
        funding_buffer=1.12,
    ),
    "germany": CountryProfile(
        name="Germany",
        currency_code="EUR",
        currency_locale="de-DE",
        usd_to_local=0.92,
        local_rounding=100,
        labor_multiplier=0.93,
        employer_oncost=0.21,
        facility_multiplier=0.94,
        market_multiplier=0.98,
        funding_buffer=1.10,
    ),
    "singapore": CountryProfile(
        name="Singapore",
        currency_code="SGD",
        currency_locale="en-SG",
        usd_to_local=1.35,
        local_rounding=100,
        labor_multiplier=0.97,
        employer_oncost=0.17,
        facility_multiplier=1.08,
        market_multiplier=1.02,
        funding_buffer=1.08,
    ),
    "canada": CountryProfile(
        name="Canada",
        currency_code="CAD",
        currency_locale="en-CA",
        usd_to_local=1.37,
        local_rounding=100,
        labor_multiplier=0.90,
        employer_oncost=0.19,
        facility_multiplier=0.90,
        market_multiplier=0.98,
        funding_buffer=1.10,
    ),
    "australia": CountryProfile(
        name="Australia",
        currency_code="AUD",
        currency_locale="en-AU",
        usd_to_local=1.52,
        local_rounding=100,
        labor_multiplier=0.95,
        employer_oncost=0.18,
        facility_multiplier=0.96,
        market_multiplier=0.99,
        funding_buffer=1.09,
    ),
    "united arab emirates": CountryProfile(
        name="United Arab Emirates",
        currency_code="AED",
        currency_locale="en-AE",
        usd_to_local=3.67,
        local_rounding=100,
        labor_multiplier=0.83,
        employer_oncost=0.12,
        facility_multiplier=1.03,
        market_multiplier=1.00,
        funding_buffer=1.10,
    ),
    "brazil": CountryProfile(
        name="Brazil",
        currency_code="BRL",
        currency_locale="pt-BR",
        usd_to_local=5.10,
        local_rounding=100,
        labor_multiplier=0.58,
        employer_oncost=0.20,
        facility_multiplier=0.61,
        market_multiplier=0.90,
        funding_buffer=1.14,
    ),
    "default": CountryProfile(
        name="Global Benchmark",
        currency_code="USD",
        currency_locale="en-US",
        usd_to_local=1.00,
        local_rounding=100,
        labor_multiplier=0.85,
        employer_oncost=0.19,
        facility_multiplier=0.85,
        market_multiplier=0.95,
        funding_buffer=1.10,
    ),
}


SAAS_ROLES = (
    role("CEO", "Executive", None, 1, 0.05, 190000, "Founder-caliber commercial and fundraising leadership."),
    role("CTO", "Executive", "CEO", 1, 0.05, 180000, "Owns platform architecture, security, and engineering quality.", 0.12),
    role("Product Manager", "Product", "CEO", 1, 0.06, 130000, "Translates customer pain points into a shippable roadmap."),
    role("Senior Software Engineer", "Engineering", "CTO", 1, 0.14, 150000, "Builds the core product quickly while mentoring the team.", 0.10),
    role("Software Engineer", "Engineering", "CTO", 1, 0.20, 120000, "Delivers application features, integrations, and internal tooling.", 0.08),
    role("UX Designer", "Product", "Product Manager", 1, 0.05, 115000, "Improves onboarding, activation, and product usability."),
    role("QA Automation Engineer", "Engineering", "CTO", 2, 0.06, 110000, "Protects release quality as product surface area grows."),
    role("DevOps Engineer", "Engineering", "CTO", 2, 0.06, 135000, "Keeps cloud infrastructure reliable and scalable.", 0.12),
    role("Head of Sales", "Sales", "CEO", 2, 0.05, 160000, "Builds a repeatable pipeline and closes early enterprise revenue."),
    role("Account Executive", "Sales", "Head of Sales", 2, 0.10, 120000, "Converts qualified demand into annual recurring revenue."),
    role("Marketing Manager", "Marketing", "CEO", 2, 0.05, 105000, "Creates category messaging and paid demand generation."),
    role("Customer Success Manager", "Customer Success", "Head of Sales", 2, 0.08, 98000, "Protects renewals, expansion, and reference customers."),
    role("Finance Manager", "Finance", "CEO", 3, 0.04, 110000, "Owns budgeting, controls, and investor-ready reporting."),
    role("HR Generalist", "People", "CEO", 3, 0.03, 85000, "Keeps hiring, onboarding, and policies consistent."),
    role("Data Analyst", "Data", "Product Manager", 3, 0.03, 102000, "Turns usage data into pricing, retention, and funnel insights.", 0.06),
)


FINTECH_ROLES = (
    role("CEO", "Executive", None, 1, 0.05, 200000, "Balances regulation, fundraising, partnerships, and growth."),
    role("CTO", "Executive", "CEO", 1, 0.05, 190000, "Leads secure architecture and payment-grade systems.", 0.14),
    role("Product Manager", "Product", "CEO", 1, 0.05, 140000, "Shapes financial workflows into trustworthy products."),
    role("Senior Software Engineer", "Engineering", "CTO", 1, 0.13, 160000, "Builds resilient systems with strong audit trails.", 0.12),
    role("Software Engineer", "Engineering", "CTO", 1, 0.16, 128000, "Implements core product features and integrations.", 0.08),
    role("Compliance Lead", "Compliance", "CEO", 1, 0.06, 155000, "Keeps licensing, KYC, AML, and controls on track.", 0.14),
    role("Risk Analyst", "Risk", "Compliance Lead", 2, 0.06, 120000, "Monitors fraud patterns, risk rules, and loss exposure.", 0.10),
    role("QA Automation Engineer", "Engineering", "CTO", 2, 0.05, 115000, "Supports safe releases in a regulated environment."),
    role("DevOps Engineer", "Engineering", "CTO", 2, 0.05, 142000, "Owns uptime, CI/CD controls, and infrastructure security.", 0.12),
    role("Head of Partnerships", "Business Development", "CEO", 2, 0.05, 150000, "Builds banking, payments, and channel relationships."),
    role("Sales Manager", "Sales", "CEO", 2, 0.08, 135000, "Drives pipeline in target commercial segments."),
    role("Customer Success Manager", "Customer Success", "Sales Manager", 2, 0.06, 105000, "Protects onboarding quality and customer retention."),
    role("Finance Manager", "Finance", "CEO", 3, 0.04, 118000, "Owns treasury visibility, controls, and reporting."),
    role("Data Analyst", "Data", "Product Manager", 3, 0.04, 108000, "Improves unit economics and underwriting decisions.", 0.08),
    role("HR Generalist", "People", "CEO", 3, 0.03, 90000, "Supports scaling while keeping policy discipline."),
)


HEALTHTECH_ROLES = (
    role("CEO", "Executive", None, 1, 0.05, 195000, "Leads fundraising, provider partnerships, and go-to-market execution."),
    role("Chief Product Officer", "Executive", "CEO", 1, 0.05, 180000, "Owns solution design across patient, provider, and workflow needs.", 0.10),
    role("Clinical Operations Lead", "Clinical Operations", "CEO", 1, 0.07, 150000, "Ensures service design fits clinical reality and patient safety.", 0.14),
    role("Senior Software Engineer", "Engineering", "Chief Product Officer", 1, 0.13, 150000, "Builds the product backbone and data workflows.", 0.10),
    role("Software Engineer", "Engineering", "Chief Product Officer", 1, 0.15, 122000, "Implements platform features and integrations.", 0.08),
    role("UX Designer", "Product", "Chief Product Officer", 1, 0.05, 112000, "Designs accessible experiences for patients and staff."),
    role("Regulatory Affairs Manager", "Compliance", "Clinical Operations Lead", 2, 0.06, 145000, "Keeps the company aligned to healthcare compliance requirements.", 0.14),
    role("Data Analyst", "Data", "Chief Product Officer", 2, 0.05, 104000, "Measures outcomes, adherence, and product effectiveness."),
    role("QA Automation Engineer", "Engineering", "Chief Product Officer", 2, 0.05, 110000, "Adds release confidence for clinical workflows."),
    role("Head of Sales", "Sales", "CEO", 2, 0.05, 155000, "Builds provider and payer pipeline discipline."),
    role("Account Executive", "Sales", "Head of Sales", 2, 0.08, 118000, "Closes new logos in targeted care segments."),
    role("Customer Success Manager", "Customer Success", "Head of Sales", 2, 0.07, 98000, "Supports adoption and contract expansion."),
    role("Finance Manager", "Finance", "CEO", 3, 0.04, 112000, "Keeps reporting, burn control, and planning reliable."),
    role("HR Generalist", "People", "CEO", 3, 0.03, 86000, "Supports hiring discipline and employee operations."),
    role("Operations Manager", "Operations", "Clinical Operations Lead", 3, 0.07, 102000, "Turns the service model into repeatable delivery."),
)


ECOMMERCE_ROLES = (
    role("CEO", "Executive", None, 1, 0.04, 180000, "Owns brand direction, growth priorities, and capital allocation."),
    role("Operations Manager", "Operations", "CEO", 1, 0.08, 110000, "Runs daily execution across inventory, vendors, and SLAs."),
    role("Product Manager", "Product", "CEO", 1, 0.05, 125000, "Prioritizes storefront, conversion, and merchandising initiatives."),
    role("Software Engineer", "Engineering", "Product Manager", 1, 0.08, 118000, "Builds internal tools, integrations, and website changes.", 0.06),
    role("UX Designer", "Product", "Product Manager", 1, 0.05, 108000, "Improves conversion flows and brand experience."),
    role("Finance Manager", "Finance", "CEO", 1, 0.05, 105000, "Tracks margin, cash conversion, and inventory economics."),
    role("Supply Chain Manager", "Operations", "Operations Manager", 2, 0.09, 115000, "Balances inventory turns, vendor reliability, and landed costs."),
    role("Performance Marketing Manager", "Marketing", "CEO", 2, 0.08, 118000, "Owns acquisition efficiency across paid channels."),
    role("Merchandising Manager", "Product", "CEO", 2, 0.07, 102000, "Shapes assortment and promotional cadence."),
    role("Customer Support Lead", "Customer Support", "Operations Manager", 2, 0.10, 78000, "Maintains response quality and repeat purchase health."),
    role("Sales Manager", "Sales", "CEO", 2, 0.05, 120000, "Builds wholesale or channel relationships when relevant."),
    role("Procurement Analyst", "Operations", "Supply Chain Manager", 3, 0.07, 88000, "Improves sourcing discipline and reorder planning."),
    role("Data Analyst", "Data", "Finance Manager", 3, 0.04, 98000, "Improves pricing, cohorts, and merchandising decisions."),
    role("HR Generalist", "People", "CEO", 3, 0.03, 82000, "Supports scale-up hiring and people processes."),
    role("Warehouse Lead", "Operations", "Operations Manager", 3, 0.12, 72000, "Owns fulfillment team coordination and throughput."),
)


MANUFACTURING_ROLES = (
    role("CEO", "Executive", None, 1, 0.03, 200000, "Owns strategy, industrial partnerships, and capital planning."),
    role("Plant Manager", "Operations", "CEO", 1, 0.07, 145000, "Runs plant throughput, safety, and production cadence."),
    role("Manufacturing Engineer", "Engineering", "Plant Manager", 1, 0.11, 120000, "Improves process yield, reliability, and line efficiency."),
    role("Quality Manager", "Quality", "Plant Manager", 1, 0.07, 118000, "Protects output consistency and audit readiness.", 0.08),
    role("Procurement Manager", "Supply Chain", "CEO", 1, 0.06, 115000, "Secures materials and supplier continuity."),
    role("Finance Manager", "Finance", "CEO", 1, 0.04, 110000, "Keeps cost accounting and cash controls sharp."),
    role("Production Supervisor", "Operations", "Plant Manager", 2, 0.10, 92000, "Translates the plan into shift-level execution."),
    role("Maintenance Engineer", "Engineering", "Plant Manager", 2, 0.08, 102000, "Reduces downtime and improves equipment uptime.", 0.08),
    role("Warehouse Lead", "Operations", "Plant Manager", 2, 0.09, 78000, "Coordinates inbound materials and outbound shipments."),
    role("Sales Manager", "Sales", "CEO", 2, 0.05, 130000, "Builds commercial demand and channel mix."),
    role("Account Manager", "Sales", "Sales Manager", 2, 0.06, 98000, "Supports repeat orders and customer retention."),
    role("HR Generalist", "People", "CEO", 3, 0.03, 85000, "Supports recruiting and workforce administration."),
    role("Supply Chain Analyst", "Supply Chain", "Procurement Manager", 3, 0.05, 90000, "Improves planning accuracy and supplier performance."),
    role("Safety Manager", "Operations", "Plant Manager", 3, 0.03, 102000, "Protects worker safety and regulatory compliance.", 0.10),
    role("Process Technician", "Operations", "Production Supervisor", 3, 0.13, 70000, "Keeps production moving with predictable line support."),
)


CONSULTING_ROLES = (
    role("CEO", "Executive", None, 1, 0.04, 185000, "Owns demand generation, positioning, and executive relationships."),
    role("Practice Director", "Delivery", "CEO", 1, 0.08, 165000, "Leads service quality and account delivery."),
    role("Principal Consultant", "Delivery", "Practice Director", 1, 0.16, 145000, "Handles complex client work and proposal leadership."),
    role("Consultant", "Delivery", "Practice Director", 1, 0.28, 108000, "Carries billable delivery capacity and analysis."),
    role("Business Development Manager", "Sales", "CEO", 1, 0.08, 130000, "Builds pipeline and translates needs into proposals."),
    role("Finance Manager", "Finance", "CEO", 1, 0.05, 102000, "Tracks utilization, margin, and reporting."),
    role("Operations Manager", "Operations", "CEO", 2, 0.05, 98000, "Keeps staffing, utilization, and internal cadence organized."),
    role("Recruiter", "People", "CEO", 2, 0.05, 92000, "Maintains bench strength and speed-to-hire."),
    role("Marketing Manager", "Marketing", "CEO", 2, 0.04, 98000, "Supports thought leadership and demand creation."),
    role("Customer Success Manager", "Customer Success", "Practice Director", 2, 0.05, 98000, "Improves renewals and expansion within existing accounts."),
    role("Data Analyst", "Delivery", "Practice Director", 3, 0.04, 96000, "Strengthens analytics-heavy engagements."),
    role("HR Generalist", "People", "CEO", 3, 0.03, 82000, "Adds process as the team becomes multi-layered."),
)


INDUSTRY_ALIASES = {
    "saas": "saas",
    "software": "saas",
    "b2b software": "saas",
    "tech": "saas",
    "fintech": "fintech",
    "healthtech": "healthtech",
    "health care": "healthtech",
    "healthcare": "healthtech",
    "ecommerce": "ecommerce",
    "e-commerce": "ecommerce",
    "retail": "ecommerce",
    "manufacturing": "manufacturing",
    "factory": "manufacturing",
    "consulting": "consulting",
    "services": "consulting",
}


INDUSTRIES = {
    "saas": IndustryProfile(
        name="B2B SaaS",
        narrative="Product-led software company with recurring revenue and strong gross margins.",
        salary_multiplier=1.00,
        gross_margin=0.82,
        revenue_per_head=220000,
        revenue_ramp=(0.18, 0.42, 0.78, 1.08, 1.35),
        headcount_plan=(6, 12, 24, 40, 60),
        tools_per_employee=5500,
        facility_per_employee=6500,
        compliance_per_employee=1800,
        capex_plan=(65000, 45000, 35000, 28000, 24000),
        sales_marketing_ratio=0.18,
        roles=SAAS_ROLES,
    ),
    "fintech": IndustryProfile(
        name="Fintech",
        narrative="Regulated financial product with higher controls, security needs, and partnership complexity.",
        salary_multiplier=1.08,
        gross_margin=0.76,
        revenue_per_head=235000,
        revenue_ramp=(0.16, 0.38, 0.70, 0.98, 1.22),
        headcount_plan=(6, 14, 28, 46, 72),
        tools_per_employee=6500,
        facility_per_employee=7200,
        compliance_per_employee=5200,
        capex_plan=(85000, 65000, 52000, 42000, 35000),
        sales_marketing_ratio=0.16,
        roles=FINTECH_ROLES,
    ),
    "healthtech": IndustryProfile(
        name="Healthtech",
        narrative="Healthcare-focused company balancing product delivery with patient, provider, and compliance demands.",
        salary_multiplier=1.03,
        gross_margin=0.71,
        revenue_per_head=210000,
        revenue_ramp=(0.18, 0.40, 0.66, 0.92, 1.18),
        headcount_plan=(6, 14, 26, 42, 64),
        tools_per_employee=5200,
        facility_per_employee=7000,
        compliance_per_employee=4800,
        capex_plan=(78000, 56000, 44000, 36000, 30000),
        sales_marketing_ratio=0.15,
        roles=HEALTHTECH_ROLES,
    ),
    "ecommerce": IndustryProfile(
        name="E-commerce",
        narrative="Digitally enabled commerce business with heavier operations, inventory, and marketing intensity.",
        salary_multiplier=0.95,
        gross_margin=0.52,
        revenue_per_head=300000,
        revenue_ramp=(0.22, 0.52, 0.84, 1.04, 1.18),
        headcount_plan=(6, 12, 26, 48, 80),
        tools_per_employee=3500,
        facility_per_employee=8200,
        compliance_per_employee=1200,
        capex_plan=(110000, 90000, 70000, 60000, 55000),
        sales_marketing_ratio=0.22,
        roles=ECOMMERCE_ROLES,
    ),
    "manufacturing": IndustryProfile(
        name="Manufacturing",
        narrative="Production-oriented company with higher facility, quality, and capital needs.",
        salary_multiplier=0.97,
        gross_margin=0.38,
        revenue_per_head=260000,
        revenue_ramp=(0.28, 0.52, 0.78, 0.96, 1.08),
        headcount_plan=(6, 12, 24, 50, 96),
        tools_per_employee=2800,
        facility_per_employee=12500,
        compliance_per_employee=2800,
        capex_plan=(320000, 240000, 180000, 155000, 130000),
        sales_marketing_ratio=0.10,
        roles=MANUFACTURING_ROLES,
    ),
    "consulting": IndustryProfile(
        name="Consulting",
        narrative="Services-led firm where revenue scales with billable talent and client relationships.",
        salary_multiplier=0.92,
        gross_margin=0.64,
        revenue_per_head=190000,
        revenue_ramp=(0.35, 0.70, 0.96, 1.12, 1.22),
        headcount_plan=(6, 10, 18, 28, 40),
        tools_per_employee=3000,
        facility_per_employee=5000,
        compliance_per_employee=1000,
        capex_plan=(35000, 24000, 18000, 16000, 15000),
        sales_marketing_ratio=0.12,
        roles=CONSULTING_ROLES,
    ),
}


LEANNESS_ALIASES = {
    "lean": "lean",
    "leanest": "lean",
    "balanced": "balanced",
    "standard": "balanced",
    "aggressive": "aggressive",
    "growth": "aggressive",
}


LEANNESS = {
    "lean": LeannessProfile(
        name="Lean",
        description="Keeps the team compact, expects broader role scope, and reduces non-essential spend.",
        headcount_multiplier=0.76,
        salary_multiplier=1.05,
        band_spread_delta=0.04,
        revenue_multiplier=0.94,
        tools_multiplier=0.92,
        facilities_multiplier=0.84,
        compliance_multiplier=0.94,
        sales_marketing_multiplier=0.82,
        general_admin_multiplier=0.88,
        capex_multiplier=0.84,
        funding_buffer_multiplier=0.92,
    ),
    "balanced": LeannessProfile(
        name="Balanced",
        description="Maintains a practical mix of efficiency and growth, with a conventional scale-up pace.",
        headcount_multiplier=1.00,
        salary_multiplier=1.00,
        band_spread_delta=0.00,
        revenue_multiplier=1.00,
        tools_multiplier=1.00,
        facilities_multiplier=1.00,
        compliance_multiplier=1.00,
        sales_marketing_multiplier=1.00,
        general_admin_multiplier=1.00,
        capex_multiplier=1.00,
        funding_buffer_multiplier=1.00,
    ),
    "aggressive": LeannessProfile(
        name="Aggressive Growth",
        description="Adds headcount earlier, invests more heavily in expansion, and accepts higher near-term burn.",
        headcount_multiplier=1.24,
        salary_multiplier=0.98,
        band_spread_delta=-0.02,
        revenue_multiplier=1.08,
        tools_multiplier=1.08,
        facilities_multiplier=1.14,
        compliance_multiplier=1.08,
        sales_marketing_multiplier=1.18,
        general_admin_multiplier=1.10,
        capex_multiplier=1.16,
        funding_buffer_multiplier=1.08,
    ),
}


INDUSTRY_OPTIONS = tuple(
    {"value": key, "label": profile.name}
    for key, profile in INDUSTRIES.items()
)
COUNTRY_OPTIONS = tuple(
    {"value": key, "label": profile.name}
    for key, profile in COUNTRIES.items()
    if key != "default"
)
LEANNESS_OPTIONS = tuple(
    {"value": key, "label": profile.name, "description": profile.description}
    for key, profile in LEANNESS.items()
)


def normalize_key(value: str) -> str:
    lowered = value.strip().lower()
    lowered = re.sub(r"[^a-z0-9\s-]", "", lowered)
    lowered = re.sub(r"\s+", " ", lowered)
    return lowered


def resolve_country(country: str) -> tuple[str, CountryProfile]:
    key = normalize_key(country)
    key = COUNTRY_ALIASES.get(key, key)
    if key in COUNTRIES:
        return key, COUNTRIES[key]

    for known, profile in COUNTRIES.items():
        if known != "default" and known in key:
            return known, profile

    return "default", COUNTRIES["default"]


def resolve_industry(industry: str) -> tuple[str, IndustryProfile]:
    key = normalize_key(industry)
    key = INDUSTRY_ALIASES.get(key, key)
    if key in INDUSTRIES:
        return key, INDUSTRIES[key]

    for known, profile in INDUSTRIES.items():
        if known in key or profile.name.lower() in key:
            return known, profile

    return "saas", INDUSTRIES["saas"]


def resolve_leanness(leanness: str) -> tuple[str, LeannessProfile]:
    key = normalize_key(leanness)
    key = LEANNESS_ALIASES.get(key, key)
    if key in LEANNESS:
        return key, LEANNESS[key]

    return "balanced", LEANNESS["balanced"]


def round_money(value: float) -> int:
    return int(round(value / 1000.0) * 1000)


def round_local_money(value: float, country_profile: CountryProfile) -> int:
    step = max(country_profile.local_rounding, 1)
    return int(round(value / step) * step)


def convert_to_local(amount_usd: int, country_profile: CountryProfile) -> int:
    return round_local_money(amount_usd * country_profile.usd_to_local, country_profile)


def allocate_role_counts(roles: tuple[RoleTemplate, ...], total_headcount: int, year: int) -> dict[str, int]:
    active_roles = [entry for entry in roles if entry.start_year <= year]
    counts = {entry.title: 1 for entry in active_roles}
    remaining = total_headcount - len(active_roles)

    if remaining < 0:
        active_roles = active_roles[:total_headcount]
        return {entry.title: 1 for entry in active_roles}

    while remaining > 0:
        best_role = max(
            active_roles,
            key=lambda entry: (total_headcount * entry.share) - counts[entry.title],
        )
        counts[best_role.title] += 1
        remaining -= 1

    return counts


def salary_position_modifier(
    role_template: RoleTemplate,
    count_for_role: int,
    index: int,
    leanness_profile: LeannessProfile,
) -> tuple[float, str]:
    band_spread = max(0.04, role_template.band_spread + leanness_profile.band_spread_delta)
    if count_for_role == 1:
        return 1.03, "set slightly above the midpoint because this is the first seat carrying broad scope"

    fraction = index / max(count_for_role - 1, 1)
    modifier = 1.0 + (band_spread / 2.0) - (band_spread * fraction)
    modifier = max(0.90, min(1.12, modifier))

    if modifier >= 1.04:
        return modifier, "includes an early-core-team premium because the person is expected to operate with wider scope"
    if modifier <= 0.96:
        return modifier, "sits lower in the band because it represents a later-stage hire in a more structured team"
    return modifier, "sits near the middle of the band for a market-rate hire at this stage"


def salary_reason(
    role_template: RoleTemplate,
    country_profile: CountryProfile,
    industry_profile: IndustryProfile,
    leanness_profile: LeannessProfile,
    band_reason: str,
) -> str:
    parts = [
        role_template.rationale,
        f"The estimate is adjusted to the {country_profile.name} labor market and shown in {country_profile.currency_code}.",
        f"The {leanness_profile.name.lower()} operating model influences the expected scope for this seat.",
        band_reason + ".",
    ]

    if role_template.scarcity_premium >= 0.10:
        parts.append(
            f"A scarcity premium is included because this capability is especially hard to replace in {industry_profile.name}."
        )

    return " ".join(parts)


def build_employees(
    role_counts: dict[str, int],
    roles: tuple[RoleTemplate, ...],
    country_profile: CountryProfile,
    industry_profile: IndustryProfile,
    leanness_profile: LeannessProfile,
    year: int,
) -> list[dict[str, Any]]:
    templates = {entry.title: entry for entry in roles}
    employees: list[dict[str, Any]] = []
    market_drift = 1.0 + ((year - 1) * 0.035)

    for title, count in role_counts.items():
        template = templates[title]
        for index in range(count):
            modifier, band_reason = salary_position_modifier(template, count, index, leanness_profile)
            salary = template.base_salary
            salary *= country_profile.labor_multiplier
            salary *= industry_profile.salary_multiplier
            salary *= leanness_profile.salary_multiplier
            salary *= 1.0 + template.scarcity_premium
            salary *= market_drift
            salary *= modifier
            final_salary_usd = round_money(salary)
            final_salary_local = convert_to_local(final_salary_usd, country_profile)
            employee_label = title if count == 1 else f"{title} {index + 1}"

            employees.append(
                {
                    "name": employee_label,
                    "title": title,
                    "department": template.department,
                    "reports_to": template.reports_to or "Board",
                    "salary_usd": final_salary_usd,
                    "salary_local": final_salary_local,
                    "salary_reason": salary_reason(
                        role_template=template,
                        country_profile=country_profile,
                        industry_profile=industry_profile,
                        leanness_profile=leanness_profile,
                        band_reason=band_reason,
                    ),
                }
            )

    employees.sort(key=lambda item: (-item["salary_usd"], item["department"], item["title"], item["name"]))
    return employees


def build_org_structure(role_counts: dict[str, int], roles: tuple[RoleTemplate, ...]) -> list[dict[str, Any]]:
    templates = {entry.title: entry for entry in roles}
    direct_reports: dict[str, list[str]] = {}

    for title, count in role_counts.items():
        template = templates[title]
        if template.reports_to and template.reports_to in role_counts:
            report_label = f"{title} x{count}" if count > 1 else title
            direct_reports.setdefault(template.reports_to, []).append(report_label)

    leaders = []
    for title, count in role_counts.items():
        template = templates[title]
        if template.reports_to is None or template.reports_to not in role_counts:
            leaders.append(
                {
                    "leader": title,
                    "department": template.department,
                    "count": count,
                    "reports": sorted(direct_reports.get(title, [])),
                }
            )

    secondary_leaders = []
    for title, count in role_counts.items():
        if title in {entry["leader"] for entry in leaders}:
            continue
        if title in direct_reports:
            template = templates[title]
            secondary_leaders.append(
                {
                    "leader": title,
                    "department": template.department,
                    "count": count,
                    "reports": sorted(direct_reports.get(title, [])),
                }
            )

    return leaders + secondary_leaders


def build_year_plan(
    year: int,
    industry_profile: IndustryProfile,
    country_profile: CountryProfile,
    leanness_profile: LeannessProfile,
) -> dict[str, Any]:
    headcount = max(1, int(round(industry_profile.headcount_plan[year - 1] * leanness_profile.headcount_multiplier)))
    role_counts = allocate_role_counts(industry_profile.roles, headcount, year)
    employees = build_employees(
        role_counts,
        industry_profile.roles,
        country_profile,
        industry_profile,
        leanness_profile,
        year,
    )

    payroll = sum(item["salary_usd"] for item in employees)
    revenue = round_money(
        headcount
        * industry_profile.revenue_per_head
        * industry_profile.revenue_ramp[year - 1]
        * country_profile.market_multiplier
        * leanness_profile.revenue_multiplier
    )
    employer_cost = round_money(payroll * country_profile.employer_oncost)
    tooling_cost = round_money(headcount * industry_profile.tools_per_employee * leanness_profile.tools_multiplier)
    facilities_cost = round_money(
        headcount
        * industry_profile.facility_per_employee
        * country_profile.facility_multiplier
        * leanness_profile.facilities_multiplier
    )
    compliance_cost = round_money(
        headcount * industry_profile.compliance_per_employee * leanness_profile.compliance_multiplier
    )
    sales_marketing_cost = round_money(
        revenue * industry_profile.sales_marketing_ratio * leanness_profile.sales_marketing_multiplier
    )
    general_admin_cost = round_money(
        ((headcount * 2800) + (45000 * year)) * leanness_profile.general_admin_multiplier
    )
    operating_costs = (
        payroll
        + employer_cost
        + tooling_cost
        + facilities_cost
        + compliance_cost
        + sales_marketing_cost
        + general_admin_cost
    )
    capex = round_money(
        industry_profile.capex_plan[year - 1]
        * country_profile.facility_multiplier
        * leanness_profile.capex_multiplier
    )
    gross_profit = round_money(revenue * industry_profile.gross_margin)
    funding_required = round_money(
        max(
            0,
            (operating_costs + capex - gross_profit)
            * country_profile.funding_buffer
            * leanness_profile.funding_buffer_multiplier,
        )
    )

    department_headcount: dict[str, int] = {}
    for employee in employees:
        department_headcount[employee["department"]] = department_headcount.get(employee["department"], 0) + 1

    return {
        "year": year,
        "headcount": headcount,
        "headcount_by_department": dict(sorted(department_headcount.items())),
        "revenue_usd": revenue,
        "revenue_local": convert_to_local(revenue, country_profile),
        "gross_profit_usd": gross_profit,
        "gross_profit_local": convert_to_local(gross_profit, country_profile),
        "operating_costs_usd": operating_costs,
        "operating_costs_local": convert_to_local(operating_costs, country_profile),
        "funding_required_usd": funding_required,
        "funding_required_local": convert_to_local(funding_required, country_profile),
        "cost_breakdown": {
            "payroll_usd": payroll,
            "payroll_local": convert_to_local(payroll, country_profile),
            "employer_costs_usd": employer_cost,
            "employer_costs_local": convert_to_local(employer_cost, country_profile),
            "tooling_usd": tooling_cost,
            "tooling_local": convert_to_local(tooling_cost, country_profile),
            "facilities_usd": facilities_cost,
            "facilities_local": convert_to_local(facilities_cost, country_profile),
            "compliance_usd": compliance_cost,
            "compliance_local": convert_to_local(compliance_cost, country_profile),
            "sales_marketing_usd": sales_marketing_cost,
            "sales_marketing_local": convert_to_local(sales_marketing_cost, country_profile),
            "general_admin_usd": general_admin_cost,
            "general_admin_local": convert_to_local(general_admin_cost, country_profile),
            "capex_usd": capex,
            "capex_local": convert_to_local(capex, country_profile),
        },
        "org_structure": build_org_structure(role_counts, industry_profile.roles),
        "employees": employees,
    }


def build_key_takeaways(
    industry_profile: IndustryProfile,
    country_profile: CountryProfile,
    leanness_profile: LeannessProfile,
    yearly_plan: list[dict[str, Any]],
) -> list[str]:
    first_year = yearly_plan[0]
    last_year = yearly_plan[-1]
    total_funding = sum(year["funding_required_usd"] for year in yearly_plan)

    return [
        f"{industry_profile.name} in {country_profile.name} on a {leanness_profile.name.lower()} plan starts with {first_year['headcount']} people and reaches {last_year['headcount']} people by year {YEARS}.",
        f"Year {YEARS} revenue is projected at about {country_profile.currency_code} {last_year['revenue_local']:,} with operating costs near {country_profile.currency_code} {last_year['operating_costs_local']:,}.",
        f"Total external funding required across the first {YEARS} years is estimated at about {country_profile.currency_code} {sum(year['funding_required_local'] for year in yearly_plan):,}.",
    ]


def generate_company_plan(industry: str, country: str, leanness: str = "balanced") -> dict[str, Any]:
    resolved_industry_key, industry_profile = resolve_industry(industry)
    resolved_country_key, country_profile = resolve_country(country)
    resolved_leanness_key, leanness_profile = resolve_leanness(leanness)

    yearly_plan = [
        build_year_plan(year, industry_profile, country_profile, leanness_profile)
        for year in range(1, YEARS + 1)
    ]
    cumulative_funding = 0
    for year in yearly_plan:
        cumulative_funding += year["funding_required_usd"]
        year["cumulative_funding_usd"] = cumulative_funding
        year["cumulative_funding_local"] = convert_to_local(cumulative_funding, country_profile)

    return {
        "inputs": {
            "industry": industry,
            "country": country,
            "leanness": leanness,
        },
        "matched_profiles": {
            "industry_key": resolved_industry_key,
            "industry_name": industry_profile.name,
            "country_key": resolved_country_key,
            "country_name": country_profile.name,
            "currency_code": country_profile.currency_code,
            "currency_locale": country_profile.currency_locale,
            "leanness_key": resolved_leanness_key,
            "leanness_name": leanness_profile.name,
        },
        "assumptions": [
            "Local-currency values are derived from fixed planning exchange-rate assumptions rather than live FX quotes.",
            "All figures are annual planning estimates for scenario design, not payroll advice or investor guidance.",
            "The model assumes a five-year company build with hiring layered in as capability needs appear.",
            "Funding need is calculated as operating burn plus capital expense not covered by gross profit, with a small execution buffer.",
        ],
        "narrative": industry_profile.narrative,
        "key_takeaways": build_key_takeaways(industry_profile, country_profile, leanness_profile, yearly_plan),
        "yearly_plan": yearly_plan,
    }
