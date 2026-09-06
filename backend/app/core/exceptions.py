"""Centralized application exception definitions for VASPTrace."""


class VASPTraceError(Exception):
    """Base exception for all VASPTrace domain errors."""

    def __init__(self, message: str, details: dict | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details or {}


class BlockchainProviderError(VASPTraceError):
    """Raised when an external blockchain provider request fails or returns invalid data."""

    pass


class InvalidWalletError(VASPTraceError):
    """Raised when a wallet address is malformed or invalid for the targeted chain."""

    pass


class InsufficientEvidenceError(VASPTraceError):
    """Raised when fund tracing cannot conclude due to missing or inconclusive evidence."""

    pass


class VASPAttributionError(VASPTraceError):
    """Raised when VASP identification or matching encounters an unrecoverable failure."""

    pass


class ReportGenerationError(VASPTraceError):
    """Raised when forensic report compilation or export fails."""

    pass
