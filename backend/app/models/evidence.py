import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.address import Address
    from app.models.case import Case
    from app.models.transaction import Transaction


class EvidenceEdge(Base):
    """Evidence Edge relationship model linking two addresses within a investigation hop chain."""

    __tablename__ = "evidence_edges"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    case_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("cases.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    from_address_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("addresses.id", ondelete="CASCADE"),
        nullable=False,
    )
    to_address_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("addresses.id", ondelete="CASCADE"),
        nullable=False,
    )
    transaction_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("transactions.id", ondelete="CASCADE"),
        nullable=False,
    )
    hop_index: Mapped[int] = mapped_column(
        Integer,
        index=True,
        nullable=False,
    )
    source: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    retrieved_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    case: Mapped["Case"] = relationship(
        "Case",
        back_populates="evidence_edges",
    )
    from_address: Mapped["Address"] = relationship(
        "Address",
        foreign_keys=[from_address_id],
    )
    to_address: Mapped["Address"] = relationship(
        "Address",
        foreign_keys=[to_address_id],
    )
    transaction: Mapped["Transaction"] = relationship(
        "Transaction",
    )

    __table_args__ = (
        Index("ix_evidence_edges_case_hop", "case_id", "hop_index"),
    )
