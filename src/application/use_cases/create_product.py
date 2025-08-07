"""
Create Product use case.

This module contains the CreateProduct use case which handles
the business logic for creating a new product.
"""


from dataclasses import dataclass

from ...domain import Product, ProductRepository, Price, ProductName


@dataclass
class CreateProductRequest:
    """Request DTO for creating a product."""

    name: str
    price: int


@dataclass
class CreateProductResponse:
    """Response DTO for creating a product."""

    id: int
    name: str
    price: int
    created_at: str
    updated_at: str


class CreateProductUseCase:
    """
    Create Product use case.

    Handles the business logic for creating a new product.
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
        request: CreateProductRequest,
    ) -> CreateProductResponse:
        """
        Execute the create product use case.

        Args:
            request: The create product request

        Returns:
            The create product response

        Raises:
            ValueError: If the request data is invalid
        """
        # Create domain objects
        product_name = ProductName(request.name)
        price = Price(request.price)

        # Create product entity
        product = Product(name=product_name, price=price)

        # Save to repository
        saved_product = await self.product_repository.save(product)

        # Return response DTO
        if saved_product.id is None:
            raise ValueError("Product ID cannot be None after save")

        # Type assertion since we've checked id is not None
        product_id_value = saved_product.id.value
        assert product_id_value is not None

        return CreateProductResponse(
            id=product_id_value,
            name=str(saved_product.name),
            price=saved_product.price.value,
            created_at=saved_product.created_at.isoformat(),
            updated_at=saved_product.updated_at.isoformat(),
        )
