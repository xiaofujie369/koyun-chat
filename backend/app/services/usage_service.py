from datetime import datetime, timezone
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.plan import Plan
from app.models.site import Site
from app.models.subscription import Subscription
from app.models.usage import UsageRecord
from app.models.workspace import Workspace, WorkspaceMember


def current_period() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m")


def increment_usage(
    db: Session,
    workspace_id: UUID,
    usage_type: str,
    site_id: UUID | None = None,
    count: int = 1,
) -> UsageRecord:
    record = UsageRecord(
        workspace_id=workspace_id,
        site_id=site_id,
        usage_type=usage_type,
        count=count,
        period=current_period(),
    )
    db.add(record)
    db.flush()
    return record


def get_workspace_plan(db: Session, workspace: Workspace) -> Plan | None:
    if workspace.plan:
        return workspace.plan
    subscription = db.scalar(
        select(Subscription)
        .where(Subscription.workspace_id == workspace.id)
        .order_by(Subscription.created_at.desc())
    )
    return subscription.plan if subscription else None


def get_usage_total(db: Session, workspace_id: UUID, usage_type: str, period: str | None = None) -> int:
    total = db.scalar(
        select(func.coalesce(func.sum(UsageRecord.count), 0)).where(
            UsageRecord.workspace_id == workspace_id,
            UsageRecord.usage_type == usage_type,
            UsageRecord.period == (period or current_period()),
        )
    )
    return int(total or 0)


def assert_can_create_site(db: Session, workspace: Workspace) -> None:
    plan = get_workspace_plan(db, workspace)
    if not plan or plan.max_sites is None:
        return
    site_count = db.scalar(select(func.count(Site.id)).where(Site.workspace_id == workspace.id))
    if int(site_count or 0) >= plan.max_sites:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="Current plan site limit reached",
        )


def assert_can_add_agent(db: Session, workspace: Workspace) -> None:
    plan = get_workspace_plan(db, workspace)
    if not plan or plan.max_agents is None:
        return
    agent_count = db.scalar(select(func.count(WorkspaceMember.id)).where(WorkspaceMember.workspace_id == workspace.id))
    if int(agent_count or 0) >= plan.max_agents:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="Current plan agent limit reached",
        )


def assert_can_use_ai(db: Session, workspace: Workspace) -> None:
    plan = get_workspace_plan(db, workspace)
    if not plan or plan.max_ai_messages_monthly is None:
        return
    used = get_usage_total(db, workspace.id, "ai_message")
    if used >= plan.max_ai_messages_monthly:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="Current plan AI message limit reached",
        )


def assert_can_track_visitor(db: Session, workspace: Workspace) -> None:
    plan = get_workspace_plan(db, workspace)
    if not plan or plan.max_visitors_monthly is None:
        return
    used = get_usage_total(db, workspace.id, "visitor")
    if used >= plan.max_visitors_monthly:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="Current plan visitor limit reached",
        )
