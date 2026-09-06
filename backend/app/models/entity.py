import enum
import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Enum, Float, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.attribution import Attribution


class EntityType(str, enum.Enum):
    """Entity classification enumeration."""

    EXCHANGE = "EXCHANGE"
    CUSTODIAN = "CUSTODIAN"
    VASP = "VASP"
    MIXER = "MIXER"
    BRIDGE = "BRIDGE"
    UNKNOWN = "UNKNOWN"


class Entity(Base):
    """VASP or Off-Chain Entity model."""

    __tablename__ = "entities"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    entity_type: Mapped[EntityType] = mapped_column(
        Enum(EntityType, name="entity_type_enum", native_enum=False),
        default=EntityType.UNKNOWN,
        nullable=False,
    )
    vasp_flag: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    source: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    source_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    confidence: Mapped[float] = mapped_column(
        Float,
        default=1.0,
        nullable=False,
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
    attributions: Mapped[list["Attribution"]] = relationship(
        "Attribution",
        back_populates="terminal_entity",
    )
