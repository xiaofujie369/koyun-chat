from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.subscription import Subscription
    from app.models.workspace import Workspace


class Plan(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "plans"

    name: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    price_monthly: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    max_sites: Mapped[int | None] = mapped_column(Integer, nullable=True)
    max_agents: Mapped[int | None] = mapped_column(Integer, nullable=True)
    max_ai_messages_monthly: Mapped[int | None] = mapped_column(Integer, nullable=True)
    max_visitors_monthly: Mapped[int | None] = mapped_column(Integer, nullable=True)
    allow_remove_branding: Mapped[bool] = mapped_column(Boolean, default=False)
    allow_custom_color: Mapped[bool] = mapped_column(Boolean, default=False)
    allow_email_notification: Mapped[bool] = mapped_column(Boolean, default=False)
    allow_private_deploy: Mapped[bool] = mapped_column(Boolean, default=False)

    workspaces: Mapped[list["Workspace"]] = relationship(back_populates="plan")
    subscriptions: Mapped[list["Subscription"]] = relationship(back_populates="plan")
