from urllib.parse import urlparse

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.page_view import PageView
from app.models.site import Site
from app.models.workspace import Workspace
from app.schemas.site import SitePublicConfig
from app.schemas.widget import (
    PageViewRequest,
    WidgetInitRequest,
    WidgetInitResponse,
    WidgetMessageRequest,
    WidgetMessageResponse,
)
from app.services.chat_service import handle_visitor_message
from app.services.visitor_service import upsert_visitor

router = APIRouter()


def get_public_site(db: Session, site_key: str) -> Site:
    site = db.scalar(select(Site).where(Site.site_key == site_key))
    if not site or site.status != "active":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Site not available")
    return site


def validate_allowed_domain(site: Site, request: Request) -> None:
    allowed_domains = site.allowed_domains or []
    if not allowed_domains:
        return
    origin = request.headers.get("origin") or request.headers.get("referer")
    host = urlparse(origin).hostname if origin else None
    if not host:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Origin is required")
    normalized = {domain.lower().removeprefix("www.") for domain in allowed_domains}
    request_host = host.lower().removeprefix("www.")
    if request_host not in normalized and not any(request_host.endswith(f".{domain}") for domain in normalized):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Origin is not allowed")


@router.get("/site/{site_key}/config", response_model=SitePublicConfig)
def get_site_config(site_key: str, request: Request, db: Session = Depends(get_db)) -> dict:
    site = get_public_site(db, site_key)
    validate_allowed_domain(site, request)
    return site.public_config()


@router.post("/init", response_model=WidgetInitResponse)
def init_widget(payload: WidgetInitRequest, request: Request, db: Session = Depends(get_db)) -> WidgetInitResponse:
    site = get_public_site(db, payload.site_key)
    validate_allowed_domain(site, request)
    workspace = db.get(Workspace, site.workspace_id)
    visitor = upsert_visitor(
        db,
        site=site,
        workspace=workspace,
        visitor_uid=payload.visitor_uid,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
        language=payload.language,
        screen_width=payload.screen_width,
        screen_height=payload.screen_height,
        is_online=True,
    )
    db.commit()
    return WidgetInitResponse(visitor_id=visitor.id, visitor_uid=visitor.visitor_uid, site_key=site.site_key)


@router.post("/page-view")
def track_page_view(payload: PageViewRequest, request: Request, db: Session = Depends(get_db)) -> dict[str, str]:
    site = get_public_site(db, payload.site_key)
    validate_allowed_domain(site, request)
    visitor = upsert_visitor(
        db,
        site=site,
        workspace=db.get(Workspace, site.workspace_id),
        visitor_uid=payload.visitor_uid,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
        is_online=True,
    )
    page_view = PageView(
        site_id=site.id,
        visitor_id=visitor.id,
        url=payload.url,
        title=payload.title,
        referrer=payload.referrer,
        utm_source=payload.utm_source,
        utm_medium=payload.utm_medium,
        utm_campaign=payload.utm_campaign,
    )
    db.add(page_view)
    db.commit()
    return {"message": "tracked"}


@router.post("/message", response_model=WidgetMessageResponse)
async def send_widget_message(
    payload: WidgetMessageRequest,
    request: Request,
    db: Session = Depends(get_db),
) -> WidgetMessageResponse:
    site = get_public_site(db, payload.site_key)
    validate_allowed_domain(site, request)
    workspace = db.get(Workspace, site.workspace_id)
    visitor = upsert_visitor(
        db,
        site=site,
        workspace=workspace,
        visitor_uid=payload.visitor_uid,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
        is_online=True,
    )
    conversation, messages = await handle_visitor_message(
        db,
        workspace=workspace,
        site=site,
        visitor=visitor,
        content=payload.content,
        source_url=payload.source_url,
        lead_payload=payload.lead,
    )
    return WidgetMessageResponse(conversation_id=conversation.id, messages=messages)
