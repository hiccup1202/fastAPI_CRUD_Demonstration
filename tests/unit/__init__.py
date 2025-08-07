"""Unit tests package.

This module provides centralized imports specifically for unit tests,
focusing on domain entities, value objects, and use cases.
"""

# Import common unit test dependencies
import pytest
from unittest.mock import AsyncMock
from datetime import datetime

# Import domain components that are frequently used in unit tests
from src.domain.entities.product import Product
from src.domain.value_objects.price import Price
from src.domain.value_objects.product_id import ProductId
from src.domain.value_objects.product_name import ProductName

# Import all use cases and their request/response objects
from src.application.use_cases.create_product import (
    CreateProductUseCase,
    CreateProductRequest,
    CreateProductResponse,
)
from src.application.use_cases.delete_product import (
    DeleteProductUseCase,
    DeleteProductRequest,
    DeleteProductResponse,
)
from src.application.use_cases.get_product import (
    GetProductUseCase,
    GetProductRequest,
    GetProductResponse,
)
from src.application.use_cases.search_products import (
    SearchProductsUseCase,
    SearchProductsRequest,
    SearchProductsResponse,
)
from src.application.use_cases.update_product import (
    UpdateProductUseCase,
    UpdateProductRequest,
    UpdateProductResponse,
)

__all__ = [
    # Test utilities
    "pytest",
    "AsyncMock",
    "datetime",
    # Domain objects
    "Product",
    "Price",
    "ProductId",
    "ProductName",
    # Create Product
    "CreateProductUseCase",
    "CreateProductRequest",
    "CreateProductResponse",
    # Delete Product
    "DeleteProductUseCase",
    "DeleteProductRequest",
    "DeleteProductResponse",
    # Get Product
    "GetProductUseCase",
    "GetProductRequest",
    "GetProductResponse",
    # Search Products
    "SearchProductsUseCase",
    "SearchProductsRequest",
    "SearchProductsResponse",
    # Update Product
    "UpdateProductUseCase",
    "UpdateProductRequest",
    "UpdateProductResponse",
]
