import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, Index, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Address(Base):
    """Blockchain Address domain model."""

    __tablename__ = "addresses"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    address: Mapped[str] = mapped_column(
        String(128),
        index=True,
        nullable=False,
    )
    chain: Mapped[str] = mapped_column(
        String(50),
        index=True,
        default="ethereum",
        nullable=False,
    )
    first_seen: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    last_seen: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint("address", "chain", name="uq_addresses_address_chain"),
        Index("ix_addresses_address_chain", "address", "chain"),
    )
