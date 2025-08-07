"""
Price value object.

This module contains the Price value object which represents
the price of a product in Japanese Yen.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Price:
    """
    Price value object.

    Represents the price of a product in Japanese Yen. This is a value object
    that encapsulates the business rules for product pricing.
    """

    value: int

    def __post_init__(self) -> None:
        """Validate the price after initialization."""
        if self.value < 0:
            raise ValueError("Price cannot be negative")

        if self.value > 999999999:
            raise ValueError("Price cannot exceed 999,999,999 yen")

    def __str__(self) -> str:
        """String representation of the price."""
        return f"{self.value:,} yen"

    def __repr__(self) -> str:
        """Detailed string representation of the price."""
        return f"Price(value={self.value})"

    def __eq__(self, other: object) -> bool:
        """Check equality with another Price."""
        if not isinstance(other, Price):
            return False
        return self.value == other.value

    def __hash__(self) -> int:
        """Hash the Price for use in sets and dictionaries."""
        return hash(self.value)

    def __lt__(self, other: "Price") -> bool:
        """Check if this price is less than another price."""
        return self.value < other.value

    def __le__(self, other: "Price") -> bool:
        """Check if this price is less than or equal to another price."""
        return self.value <= other.value

    def __gt__(self, other: "Price") -> bool:
        """Check if this price is greater than another price."""
        return self.value > other.value

    def __ge__(self, other: "Price") -> bool:
        """Check if this price is greater than or equal to another price."""
        return self.value >= other.value

    def is_in_range(self, min_price: int, max_price: int) -> bool:
        """
        Check if the price is within a specified range.

        Args:
            min_price: Minimum price (inclusive)
            max_price: Maximum price (inclusive)

        Returns:
            True if the price is within the range, False otherwise
        """
        return min_price <= self.value <= max_price

    def is_expensive(self, threshold: int = 100000) -> bool:
        """
        Check if the price is expensive based on a threshold.

        Args:
            threshold: Price threshold in yen (default: 100,000)

        Returns:
            True if price is above threshold, False otherwise
        """
        return self.value > threshold

    def is_affordable(self, budget: int) -> bool:
        """
        Check if the price is affordable within a given budget.

        Args:
            budget: Available budget in yen

        Returns:
            True if price is within budget, False otherwise
        """
        return self.value <= budget
