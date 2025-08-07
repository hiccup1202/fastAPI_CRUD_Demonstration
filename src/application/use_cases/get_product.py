"""
Get Product use case.

This module contains the GetProduct use case which handles
the business logic for retrieving a product by ID.
"""

from dataclasses import dataclass
from typing import Optional

from ...domain import ProductRepository, ProductId


@dataclass
class GetProductRequest:
    """Request DTO for getting a product."""

    product_id: int


@dataclass
class GetProductResponse:
    """Response DTO for getting a product."""

    id: int
    name: str
    price: int
    created_at: str
    updated_at: str


class GetProductUseCase:
    """
    Get Product use case.

    Handles the business logic for retrieving a product by ID.
    This use case belongs to the application layer and orchestrates
    the domain objects and repository operations.
    """

    def __init__(self, product_repository: ProductRepository):
        """
        Initialize the use case.

        Args:
            product_repository: Repository for product operations
        """
        self.product_repository = product_repository

    async def execute(
        self,
        request: GetProductRequest,
    ) -> Optional[GetProductResponse]:
        """
        Execute the get product use case.

        Args:
            request: The get product request

        Returns:
            The get product response if found, None otherwise
        """
        # Create domain object
        product_id = ProductId(request.product_id)

        # Find product in repository
        product = await self.product_repository.find_by_id(product_id)

        if product is None:
            return None

        # Return response DTO
        if product.id is None:
            raise ValueError("Product ID cannot be None")

        # Type assertion since we've checked id is not None
        product_id_value = product.id.value
        assert product_id_value is not None

        return GetProductResponse(
            id=product_id_value,
            name=str(product.name),
            price=product.price.value,
            created_at=product.created_at.isoformat(),
            updated_at=product.updated_at.isoformat(),
        )
