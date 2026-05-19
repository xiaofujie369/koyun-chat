from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class SiteBase(BaseModel):
    name: str = Field(min_length=1, max_length=160)
    domain: str | None = Field(default=None, max_length=255)
    allowed_domains: list[str] = Field(default_factory=list)
    widget_color: str = "#2563eb"
    widget_position: str = "bottom-right"
    welcome_message: str = "您好，我是在线客服，有什么可以帮您？"
    offline_message: str = "当前客服不在线，请留下联系方式，我们会尽快回复。"
    ai_enabled: bool = True
    human_chat_enabled: bool = True
    show_branding: bool = True
    status: str = "active"


class SiteCreate(SiteBase):
    pass


class SiteUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=160)
    domain: str | None = Field(default=None, max_length=255)
    allowed_domains: list[str] | None = None
    widget_color: str | None = None
    widget_position: str | None = None
    welcome_message: str | None = None
    offline_message: str | None = None
    ai_enabled: bool | None = None
    human_chat_enabled: bool | None = None
    show_branding: bool | None = None
    status: str | None = None


class SiteRead(SiteBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    workspace_id: UUID
    site_key: str
    created_at: datetime
    updated_at: datetime


class EmbedCodeResponse(BaseModel):
    site_key: str
    embed_code: str


class SitePublicConfig(BaseModel):
    site_key: str
    name: str
    widget_color: str
    widget_position: str
    welcome_message: str
    offline_message: str
    ai_enabled: bool
    human_chat_enabled: bool
    show_branding: bool
    status: str
