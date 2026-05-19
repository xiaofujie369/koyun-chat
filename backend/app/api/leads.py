from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_workspace
from app.models.lead import Lead
from app.models.site import Site
from app.models.workspace import Workspace
from app.schemas.lead import LeadRead, LeadUpdate

router = APIRouter()


@router.get("", response_model=list[LeadRead])
def list_leads(
    site_id: UUID | None = None,
    status: str | None = None,
    workspace: Workspace = Depends(get_current_workspace),
    db: Session = Depends(get_db),
) -> list[Lead]:
    query = select(Lead).join(Site).where(Site.workspace_id == workspace.id)
    if site_id:
        query = query.where(Lead.site_id == site_id)
    if status:
        query = query.where(Lead.status == status)
    return list(db.scalars(query.order_by(Lead.created_at.desc()).limit(200)).all())


@router.get("/{lead_id}", response_model=LeadRead)
def get_lead(
    lead_id: UUID,
    workspace: Workspace = Depends(get_current_workspace),
    db: Session = Depends(get_db),
) -> Lead:
    lead = db.scalar(select(Lead).join(Site).where(Lead.id == lead_id, Site.workspace_id == workspace.id))
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead


@router.put("/{lead_id}", response_model=LeadRead)
def update_lead(
    lead_id: UUID,
    payload: LeadUpdate,
    workspace: Workspace = Depends(get_current_workspace),
    db: Session = Depends(get_db),
) -> Lead:
    lead = db.scalar(select(Lead).join(Site).where(Lead.id == lead_id, Site.workspace_id == workspace.id))
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(lead, key, value)
    db.commit()
    return lead
