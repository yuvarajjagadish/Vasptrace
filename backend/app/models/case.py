import enum
import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.attribution import Attribution
    from app.models.evidence import EvidenceEdge


class CaseStatus(str, enum.Enum):
    """Case investigation status enumeration."""

    OPEN = "OPEN"
    ANALYZING = "ANALYZING"
    COMPLETED = "COMPLETED"
    UNRESOLVED = "UNRESOLVED"
    FAILED = "FAILED"


class Case(Base):
    """Investigation Case model representing a wallet tracing task."""

    __tablename__ = "cases"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    case_reference: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
        nullable=False,
    )
    input_address: Mapped[str] = mapped_column(
        String(128),
        index=True,
        nullable=False,
    )
    chain: Mapped[str] = mapped_column(
        String(50),
        default="ethereum",
        nullable=False,
    )
    status: Mapped[CaseStatus] = mapped_column(
        Enum(CaseStatus, name="case_status_enum", native_enum=False),
        default=CaseStatus.OPEN,
        nullable=False,
    )
    investigator_note: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    evidence_edges: Mapped[list["EvidenceEdge"]] = relationship(
        "EvidenceEdge",
        back_populates="case",
        cascade="all, delete-orphan",
    )
    attributions: Mapped[list["Attribution"]] = relationship(
        "Attribution",
        back_populates="case",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        Index("ix_cases_chain_status", "chain", "status"),
    )
