from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_workspace
from app.models.knowledge import KnowledgeBase
from app.models.site import Site
from app.models.workspace import Workspace
from app.schemas.knowledge import KnowledgeCreate, KnowledgeRead, KnowledgeUpdate

router = APIRouter()


def ensure_site_scope(db: Session, workspace: Workspace, site_id: UUID) -> Site:
    site = db.scalar(select(Site).where(Site.id == site_id, Site.workspace_id == workspace.id))
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    return site


@router.get("", response_model=list[KnowledgeRead])
def list_knowledge(
    site_id: UUID | None = None,
    workspace: Workspace = Depends(get_current_workspace),
    db: Session = Depends(get_db),
) -> list[KnowledgeBase]:
    query = select(KnowledgeBase).join(Site).where(Site.workspace_id == workspace.id)
    if site_id:
        query = query.where(KnowledgeBase.site_id == site_id)
    return list(db.scalars(query.order_by(KnowledgeBase.updated_at.desc())).all())


@router.post("", response_model=KnowledgeRead, status_code=status.HTTP_201_CREATED)
def create_knowledge(
    payload: KnowledgeCreate,
    workspace: Workspace = Depends(get_current_workspace),
    db: Session = Depends(get_db),
) -> KnowledgeBase:
    ensure_site_scope(db, workspace, payload.site_id)
    entry = KnowledgeBase(**payload.model_dump())
    db.add(entry)
    db.commit()
    return entry


@router.put("/{knowledge_id}", response_model=KnowledgeRead)
def update_knowledge(
    knowledge_id: UUID,
    payload: KnowledgeUpdate,
    workspace: Workspace = Depends(get_current_workspace),
    db: Session = Depends(get_db),
) -> KnowledgeBase:
    entry = db.scalar(
        select(KnowledgeBase).join(Site).where(KnowledgeBase.id == knowledge_id, Site.workspace_id == workspace.id)
    )
    if not entry:
        raise HTTPException(status_code=404, detail="Knowledge entry not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(entry, key, value)
    db.commit()
    return entry


@router.delete("/{knowledge_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_knowledge(
    knowledge_id: UUID,
    workspace: Workspace = Depends(get_current_workspace),
    db: Session = Depends(get_db),
) -> None:
    entry = db.scalar(
        select(KnowledgeBase).join(Site).where(KnowledgeBase.id == knowledge_id, Site.workspace_id == workspace.id)
    )
    if not entry:
        raise HTTPException(status_code=404, detail="Knowledge entry not found")
    db.delete(entry)
    db.commit()
