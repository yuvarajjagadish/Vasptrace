import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class TransactionBase(BaseModel):
    """Base Transaction schema."""

    tx_hash: str = Field(..., max_length=128, description="Transaction hash")
    chain: str = Field(default="ethereum", max_length=50, description="Blockchain network name")
    block_number: int = Field(..., ge=0, description="Block number")
    timestamp: datetime = Field(..., description="Transaction timestamp")
    from_address_id: uuid.UUID = Field(..., description="Foreign key to sender address")
    to_address_id: uuid.UUID = Field(..., description="Foreign key to recipient address")
    value: Decimal = Field(..., description="Transaction value (safe Decimal representation)")
    token_contract: str | None = Field(
        default=None,
        max_length=128,
        description="ERC20 token contract address",
    )
    token_symbol: str | None = Field(
        default=None,
        max_length=20,
        description="Token ticker symbol",
    )
    data_source: str = Field(..., max_length=100, description="Data origin (e.g. etherscan)")


class TransactionCreate(TransactionBase):
    """Schema for creating a transaction record."""

    pass


class TransactionResponse(TransactionBase):
    """Schema for returning transaction details."""

    id: uuid.UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
