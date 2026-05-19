import secrets
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.deps import get_current_workspace
from app.models.site import Site
from app.models.workspace import Workspace
from app.schemas.site import EmbedCodeResponse, SiteCreate, SiteRead, SiteUpdate
from app.services.usage_service import assert_can_create_site

router = APIRouter()


def generate_site_key(db: Session) -> str:
    for _ in range(20):
        site_key = f"site_{secrets.token_urlsafe(8).replace('-', '').replace('_', '')[:10]}"
        if not db.scalar(select(Site).where(Site.site_key == site_key)):
            return site_key
    raise RuntimeError("Unable to generate unique site key")


@router.get("", response_model=list[SiteRead])
def list_sites(
    workspace: Workspace = Depends(get_current_workspace),
    db: Session = Depends(get_db),
) -> list[Site]:
    return list(db.scalars(select(Site).where(Site.workspace_id == workspace.id).order_by(Site.created_at.desc())).all())


@router.post("", response_model=SiteRead, status_code=status.HTTP_201_CREATED)
def create_site(
    payload: SiteCreate,
    workspace: Workspace = Depends(get_current_workspace),
    db: Session = Depends(get_db),
) -> Site:
    assert_can_create_site(db, workspace)
    site = Site(
        workspace_id=workspace.id,
        site_key=generate_site_key(db),
        **payload.model_dump(),
    )
    db.add(site)
    db.commit()
    return site


@router.get("/{site_id}", response_model=SiteRead)
def get_site(
    site_id: UUID,
    workspace: Workspace = Depends(get_current_workspace),
    db: Session = Depends(get_db),
) -> Site:
    site = db.scalar(select(Site).where(Site.id == site_id, Site.workspace_id == workspace.id))
    if not site:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Site not found")
    return site


@router.put("/{site_id}", response_model=SiteRead)
def update_site(
    site_id: UUID,
    payload: SiteUpdate,
    workspace: Workspace = Depends(get_current_workspace),
    db: Session = Depends(get_db),
) -> Site:
    site = db.scalar(select(Site).where(Site.id == site_id, Site.workspace_id == workspace.id))
    if not site:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Site not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(site, key, value)
    db.commit()
    return site


@router.delete("/{site_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_site(
    site_id: UUID,
    workspace: Workspace = Depends(get_current_workspace),
    db: Session = Depends(get_db),
) -> None:
    site = db.scalar(select(Site).where(Site.id == site_id, Site.workspace_id == workspace.id))
    if not site:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Site not found")
    db.delete(site)
    db.commit()


@router.get("/{site_id}/embed-code", response_model=EmbedCodeResponse)
def get_embed_code(
    site_id: UUID,
    workspace: Workspace = Depends(get_current_workspace),
    db: Session = Depends(get_db),
) -> EmbedCodeResponse:
    site = db.scalar(select(Site).where(Site.id == site_id, Site.workspace_id == workspace.id))
    if not site:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Site not found")
    embed = f'<script src="{settings.app_url.rstrip("/")}/widget.js" data-site-id="{site.site_key}" async></script>'
    return EmbedCodeResponse(site_key=site.site_key, embed_code=embed)
