import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.entity import EntityType


class EntityBase(BaseModel):
    """Base Entity schema."""

    name: str = Field(..., max_length=255, description="Entity or VASP name")
    entity_type: EntityType = Field(
        default=EntityType.UNKNOWN,
        description="Entity type classification",
    )
    vasp_flag: bool = Field(default=False, description="Flag indicating VASP status")
    source: str = Field(..., max_length=255, description="Data or intelligence source")
    source_url: str | None = Field(default=None, description="Optional reference URL")
    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Attribution confidence score",
    )


class EntityCreate(EntityBase):
    """Schema for creating a new entity."""

    pass


class EntityResponse(EntityBase):
    """Schema for returning entity details."""

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
