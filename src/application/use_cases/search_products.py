"""
Search Products use case.

This module contains the SearchProducts use case which handles
the business logic for searching products by name and price range.
"""

from dataclasses import dataclass
from typing import List, Optional

from ...domain import ProductRepository


@dataclass
class SearchProductsRequest:
    """Request DTO for searching products."""

    name: Optional[str] = None
    min_price: Optional[int] = None
    max_price: Optional[int] = None
    skip: int = 0
    limit: int = 100


@dataclass
class ProductSearchItem:
    """DTO for a product in search results."""

    id: int
    name: str
    price: int
    created_at: str
    updated_at: str


@dataclass
class SearchProductsResponse:
    """Response DTO for searching products."""

    products: List[ProductSearchItem]
    total_count: int
    skip: int
    limit: int
    search_criteria: dict


class SearchProductsUseCase:
    """
    Search Products use case.

    Handles the business logic for searching products by name and price range.
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
        request: SearchProductsRequest,
    ) -> SearchProductsResponse:
        """
        Execute the search products use case.

        Args:
            request: The search products request

        Returns:
            The search products response
        """
        # Use the consolidated search method
        if (
            request.name is not None
            or request.min_price is not None
            or request.max_price is not None
        ):
            # Search with provided criteria
            products = await self.product_repository.search(
                name=request.name,
                min_price=request.min_price,
                max_price=request.max_price,
                skip=request.skip,
                limit=request.limit,
            )
        else:
            # No search criteria, return all products
            products = await self.product_repository.find_all(
                skip=request.skip, limit=request.limit
            )

        # Convert to DTOs
        product_items = []
        for product in products:
            if product.id is None:
                raise ValueError("Product ID cannot be None")

            # Type assertion since we've checked id is not None
            product_id_value = product.id.value
            assert product_id_value is not None

            product_items.append(
                ProductSearchItem(
                    id=product_id_value,
                    name=str(product.name),
                    price=product.price.value,
                    created_at=product.created_at.isoformat(),
                    updated_at=product.updated_at.isoformat(),
                )
            )

        # Build search criteria for response
        search_criteria: dict = {}
        if request.name:
            search_criteria["name"] = request.name
        if request.min_price is not None:
            search_criteria["min_price"] = request.min_price
        if request.max_price is not None:
            search_criteria["max_price"] = request.max_price

        # Return response DTO
        return SearchProductsResponse(
            products=product_items,
            total_count=len(product_items),
            skip=request.skip,
            limit=request.limit,
            search_criteria=search_criteria,
        )
