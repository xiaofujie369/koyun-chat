from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_workspace
from app.models.site import Site
from app.models.visitor import Visitor
from app.models.workspace import Workspace
from app.schemas.visitor import VisitorRead

router = APIRouter()


def workspace_site_ids(db: Session, workspace: Workspace) -> list[UUID]:
    return list(db.scalars(select(Site.id).where(Site.workspace_id == workspace.id)).all())


@router.get("", response_model=list[VisitorRead])
def list_visitors(
    site_id: UUID | None = None,
    workspace: Workspace = Depends(get_current_workspace),
    db: Session = Depends(get_db),
) -> list[Visitor]:
    query = select(Visitor).join(Site).where(Site.workspace_id == workspace.id)
    if site_id:
        query = query.where(Visitor.site_id == site_id)
    return list(db.scalars(query.order_by(Visitor.last_seen_at.desc()).limit(200)).all())


@router.get("/online", response_model=list[VisitorRead])
def online_visitors(
    workspace: Workspace = Depends(get_current_workspace),
    db: Session = Depends(get_db),
) -> list[Visitor]:
    return list(
        db.scalars(
            select(Visitor)
            .join(Site)
            .where(Site.workspace_id == workspace.id, Visitor.is_online.is_(True))
            .order_by(Visitor.last_seen_at.desc())
        ).all()
    )


@router.get("/{visitor_id}", response_model=VisitorRead)
def get_visitor(
    visitor_id: UUID,
    workspace: Workspace = Depends(get_current_workspace),
    db: Session = Depends(get_db),
) -> Visitor:
    visitor = db.scalar(select(Visitor).join(Site).where(Visitor.id == visitor_id, Site.workspace_id == workspace.id))
    if not visitor:
        raise HTTPException(status_code=404, detail="Visitor not found")
    return visitor
