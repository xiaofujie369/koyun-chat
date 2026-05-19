import uuid
from typing import TYPE_CHECKING, Any

from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.conversation import Conversation
    from app.models.knowledge import KnowledgeBase
    from app.models.lead import Lead
    from app.models.page_view import PageView
    from app.models.usage import UsageRecord
    from app.models.visitor import Visitor
    from app.models.workspace import Workspace


class Site(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "sites"

    workspace_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("workspaces.id", ondelete="CASCADE"), index=True
    )
    site_key: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(160))
    domain: Mapped[str | None] = mapped_column(String(255), nullable=True)
    allowed_domains: Mapped[list[str]] = mapped_column(JSONB, default=list)
    widget_color: Mapped[str] = mapped_column(String(20), default="#2563eb")
    widget_position: Mapped[str] = mapped_column(String(40), default="bottom-right")
    welcome_message: Mapped[str] = mapped_column(
        Text, default="您好，我是在线客服，有什么可以帮您？"
    )
    offline_message: Mapped[str] = mapped_column(
        Text, default="当前客服不在线，请留下联系方式，我们会尽快回复。"
    )
    ai_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    human_chat_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    show_branding: Mapped[bool] = mapped_column(Boolean, default=True)
    status: Mapped[str] = mapped_column(String(40), default="active", index=True)

    workspace: Mapped["Workspace"] = relationship(back_populates="sites")
    visitors: Mapped[list["Visitor"]] = relationship(back_populates="site", cascade="all, delete-orphan")
    page_views: Mapped[list["PageView"]] = relationship(back_populates="site", cascade="all, delete-orphan")
    conversations: Mapped[list["Conversation"]] = relationship(back_populates="site", cascade="all, delete-orphan")
    knowledge_base: Mapped[list["KnowledgeBase"]] = relationship(back_populates="site", cascade="all, delete-orphan")
    leads: Mapped[list["Lead"]] = relationship(back_populates="site", cascade="all, delete-orphan")
    usage_records: Mapped[list["UsageRecord"]] = relationship(back_populates="site")

    def public_config(self) -> dict[str, Any]:
        return {
            "site_key": self.site_key,
            "name": self.name,
            "widget_color": self.widget_color,
            "widget_position": self.widget_position,
            "welcome_message": self.welcome_message,
            "offline_message": self.offline_message,
            "ai_enabled": self.ai_enabled,
            "human_chat_enabled": self.human_chat_enabled,
            "show_branding": self.show_branding,
            "status": self.status,
        }
