import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.case import CaseStatus


class CaseBase(BaseModel):
    """Base Case schema."""

    case_reference: str = Field(
        ...,
        max_length=100,
        description="Unique human-readable case reference",
    )
    input_address: str = Field(
        ...,
        max_length=128,
        description="Target suspect wallet address",
    )
    chain: str = Field(
        default="ethereum",
        max_length=50,
        description="Blockchain network name",
    )
    investigator_note: str | None = Field(
        default=None,
        description="Optional investigator commentary",
    )


class CaseCreate(CaseBase):
    """Schema for creating a new investigation case."""

    pass


class CaseUpdate(BaseModel):
    """Schema for updating an existing case."""

    status: CaseStatus | None = None
    investigator_note: str | None = None


class CaseResponse(CaseBase):
    """Schema for returning case details."""

    id: uuid.UUID
    status: CaseStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
