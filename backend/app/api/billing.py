from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_workspace
from app.models.plan import Plan
from app.models.subscription import Subscription
from app.models.workspace import Workspace
from app.schemas.billing import CheckoutRequest, CheckoutResponse, PlanRead, SubscriptionRead
from app.services.billing_service import ensure_default_plans

router = APIRouter()


@router.get("/plans", response_model=list[PlanRead])
def list_plans(db: Session = Depends(get_db)) -> list[Plan]:
    ensure_default_plans(db)
    db.commit()
    return list(db.scalars(select(Plan).order_by(Plan.price_monthly.asc().nullslast())).all())


@router.get("/subscription", response_model=SubscriptionRead | None)
def get_subscription(
    workspace: Workspace = Depends(get_current_workspace),
    db: Session = Depends(get_db),
) -> Subscription | None:
    return db.scalar(
        select(Subscription)
        .where(Subscription.workspace_id == workspace.id)
        .order_by(Subscription.created_at.desc())
    )


@router.post("/checkout", response_model=CheckoutResponse)
def create_checkout(payload: CheckoutRequest) -> CheckoutResponse:
    return CheckoutResponse(
        checkout_url=None,
        message=f"Checkout for {payload.plan_name} is not connected yet. Configure Stripe or EasyPay first.",
    )


@router.post("/webhook")
def billing_webhook() -> dict[str, str]:
    return {"message": "webhook received"}
