"""Error handlers package.

This module provides centralized error handling for the FastAPI application.
"""

from .exception_handlers import setup_exception_handlers
from .custom_exceptions import (
    BusinessLogicError,
    ResourceNotFoundError,
    ValidationError as CustomValidationError,
)

__all__ = [
    "setup_exception_handlers",
    "BusinessLogicError",
    "ResourceNotFoundError",
    "CustomValidationError",
]
