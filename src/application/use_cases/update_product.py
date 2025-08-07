"""
Update Product use case.

This module contains the UpdateProduct use case which handles
the business logic for updating an existing product.
"""

from dataclasses import dataclass
from typing import Optional

from ...domain import ProductRepository, Price, ProductId, ProductName


@dataclass
class UpdateProductRequest:
    """Request DTO for updating a product."""

    product_id: int
    name: Optional[str] = None
    price: Optional[int] = None


@dataclass
class UpdateProductResponse:
    """Response DTO for updating a product."""

    id: int
    name: str
    price: int
    created_at: str
    updated_at: str


class UpdateProductUseCase:
    """
    Update Product use case.

    Handles the business logic for updating an existing product.
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
        self, request: UpdateProductRequest
    ) -> Optional[UpdateProductResponse]:
        """
        Execute the update product use case.

        Args:
            request: The update product request

        Returns:
            The update product response if found, None otherwise

        Raises:
            ValueError: If the request data is invalid
        """
        # Create domain object
        product_id = ProductId(request.product_id)

        # Find existing product
        existing_product = await self.product_repository.find_by_id(product_id)

        if existing_product is None:
            return None

        # Create domain objects for updates
        name = ProductName(request.name) if request.name is not None else None
        price = Price(request.price) if request.price is not None else None

        # Update product
        existing_product.update(name=name, price=price)

        # Save to repository
        updated_product = await self.product_repository.update(
            existing_product,
        )

        # Return response DTO
        if updated_product.id is None:
            raise ValueError("Product ID cannot be None after update")

        # Type assertion since we've checked id is not None
        product_id_value = updated_product.id.value
        assert product_id_value is not None

        return UpdateProductResponse(
            id=product_id_value,
            name=str(updated_product.name),
            price=updated_product.price.value,
            created_at=updated_product.created_at.isoformat(),
            updated_at=updated_product.updated_at.isoformat(),
        )
