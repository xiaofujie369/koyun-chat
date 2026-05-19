"""initial schema

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-05-20
"""

from decimal import Decimal
from uuid import UUID

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from app.models import Base

revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


PLAN_IDS = {
    "Trial": UUID("00000000-0000-4000-8000-000000000001"),
    "Basic": UUID("00000000-0000-4000-8000-000000000002"),
    "Pro": UUID("00000000-0000-4000-8000-000000000003"),
    "Business": UUID("00000000-0000-4000-8000-000000000004"),
    "Private": UUID("00000000-0000-4000-8000-000000000005"),
}


def upgrade() -> None:
    bind = op.get_bind()
    Base.metadata.create_all(bind=bind)

    plans = sa.table(
        "plans",
        sa.column("id", postgresql.UUID(as_uuid=True)),
        sa.column("name", sa.String),
        sa.column("price_monthly", sa.Numeric),
        sa.column("max_sites", sa.Integer),
        sa.column("max_agents", sa.Integer),
        sa.column("max_ai_messages_monthly", sa.Integer),
        sa.column("max_visitors_monthly", sa.Integer),
        sa.column("allow_remove_branding", sa.Boolean),
        sa.column("allow_custom_color", sa.Boolean),
        sa.column("allow_email_notification", sa.Boolean),
        sa.column("allow_private_deploy", sa.Boolean),
    )
    op.bulk_insert(
        plans,
        [
            {
                "id": PLAN_IDS["Trial"],
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
                "id": PLAN_IDS["Basic"],
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
                "id": PLAN_IDS["Pro"],
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
                "id": PLAN_IDS["Business"],
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
                "id": PLAN_IDS["Private"],
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
        ],
    )


def downgrade() -> None:
    bind = op.get_bind()
    Base.metadata.drop_all(bind=bind)
