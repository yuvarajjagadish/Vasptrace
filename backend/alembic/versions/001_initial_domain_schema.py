"""Initial domain schema migration.

Revision ID: 001_initial_domain_schema
Revises:
Create Date: 2026-09-06 00:00:00.000000

"""
from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "001_initial_domain_schema"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # 1. Create cases table
    op.create_table(
        "cases",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("case_reference", sa.String(length=100), nullable=False),
        sa.Column("input_address", sa.String(length=128), nullable=False),
        sa.Column("chain", sa.String(length=50), nullable=False, server_default="ethereum"),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="OPEN"),
        sa.Column("investigator_note", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("case_reference", name="uq_cases_case_reference"),
    )
    op.create_index("ix_cases_case_reference", "cases", ["case_reference"])
    op.create_index("ix_cases_input_address", "cases", ["input_address"])
    op.create_index("ix_cases_chain_status", "cases", ["chain", "status"])

    # 2. Create addresses table
    op.create_table(
        "addresses",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("address", sa.String(length=128), nullable=False),
        sa.Column("chain", sa.String(length=50), nullable=False, server_default="ethereum"),
        sa.Column("first_seen", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_seen", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("address", "chain", name="uq_addresses_address_chain"),
    )
    op.create_index("ix_addresses_address", "addresses", ["address"])
    op.create_index("ix_addresses_chain", "addresses", ["chain"])
    op.create_index("ix_addresses_address_chain", "addresses", ["address", "chain"])

    # 3. Create entities table
    op.create_table(
        "entities",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("entity_type", sa.String(length=50), nullable=False, server_default="UNKNOWN"),
        sa.Column("vasp_flag", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("source", sa.String(length=255), nullable=False),
        sa.Column("source_url", sa.Text(), nullable=True),
        sa.Column("confidence", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    # 4. Create transactions table
    op.create_table(
        "transactions",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("tx_hash", sa.String(length=128), nullable=False),
        sa.Column("chain", sa.String(length=50), nullable=False, server_default="ethereum"),
        sa.Column("block_number", sa.BigInteger(), nullable=False),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("from_address_id", sa.UUID(), nullable=False),
        sa.Column("to_address_id", sa.UUID(), nullable=False),
        sa.Column("value", sa.Numeric(precision=38, scale=18), nullable=False),
        sa.Column("token_contract", sa.String(length=128), nullable=True),
        sa.Column("token_symbol", sa.String(length=20), nullable=True),
        sa.Column("data_source", sa.String(length=100), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["from_address_id"], ["addresses.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["to_address_id"], ["addresses.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("tx_hash", "chain", name="uq_transactions_tx_hash_chain"),
    )
    op.create_index("ix_transactions_tx_hash", "transactions", ["tx_hash"])
    op.create_index("ix_transactions_chain", "transactions", ["chain"])
    op.create_index("ix_transactions_timestamp", "transactions", ["timestamp"])
    op.create_index("ix_transactions_from_address_id", "transactions", ["from_address_id"])
    op.create_index("ix_transactions_to_address_id", "transactions", ["to_address_id"])
    op.create_index("ix_transactions_tx_hash_chain", "transactions", ["tx_hash", "chain"])

    # 5. Create evidence_edges table
    op.create_table(
        "evidence_edges",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("case_id", sa.UUID(), nullable=False),
        sa.Column("from_address_id", sa.UUID(), nullable=False),
        sa.Column("to_address_id", sa.UUID(), nullable=False),
        sa.Column("transaction_id", sa.UUID(), nullable=False),
        sa.Column("hop_index", sa.Integer(), nullable=False),
        sa.Column("source", sa.String(length=100), nullable=False),
        sa.Column("retrieved_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["case_id"], ["cases.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["from_address_id"], ["addresses.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["to_address_id"], ["addresses.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["transaction_id"], ["transactions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_evidence_edges_case_id", "evidence_edges", ["case_id"])
    op.create_index("ix_evidence_edges_hop_index", "evidence_edges", ["hop_index"])
    op.create_index("ix_evidence_edges_case_hop", "evidence_edges", ["case_id", "hop_index"])

    # 6. Create attributions table
    op.create_table(
        "attributions",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("case_id", sa.UUID(), nullable=False),
        sa.Column("terminal_entity_id", sa.UUID(), nullable=False),
        sa.Column("confidence_score", sa.Float(), nullable=False),
        sa.Column(
            "scoring_breakdown",
            postgresql.JSONB(astext_type=sa.Text()).with_variant(sa.JSON(), "sqlite"),
            nullable=False,
        ),
        sa.Column("generated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["case_id"], ["cases.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["terminal_entity_id"], ["entities.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_attributions_case_id", "attributions", ["case_id"])


def downgrade() -> None:
    op.drop_table("attributions")
    op.drop_table("evidence_edges")
    op.drop_table("transactions")
    op.drop_table("entities")
    op.drop_table("addresses")
    op.drop_table("cases")
