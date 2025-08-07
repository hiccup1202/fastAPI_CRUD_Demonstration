"""Integration tests package.

This module provides centralized imports specifically for integration tests,
focusing on FastAPI testing utilities and the presentation layer.
"""

# Import integration test dependencies
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient

# Import the FastAPI app for testing
from src.presentation.main import app

__all__ = [
    # Test utilities
    "pytest",
    "patch",
    "TestClient",
    # FastAPI app
    "app",
]
