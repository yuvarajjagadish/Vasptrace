import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class AttributionBase(BaseModel):
    """Base Attribution schema."""

    case_id: uuid.UUID = Field(
        ...,
        description="Foreign key to case",
    )
    terminal_entity_id: uuid.UUID = Field(
        ...,
        description="Foreign key to identified terminal entity",
    )
    confidence_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Overall attribution confidence score",
    )
    scoring_breakdown: dict[str, Any] = Field(
        default_factory=dict,
        description="JSONB scoring breakdown detail",
    )


class AttributionCreate(AttributionBase):
    """Schema for creating an attribution record."""

    pass


class AttributionResponse(AttributionBase):
    """Schema for returning attribution details."""

    id: uuid.UUID
    generated_at: datetime

    model_config = ConfigDict(from_attributes=True)
