import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class EvidenceEdgeBase(BaseModel):
    """Base EvidenceEdge schema."""

    case_id: uuid.UUID = Field(..., description="Foreign key to case")
    from_address_id: uuid.UUID = Field(..., description="Foreign key to source address")
    to_address_id: uuid.UUID = Field(..., description="Foreign key to destination address")
    transaction_id: uuid.UUID = Field(..., description="Foreign key to underlying transaction")
    hop_index: int = Field(..., ge=0, description="Trace hop distance index")
    source: str = Field(..., max_length=100, description="Evidence provenance source")
    retrieved_at: datetime = Field(..., description="Timestamp when evidence was retrieved")


class EvidenceEdgeCreate(EvidenceEdgeBase):
    """Schema for recording an evidence edge."""

    pass


class EvidenceEdgeResponse(EvidenceEdgeBase):
    """Schema for returning evidence edge details."""

    id: uuid.UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
