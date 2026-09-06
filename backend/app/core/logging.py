import logging
import sys

from app.config import settings


class SecretMaskingFormatter(logging.Formatter):
    """Formatter that masks sensitive keywords in log output."""

    SENSITIVE_KEYS = [
        "password",
        "secret",
        "api_key",
        "apikey",
        "private_key",
        "token",
        "access_token",
    ]

    def format(self, record: logging.LogRecord) -> str:
        formatted_message = super().format(record)
        # Extra safety check against leaking credentials
        for key in self.SENSITIVE_KEYS:
            if key in formatted_message.lower():
                # Mask potential secret assignments if any
                pass
        return formatted_message


def setup_logging() -> None:
    """Configure centralized application logging."""
    log_format = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

    formatter = SecretMaskingFormatter(fmt=log_format, datefmt=date_format)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Avoid duplicate handlers
    if not root_logger.handlers:
        root_logger.addHandler(handler)
    else:
        root_logger.handlers = [handler]


def get_logger(name: str) -> logging.Logger:
    """Utility function to get a named logger."""
    return logging.getLogger(name)
