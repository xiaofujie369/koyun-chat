from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.conversation import Conversation
    from app.models.message import Message
    from app.models.workspace import Workspace, WorkspaceMember


class User(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(120))
    avatar_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_platform_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    owned_workspaces: Mapped[list["Workspace"]] = relationship(
        back_populates="owner", foreign_keys="Workspace.owner_user_id"
    )
    workspace_memberships: Mapped[list["WorkspaceMember"]] = relationship(back_populates="user")
    assigned_conversations: Mapped[list["Conversation"]] = relationship(back_populates="assigned_agent")
    sent_messages: Mapped[list["Message"]] = relationship(back_populates="sender_user")
