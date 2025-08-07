"""
Product Repository interface.

This module contains the ProductRepository interface which defines
the contract for product data access in the domain layer.
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.product import Product
from ..value_objects.product_id import ProductId


class ProductRepository(ABC):
    """
    Product Repository interface.

    Defines the contract for product data access operations.
    This interface belongs to the domain layer and is implemented
    by the infrastructure layer.
    """

    @abstractmethod
    async def save(self, product: Product) -> Product:
        """
        Save a product to the repository.

        Args:
            product: The product to save

        Returns:
            The saved product with generated ID

        Raises:
            RepositoryError: If the save operation fails
        """
        pass

    @abstractmethod
    async def find_by_id(self, product_id: ProductId) -> Optional[Product]:
        """
        Find a product by its ID.

        Args:
            product_id: The product ID to search for

        Returns:
            The product if found, None otherwise

        Raises:
            RepositoryError: If the find operation fails
        """
        pass

    @abstractmethod
    async def find_all(self, skip: int = 0, limit: int = 100) -> List[Product]:
        """
        Find all products with pagination.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of products

        Raises:
            RepositoryError: If the find operation fails
        """
        pass

    @abstractmethod
    async def update(self, product: Product) -> Product:
        """
        Update an existing product.

        Args:
            product: The product to update

        Returns:
            The updated product

        Raises:
            RepositoryError: If the update operation fails
            ProductNotFoundError: If the product doesn't exist
        """
        pass

    @abstractmethod
    async def delete(self, product_id: ProductId) -> bool:
        """
        Delete a product by its ID.

        Args:
            product_id: The product ID to delete

        Returns:
            True if the product was deleted, False if it didn't exist

        Raises:
            RepositoryError: If the delete operation fails
        """
        pass

    @abstractmethod
    async def search(
        self,
        name: Optional[str] = None,
        min_price: Optional[int] = None,
        max_price: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Product]:
        """
        Search products by name and/or price range.

        Args:
            name: Product name (case-insensitive partial match), optional
            min_price: Minimum price (inclusive), optional
            max_price: Maximum price (inclusive), optional
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of matching products

        Raises:
            RepositoryError: If the search operation fails
        """
        pass
