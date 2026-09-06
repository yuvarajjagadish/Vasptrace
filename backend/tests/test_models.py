import uuid
from datetime import datetime, timezone
from decimal import Decimal

import pytest
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.database import Base
from app.models import (
    Address,
    Case,
    CaseStatus,
    Entity,
    EntityType,
    Transaction,
)
from app.schemas import (
    CaseCreate,
    CaseResponse,
    EntityCreate,
    TransactionCreate,
)


def test_models_metadata_tables():
    """Verify all 6 domain tables exist in SQLAlchemy metadata."""
    tables = Base.metadata.tables.keys()
    assert "cases" in tables
    assert "addresses" in tables
    assert "entities" in tables
    assert "transactions" in tables
    assert "evidence_edges" in tables
    assert "attributions" in tables


def test_models_indexes_and_uniqueness():
    """Verify indexes and unique constraints on domain tables."""
    # Cases table
    cases_table = Base.metadata.tables["cases"]
    assert "ix_cases_case_reference" in [idx.name for idx in cases_table.indexes]
    assert "ix_cases_input_address" in [idx.name for idx in cases_table.indexes]

    # Addresses table
    addresses_table = Base.metadata.tables["addresses"]
    assert "uq_addresses_address_chain" in [c.name for c in addresses_table.constraints]

    # Transactions table
    transactions_table = Base.metadata.tables["transactions"]
    assert "uq_transactions_tx_hash_chain" in [c.name for c in transactions_table.constraints]
    assert "ix_transactions_tx_hash" in [idx.name for idx in transactions_table.indexes]

    # Evidence edges table
    evidence_table = Base.metadata.tables["evidence_edges"]
    assert "ix_evidence_edges_case_id" in [idx.name for idx in evidence_table.indexes]
    assert "ix_evidence_edges_hop_index" in [idx.name for idx in evidence_table.indexes]

    # Attributions table
    attributions_table = Base.metadata.tables["attributions"]
    assert "ix_attributions_case_id" in [idx.name for idx in attributions_table.indexes]


def test_foreign_key_relationships():
    """Verify foreign key references exist between tables."""
    tx_table = Base.metadata.tables["transactions"]
    fk_targets = [
        [fk.column.table.name for fk in col.foreign_keys]
        for col in tx_table.columns
        if col.foreign_keys
    ]
    assert ["addresses"] in fk_targets

    edge_table = Base.metadata.tables["evidence_edges"]
    edge_fk_targets = [
        [fk.column.table.name for fk in col.foreign_keys]
        for col in edge_table.columns
        if col.foreign_keys
    ]
    assert ["cases"] in edge_fk_targets
    assert ["addresses"] in edge_fk_targets
    assert ["transactions"] in edge_fk_targets

    attr_table = Base.metadata.tables["attributions"]
    attr_fk_targets = [
        [fk.column.table.name for fk in col.foreign_keys]
        for col in attr_table.columns
        if col.foreign_keys
    ]
    assert ["cases"] in attr_fk_targets
    assert ["entities"] in attr_fk_targets


def test_pydantic_schema_validation():
    """Verify Pydantic schemas validate correctly."""
    # Case Schema
    case_in = CaseCreate(
        case_reference="CASE-2026-001",
        input_address="0x71C7656EC7ab88b098defB751B7401B5f6d8976F",
        chain="ethereum",
        investigator_note="Suspect ransomware wallet",
    )
    assert case_in.case_reference == "CASE-2026-001"

    case_res = CaseResponse(
        id=uuid.uuid4(),
        case_reference="CASE-2026-001",
        input_address="0x71C7656EC7ab88b098defB751B7401B5f6d8976F",
        chain="ethereum",
        status=CaseStatus.OPEN,
        investigator_note="Suspect ransomware wallet",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    assert case_res.status == CaseStatus.OPEN

    # Entity Schema Confidence bounds
    with pytest.raises(ValidationError):
        EntityCreate(
            name="Binance Hot Wallet",
            entity_type=EntityType.VASP,
            source="Etherscan Labels",
            confidence=1.5,  # Out of 0.0-1.0 range
        )

    # Transaction Schema Decimal value
    tx_in = TransactionCreate(
        tx_hash="0xabc123",
        chain="ethereum",
        block_number=19000000,
        timestamp=datetime.now(timezone.utc),
        from_address_id=uuid.uuid4(),
        to_address_id=uuid.uuid4(),
        value=Decimal("1500.500000000000000000"),
        data_source="etherscan",
    )
    assert isinstance(tx_in.value, Decimal)


@pytest.mark.asyncio
async def test_async_database_model_crud():
    """Verify domain models work asynchronously in an in-memory SQLite database."""
    test_engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async_session = async_sessionmaker(
        bind=test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        # Create Case
        new_case = Case(
            case_reference="CASE-TEST-999",
            input_address="0x1234567890abcdef1234567890abcdef12345678",
            chain="ethereum",
            status=CaseStatus.OPEN,
        )
        session.add(new_case)
        await session.commit()
        await session.refresh(new_case)

        assert new_case.id is not None
        assert new_case.case_reference == "CASE-TEST-999"

        # Create Addresses
        addr1 = Address(address="0x123", chain="ethereum")
        addr2 = Address(address="0x456", chain="ethereum")
        session.add_all([addr1, addr2])
        await session.commit()

        # Create Entity
        entity = Entity(
            name="Test VASP",
            entity_type=EntityType.VASP,
            vasp_flag=True,
            source="manual",
        )
        session.add(entity)
        await session.commit()

        # Create Transaction
        tx = Transaction(
            tx_hash="0xhash123",
            chain="ethereum",
            block_number=100,
            timestamp=datetime.now(timezone.utc),
            from_address_id=addr1.id,
            to_address_id=addr2.id,
            value=Decimal("10.5"),
            data_source="test_source",
        )
        session.add(tx)
        await session.commit()

        assert tx.id is not None
        assert tx.from_address_id == addr1.id

    await test_engine.dispose()
