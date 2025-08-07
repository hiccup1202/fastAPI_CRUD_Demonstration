"""
Product domain entity.

This module contains the Product entity which represents the core business
object for product management in the domain layer.
"""


from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

from ..value_objects.price import Price
from ..value_objects.product_id import ProductId
from ..value_objects.product_name import ProductName


@dataclass
class Product:
    """
    Product domain entity.

    Represents a product in the domain with its core business logic.
    The entity is responsible for maintaining the integrity of product data
    and enforcing business rules.
    """

    name: ProductName
    price: Price
    id: Optional[ProductId] = None
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc),
    )
    updated_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc),
    )

    def __post_init__(self) -> None:
        """Validate entity after initialization."""
        if self.id is None:
            self.id = ProductId()

    def update(
        self, name: Optional[ProductName] = None, price: Optional[Price] = None
    ) -> None:
        """
        Update product information.

        Args:
            name: New product name (optional)
            price: New product price (optional)

        Raises:
            ValueError: If both name and price are None
        """
        if name is None and price is None:
            raise ValueError("At least one field must be provided for update")

        if name is not None:
            self.name = name

        if price is not None:
            self.price = price

        self.updated_at = datetime.now(timezone.utc)

    def is_expensive(self, threshold: int = 100000) -> bool:
        """
        Check if the product is expensive based on a threshold.

        Args:
            threshold: Price threshold in yen (default: 100,000)

        Returns:
            True if product price is above threshold, False otherwise
        """
        return self.price.value > threshold

    def is_affordable(self, budget: int) -> bool:
        """
        Check if the product is affordable within a given budget.

        Args:
            budget: Available budget in yen

        Returns:
            True if product price is within budget, False otherwise
        """
        return self.price.value <= budget

    def get_price_in_yen(self) -> int:
        """
        Get the product price in yen.

        Returns:
            Product price in yen
        """
        return self.price.value

    def __str__(self) -> str:
        """String representation of the product."""
        return f"Product(id={self.id}, name={self.name}, price={self.price})"

    def __repr__(self) -> str:
        """Detailed string representation of the product."""
        return (
            f"Product("
            f"id={self.id}, "
            f"name={self.name}, "
            f"price={self.price}, "
            f"created_at={self.created_at}, "
            f"updated_at={self.updated_at}"
            f")"
        )
