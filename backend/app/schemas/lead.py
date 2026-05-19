from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class LeadUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    telegram: str | None = None
    whatsapp: str | None = None
    message: str | None = None
    source_url: str | None = None
    status: str | None = None


class LeadRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    site_id: UUID
    conversation_id: UUID | None = None
    visitor_id: UUID | None = None
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    telegram: str | None = None
    whatsapp: str | None = None
    message: str | None = None
    source_url: str | None = None
    status: str
    created_at: datetime
    updated_at: datetime
