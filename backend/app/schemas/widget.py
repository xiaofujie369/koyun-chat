from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.message import MessageRead


class WidgetInitRequest(BaseModel):
    site_key: str
    visitor_uid: str
    url: str | None = None
    title: str | None = None
    referrer: str | None = None
    language: str | None = None
    screen_width: int | None = None
    screen_height: int | None = None


class WidgetInitResponse(BaseModel):
    visitor_id: UUID
    visitor_uid: str
    site_key: str


class PageViewRequest(BaseModel):
    site_key: str
    visitor_uid: str
    url: str
    title: str | None = None
    referrer: str | None = None
    utm_source: str | None = None
    utm_medium: str | None = None
    utm_campaign: str | None = None


class WidgetMessageRequest(BaseModel):
    site_key: str
    visitor_uid: str
    content: str = Field(min_length=1, max_length=5000)
    source_url: str | None = None
    lead: dict[str, Any] | None = None


class WidgetMessageResponse(BaseModel):
    conversation_id: UUID
    messages: list[MessageRead]
