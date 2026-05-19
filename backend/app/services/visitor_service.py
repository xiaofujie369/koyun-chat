from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.site import Site
from app.models.visitor import Visitor
from app.models.workspace import Workspace
from app.services.usage_service import assert_can_track_visitor, increment_usage


def parse_browser(user_agent: str | None) -> str | None:
    if not user_agent:
        return None
    lowered = user_agent.lower()
    if "edg" in lowered:
        return "Edge"
    if "chrome" in lowered:
        return "Chrome"
    if "safari" in lowered:
        return "Safari"
    if "firefox" in lowered:
        return "Firefox"
    return "Other"


def parse_os(user_agent: str | None) -> str | None:
    if not user_agent:
        return None
    lowered = user_agent.lower()
    if "windows" in lowered:
        return "Windows"
    if "mac os" in lowered:
        return "macOS"
    if "android" in lowered:
        return "Android"
    if "iphone" in lowered or "ipad" in lowered:
        return "iOS"
    if "linux" in lowered:
        return "Linux"
    return "Other"


def parse_device(user_agent: str | None) -> str:
    if not user_agent:
        return "desktop"
    lowered = user_agent.lower()
    if "mobile" in lowered or "iphone" in lowered or "android" in lowered:
        return "mobile"
    if "ipad" in lowered or "tablet" in lowered:
        return "tablet"
    return "desktop"


def upsert_visitor(
    db: Session,
    site: Site,
    workspace: Workspace,
    visitor_uid: str,
    ip_address: str | None,
    user_agent: str | None,
    language: str | None = None,
    screen_width: int | None = None,
    screen_height: int | None = None,
    is_online: bool = True,
) -> Visitor:
    visitor = db.scalar(select(Visitor).where(Visitor.site_id == site.id, Visitor.visitor_uid == visitor_uid))
    now = datetime.now(timezone.utc)
    is_new = visitor is None
    if is_new:
        assert_can_track_visitor(db, workspace)
        visitor = Visitor(
            site_id=site.id,
            visitor_uid=visitor_uid,
            first_seen_at=now,
            last_seen_at=now,
        )
        db.add(visitor)
    visitor.ip_address = ip_address
    visitor.user_agent = user_agent
    visitor.browser = parse_browser(user_agent)
    visitor.os = parse_os(user_agent)
    visitor.device_type = parse_device(user_agent)
    visitor.language = language or visitor.language
    visitor.screen_width = screen_width or visitor.screen_width
    visitor.screen_height = screen_height or visitor.screen_height
    visitor.last_seen_at = now
    visitor.is_online = is_online
    db.flush()
    if is_new:
        increment_usage(db, workspace.id, "visitor", site_id=site.id)
    return visitor
