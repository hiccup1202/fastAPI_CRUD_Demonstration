"""
Product ID value object.

This module contains the ProductId value object which represents
the unique identifier for a product in the domain.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ProductId:
    """
    Product ID value object.

    Represents a unique identifier for a product. This is a value object
    that encapsulates the business rules for product identification.
    """

    value: Optional[int] = None

    def __post_init__(self) -> None:
        """Validate the product ID after initialization."""
        if self.value is not None and self.value <= 0:
            raise ValueError("Product ID must be a positive integer")

    def __str__(self) -> str:
        """String representation of the product ID."""
        return str(self.value) if self.value is not None else "None"

    def __repr__(self) -> str:
        """Detailed string representation of the product ID."""
        return f"ProductId(value={self.value})"

    def __eq__(self, other: object) -> bool:
        """Check equality with another ProductId."""
        if not isinstance(other, ProductId):
            return False
        return self.value == other.value

    def __hash__(self) -> int:
        """Hash the ProductId for use in sets and dictionaries."""
        return hash(self.value)
