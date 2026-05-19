from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class KnowledgeCreate(BaseModel):
    site_id: UUID
    title: str = Field(min_length=1, max_length=220)
    content: str = Field(min_length=1)
    category: str | None = Field(default=None, max_length=120)
    is_active: bool = True


class KnowledgeUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=220)
    content: str | None = Field(default=None, min_length=1)
    category: str | None = Field(default=None, max_length=120)
    is_active: bool | None = None


class KnowledgeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    site_id: UUID
    title: str
    content: str
    category: str | None = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
