from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class PlanRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    price_monthly: Decimal | None = None
    max_sites: int | None = None
    max_agents: int | None = None
    max_ai_messages_monthly: int | None = None
    max_visitors_monthly: int | None = None
    allow_remove_branding: bool
    allow_custom_color: bool
    allow_email_notification: bool
    allow_private_deploy: bool


class SubscriptionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    workspace_id: UUID
    plan_id: UUID
    status: str
    provider: str | None = None
    provider_subscription_id: str | None = None
    current_period_start: datetime | None = None
    current_period_end: datetime | None = None
    created_at: datetime
    updated_at: datetime


class CheckoutRequest(BaseModel):
    plan_name: str


class CheckoutResponse(BaseModel):
    checkout_url: str | None = None
    message: str
