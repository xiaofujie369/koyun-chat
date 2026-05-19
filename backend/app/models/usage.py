import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.site import Site
    from app.models.workspace import Workspace


class UsageRecord(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "usage_records"

    workspace_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("workspaces.id", ondelete="CASCADE"), index=True
    )
    site_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("sites.id", ondelete="CASCADE"), nullable=True, index=True
    )
    usage_type: Mapped[str] = mapped_column(String(40), index=True)
    count: Mapped[int] = mapped_column(Integer, default=1)
    period: Mapped[str] = mapped_column(String(20), index=True)
    workspace: Mapped["Workspace"] = relationship(back_populates="usage_records")
    site: Mapped["Site | None"] = relationship(back_populates="usage_records")
