"""Product Management API - Root Package."""

# Main application
from .presentation import app

# Domain layer
from .domain import (
    Product,
    Price,
    ProductId,
    ProductName,
    ProductRepository,
)

# Application layer - Use cases
from .application import (
    CreateProductUseCase,
    GetProductUseCase,
    SearchProductsUseCase,
    UpdateProductUseCase,
    DeleteProductUseCase,
)

# Infrastructure layer
from .infrastructure import (
    SQLAlchemyProductRepository,
    get_product_repository,
)

__all__ = [
    # Main app
    "app",
    # Domain
    "Product",
    "Price",
    "ProductId",
    "ProductName",
    "ProductRepository",
    # Application
    "CreateProductUseCase",
    "GetProductUseCase",
    "SearchProductsUseCase",
    "UpdateProductUseCase",
    "DeleteProductUseCase",
    # Infrastructure
    "SQLAlchemyProductRepository",
    "get_product_repository",
]
