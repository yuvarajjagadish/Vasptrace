import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AddressBase(BaseModel):
    """Base Address schema."""

    address: str = Field(..., max_length=128, description="Blockchain address")
    chain: str = Field(default="ethereum", max_length=50, description="Blockchain network name")
    first_seen: datetime | None = None
    last_seen: datetime | None = None


class AddressCreate(AddressBase):
    """Schema for recording a new address."""

    pass


class AddressResponse(AddressBase):
    """Schema for returning address details."""

    id: uuid.UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
