import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.site import Site


class KnowledgeBase(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "knowledge_base"

    site_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("sites.id", ondelete="CASCADE"), index=True
    )
    title: Mapped[str] = mapped_column(String(220))
    content: Mapped[str] = mapped_column(Text)
    category: Mapped[str | None] = mapped_column(String(120), nullable=True, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    site: Mapped["Site"] = relationship(back_populates="knowledge_base")
