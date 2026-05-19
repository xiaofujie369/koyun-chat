from datetime import datetime, timedelta, timezone
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.plan import Plan
from app.models.subscription import Subscription
from app.models.workspace import Workspace

DEFAULT_PLANS = [
    {
        "name": "Trial",
        "price_monthly": Decimal("0.00"),
        "max_sites": 1,
        "max_agents": 1,
        "max_ai_messages_monthly": 100,
        "max_visitors_monthly": 1000,
        "allow_remove_branding": False,
        "allow_custom_color": False,
        "allow_email_notification": False,
        "allow_private_deploy": False,
    },
    {
        "name": "Basic",
        "price_monthly": Decimal("9.90"),
        "max_sites": 1,
        "max_agents": 1,
        "max_ai_messages_monthly": 1000,
        "max_visitors_monthly": 5000,
        "allow_remove_branding": False,
        "allow_custom_color": False,
        "allow_email_notification": True,
        "allow_private_deploy": False,
    },
    {
        "name": "Pro",
        "price_monthly": Decimal("19.90"),
        "max_sites": 3,
        "max_agents": 3,
        "max_ai_messages_monthly": 5000,
        "max_visitors_monthly": 20000,
        "allow_remove_branding": False,
        "allow_custom_color": True,
        "allow_email_notification": True,
        "allow_private_deploy": False,
    },
    {
        "name": "Business",
        "price_monthly": Decimal("49.00"),
        "max_sites": 10,
        "max_agents": 10,
        "max_ai_messages_monthly": 20000,
        "max_visitors_monthly": 100000,
        "allow_remove_branding": True,
        "allow_custom_color": True,
        "allow_email_notification": True,
        "allow_private_deploy": False,
    },
    {
        "name": "Private",
        "price_monthly": None,
        "max_sites": None,
        "max_agents": None,
        "max_ai_messages_monthly": None,
        "max_visitors_monthly": None,
        "allow_remove_branding": True,
        "allow_custom_color": True,
        "allow_email_notification": True,
        "allow_private_deploy": True,
    },
]


def ensure_default_plans(db: Session) -> None:
    existing_names = set(db.scalars(select(Plan.name)).all())
    for plan_data in DEFAULT_PLANS:
        if plan_data["name"] not in existing_names:
            db.add(Plan(**plan_data))
    db.flush()


def get_trial_plan(db: Session) -> Plan:
    ensure_default_plans(db)
    plan = db.scalar(select(Plan).where(Plan.name == "Trial"))
    if not plan:
        raise RuntimeError("Trial plan is missing")
    return plan


def create_trial_subscription(db: Session, workspace: Workspace) -> Subscription:
    trial = get_trial_plan(db)
    workspace.plan_id = trial.id
    now = datetime.now(timezone.utc)
    subscription = Subscription(
        workspace_id=workspace.id,
        plan_id=trial.id,
        status="trial",
        provider="manual",
        current_period_start=now,
        current_period_end=now + timedelta(days=7),
    )
    db.add(subscription)
    db.flush()
    return subscription
