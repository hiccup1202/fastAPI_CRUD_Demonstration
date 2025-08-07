"""Middleware package.

This module provides centralized middleware components for the app.
"""

from .cors_middleware import setup_cors_middleware
from .logging_middleware import setup_logging_middleware

__all__ = [
    "setup_cors_middleware",
    "setup_logging_middleware",
]
