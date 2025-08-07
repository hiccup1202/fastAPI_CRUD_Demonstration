"""Test package.

This module provides centralized imports for all test modules,
following the same pattern as the application layer.
"""

# Import common test dependencies
import pytest
from unittest.mock import AsyncMock, Mock, patch
from datetime import datetime

# Import FastAPI test dependencies
from fastapi.testclient import TestClient

# Import domain entities and value objects for testing
from src.domain.entities.product import Product
from src.domain.value_objects.price import Price
from src.domain.value_objects.product_id import ProductId
from src.domain.value_objects.product_name import ProductName

# Import application layer components
from src.application.use_cases import (
    # Create Product
    CreateProductUseCase,
    CreateProductRequest,
    CreateProductResponse,
    # Delete Product
    DeleteProductUseCase,
    DeleteProductRequest,
    DeleteProductResponse,
    # Get Product
    GetProductUseCase,
    GetProductRequest,
    GetProductResponse,
    # Search Products
    SearchProductsUseCase,
    SearchProductsRequest,
    SearchProductsResponse,
    # Update Product
    UpdateProductUseCase,
    UpdateProductRequest,
    UpdateProductResponse,
)

# Import presentation layer for integration tests
from src.presentation.main import app

__all__ = [
    # Test utilities
    "pytest",
    "AsyncMock",
    "Mock",
    "patch",
    "datetime",
    "TestClient",
    # Domain objects
    "Product",
    "Price",
    "ProductId",
    "ProductName",
    # Use Cases
    "CreateProductUseCase",
    "CreateProductRequest",
    "CreateProductResponse",
    "DeleteProductUseCase",
    "DeleteProductRequest",
    "DeleteProductResponse",
    "GetProductUseCase",
    "GetProductRequest",
    "GetProductResponse",
    "SearchProductsUseCase",
    "SearchProductsRequest",
    "SearchProductsResponse",
    "UpdateProductUseCase",
    "UpdateProductRequest",
    "UpdateProductResponse",
    # FastAPI app
    "app",
]
