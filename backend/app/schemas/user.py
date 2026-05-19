from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: EmailStr
    name: str
    avatar_url: str | None = None
    is_active: bool
    is_platform_admin: bool
    created_at: datetime
    last_login_at: datetime | None = None
