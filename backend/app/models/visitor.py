import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.conversation import Conversation
    from app.models.lead import Lead
    from app.models.page_view import PageView
    from app.models.site import Site


class Visitor(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "visitors"
    __table_args__ = (UniqueConstraint("site_id", "visitor_uid", name="uq_site_visitor_uid"),)

    site_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("sites.id", ondelete="CASCADE"), index=True
    )
    visitor_uid: Mapped[str] = mapped_column(String(120), index=True)
    ip_address: Mapped[str | None] = mapped_column(String(80), nullable=True)
    country: Mapped[str | None] = mapped_column(String(80), nullable=True)
    region: Mapped[str | None] = mapped_column(String(120), nullable=True)
    city: Mapped[str | None] = mapped_column(String(120), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(String(800), nullable=True)
    browser: Mapped[str | None] = mapped_column(String(120), nullable=True)
    os: Mapped[str | None] = mapped_column(String(120), nullable=True)
    device_type: Mapped[str | None] = mapped_column(String(80), nullable=True)
    language: Mapped[str | None] = mapped_column(String(80), nullable=True)
    screen_width: Mapped[int | None] = mapped_column(Integer, nullable=True)
    screen_height: Mapped[int | None] = mapped_column(Integer, nullable=True)
    first_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    last_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    is_online: Mapped[bool] = mapped_column(Boolean, default=False, index=True)

    site: Mapped["Site"] = relationship(back_populates="visitors")
    page_views: Mapped[list["PageView"]] = relationship(back_populates="visitor", cascade="all, delete-orphan")
    conversations: Mapped[list["Conversation"]] = relationship(back_populates="visitor")
    leads: Mapped[list["Lead"]] = relationship(back_populates="visitor")
