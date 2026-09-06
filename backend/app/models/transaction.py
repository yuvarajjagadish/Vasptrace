import uuid
from datetime import datetime, timezone
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, DateTime, ForeignKey, Index, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.address import Address


class Transaction(Base):
    """Blockchain Transaction domain model."""

    __tablename__ = "transactions"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    tx_hash: Mapped[str] = mapped_column(
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
    block_number: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        index=True,
        nullable=False,
    )
    from_address_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("addresses.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    to_address_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("addresses.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    value: Mapped[Decimal] = mapped_column(
        Numeric(precision=38, scale=18),
        nullable=False,
    )
    token_contract: Mapped[str | None] = mapped_column(
        String(128),
        nullable=True,
    )
    token_symbol: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )
    data_source: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    from_address: Mapped["Address"] = relationship(
        "Address",
        foreign_keys=[from_address_id],
    )
    to_address: Mapped["Address"] = relationship(
        "Address",
        foreign_keys=[to_address_id],
    )

    __table_args__ = (
        UniqueConstraint("tx_hash", "chain", name="uq_transactions_tx_hash_chain"),
        Index("ix_transactions_tx_hash_chain", "tx_hash", "chain"),
    )
