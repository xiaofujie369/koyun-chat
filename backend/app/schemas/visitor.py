from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class VisitorRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    site_id: UUID
    visitor_uid: str
    ip_address: str | None = None
    country: str | None = None
    region: str | None = None
    city: str | None = None
    user_agent: str | None = None
    browser: str | None = None
    os: str | None = None
    device_type: str | None = None
    language: str | None = None
    screen_width: int | None = None
    screen_height: int | None = None
    first_seen_at: datetime
    last_seen_at: datetime
    is_online: bool
    created_at: datetime
    updated_at: datetime
