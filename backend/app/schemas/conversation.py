from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.schemas.message import MessageRead


class ConversationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    site_id: UUID
    visitor_id: UUID
    assigned_agent_id: UUID | None = None
    status: str
    channel: str
    started_at: datetime
    last_message_at: datetime | None = None
    closed_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


class ConversationWithMessages(ConversationRead):
    messages: list[MessageRead] = []


class AssignConversationRequest(BaseModel):
    agent_id: UUID | None = None
