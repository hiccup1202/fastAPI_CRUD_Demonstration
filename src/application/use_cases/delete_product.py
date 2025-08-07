"""
Delete Product use case.

This module contains the DeleteProduct use case which handles
the business logic for deleting an existing product.
"""

from dataclasses import dataclass
from typing import Optional

from ...domain import ProductRepository, ProductId


@dataclass
class DeleteProductRequest:
    """Request DTO for deleting a product."""

    product_id: int


@dataclass
class DeleteProductResponse:
    """Response DTO for deleting a product."""

    success: bool
    message: str


class DeleteProductUseCase:
    """
    Delete Product use case.

    Handles the business logic for deleting an existing product.
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
        request: DeleteProductRequest,
    ) -> Optional[DeleteProductResponse]:
        """
        Execute the delete product use case.

        Args:
            request: The delete product request

        Returns:
            The delete product response
        """
        # Create domain object
        product_id = ProductId(request.product_id)
        # Find existing product
        existing_product = await self.product_repository.find_by_id(product_id)

        if existing_product is None:
            return None
        # Delete from repository
        success = await self.product_repository.delete(product_id)

        if success:
            message = f"Product with ID {request.product_id} was deleted"
        else:
            message = f"Product with ID {request.product_id} was not found"

        # Return response DTO
        return DeleteProductResponse(success=success, message=message)
