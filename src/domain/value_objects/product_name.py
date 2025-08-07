"""
Product Name value object.

This module contains the ProductName value object which represents
the name of a product in the domain.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ProductName:
    """
    Product Name value object.

    Represents the name of a product. This is a value object that
    encapsulates the business rules for product naming.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the product name after initialization."""
        if not self.value or not self.value.strip():
            raise ValueError("Product name cannot be empty")

        if len(self.value.strip()) > 1000:
            raise ValueError("Product name cannot exceed 1000 characters")

        # Update the value to be stripped
        object.__setattr__(self, "value", self.value.strip())

    def __str__(self) -> str:
        """String representation of the product name."""
        return self.value

    def __repr__(self) -> str:
        """Detailed string representation of the product name."""
        return f"ProductName(value='{self.value}')"

    def __eq__(self, other: object) -> bool:
        """Check equality with another ProductName."""
        if not isinstance(other, ProductName):
            return False
        return self.value == other.value

    def __hash__(self) -> int:
        """Hash the ProductName for use in sets and dictionaries."""
        return hash(self.value)

    def contains(self, text: str) -> bool:
        """
        Check if the product name contains the given text (case-insensitive).

        Args:
            text: Text to search for

        Returns:
            True if the text is found in the product name, False otherwise
        """
        return text.lower() in self.value.lower()
