"""
Unit tests for domain entities and value objects.
"""

# Import everything needed from the unit tests package
from tests.unit import (
    # Test utilities
    pytest,
    datetime,
    # Domain objects
    Product,
    Price,
    ProductId,
    ProductName,
)


class TestProductId:
    """Test cases for ProductId value object."""

    def test_create_product_id_with_value(self):
        """Test creating ProductId with a specific value."""
        product_id = ProductId(123)
        assert product_id.value == 123

    def test_create_product_id_without_value(self):
        """Test creating ProductId without a value."""
        product_id = ProductId()
        assert product_id.value is None

    def test_product_id_with_invalid_value(self):
        """Test ProductId validation with invalid value."""
        with pytest.raises(
            ValueError,
            match="Product ID must be a positive integer",
        ):
            ProductId(0)

        with pytest.raises(
            ValueError,
            match="Product ID must be a positive integer",
        ):
            ProductId(-1)

    def test_product_id_equality(self):
        """Test ProductId equality."""
        id1 = ProductId(123)
        id2 = ProductId(123)
        id3 = ProductId(456)

        assert id1 == id2
        assert id1 != id3
        assert id1 != "not a ProductId"

    def test_product_id_hash(self):
        """Test ProductId hashing."""
        id1 = ProductId(123)
        id2 = ProductId(123)

        assert hash(id1) == hash(id2)

    def test_product_id_string_representation(self):
        """Test ProductId string representation."""
        product_id = ProductId(123)
        assert str(product_id) == "123"

        product_id_none = ProductId()
        assert str(product_id_none) == "None"


class TestProductName:
    """Test cases for ProductName value object."""

    def test_create_valid_product_name(self):
        """Test creating ProductName with valid value."""
        name = ProductName("Test Product")
        assert name.value == "Test Product"

    def test_product_name_strips_whitespace(self):
        """Test that ProductName strips whitespace."""
        name = ProductName("  Test Product  ")
        assert name.value == "Test Product"

    def test_product_name_with_empty_string(self):
        """Test ProductName validation with empty string."""
        with pytest.raises(ValueError, match="Product name cannot be empty"):
            ProductName("")

        with pytest.raises(ValueError, match="Product name cannot be empty"):
            ProductName("   ")

    def test_product_name_with_none(self):
        """Test ProductName validation with None."""
        with pytest.raises(ValueError, match="Product name cannot be empty"):
            ProductName(None)

    def test_product_name_too_long(self):
        """Test ProductName validation with too long name."""
        long_name = "a" * 1001
        with pytest.raises(
            ValueError, match="Product name cannot exceed 1000 characters"
        ):
            ProductName(long_name)

    def test_product_name_equality(self):
        """Test ProductName equality."""
        name1 = ProductName("Test Product")
        name2 = ProductName("Test Product")
        name3 = ProductName("Different Product")

        assert name1 == name2
        assert name1 != name3
        assert name1 != "not a ProductName"

    def test_product_name_hash(self):
        """Test ProductName hashing."""
        name1 = ProductName("Test Product")
        name2 = ProductName("Test Product")

        assert hash(name1) == hash(name2)

    def test_product_name_contains(self):
        """Test ProductName contains method."""
        name = ProductName("Laptop Computer")

        assert name.contains("laptop") is True
        assert name.contains("computer") is True
        assert name.contains("LAPTOP") is True
        assert name.contains("phone") is False

    def test_product_name_string_representation(self):
        """Test ProductName string representation."""
        name = ProductName("Test Product")
        assert str(name) == "Test Product"


class TestPrice:
    """Test cases for Price value object."""

    def test_create_valid_price(self):
        """Test creating Price with valid value."""
        price = Price(1000)
        assert price.value == 1000

    def test_price_with_zero(self):
        """Test Price with zero value."""
        price = Price(0)
        assert price.value == 0

    def test_price_with_negative_value(self):
        """Test Price validation with negative value."""
        with pytest.raises(ValueError, match="Price cannot be negative"):
            Price(-1)

    def test_price_too_high(self):
        """Test Price validation with too high value."""
        with pytest.raises(
            ValueError,
            match="Price cannot exceed 999,999,999 yen",
        ):
            Price(1000000000)

    def test_price_equality(self):
        """Test Price equality."""
        price1 = Price(1000)
        price2 = Price(1000)
        price3 = Price(2000)

        assert price1 == price2
        assert price1 != price3
        assert price1 != "not a Price"

    def test_price_hash(self):
        """Test Price hashing."""
        price1 = Price(1000)
        price2 = Price(1000)

        assert hash(price1) == hash(price2)

    def test_price_comparison(self):
        """Test Price comparison operators."""
        price1 = Price(1000)
        price2 = Price(2000)

        assert price1 < price2
        assert price1 <= price2
        assert price2 > price1
        assert price2 >= price1
        assert price1 <= price1
        assert price1 >= price1

    def test_price_is_in_range(self):
        """Test Price is_in_range method."""
        price = Price(1500)

        assert price.is_in_range(1000, 2000) is True
        assert price.is_in_range(1500, 1500) is True
        assert price.is_in_range(2000, 3000) is False
        assert price.is_in_range(1000, 1400) is False

    def test_price_is_expensive(self):
        """Test Price is_expensive method."""
        expensive_price = Price(150000)
        cheap_price = Price(50000)

        assert expensive_price.is_expensive() is True
        assert cheap_price.is_expensive() is False
        assert cheap_price.is_expensive(threshold=30000) is True

    def test_price_is_affordable(self):
        """Test Price is_affordable method."""
        affordable_price = Price(50000)
        expensive_price = Price(150000)
        budget = 100000

        assert affordable_price.is_affordable(budget) is True
        assert expensive_price.is_affordable(budget) is False

    def test_price_string_representation(self):
        """Test Price string representation."""
        price = Price(150000)
        assert str(price) == "150,000 yen"


class TestProduct:
    """Test cases for Product entity."""

    def test_create_product(self):
        """Test creating a Product."""
        name = ProductName("Test Product")
        price = Price(1000)
        product = Product(name=name, price=price)

        assert product.name == name
        assert product.price == price
        assert product.id is not None
        assert isinstance(product.created_at, datetime)
        assert isinstance(product.updated_at, datetime)

    def test_create_product_with_id(self):
        """Test creating a Product with specific ID."""
        name = ProductName("Test Product")
        price = Price(1000)
        product_id = ProductId(123)
        product = Product(name=name, price=price, id=product_id)

        assert product.id == product_id

    def test_product_update_name(self):
        """Test updating product name."""
        product = Product(name=ProductName("Old Name"), price=Price(1000))
        old_updated_at = product.updated_at

        new_name = ProductName("New Name")
        product.update(name=new_name)

        assert product.name == new_name
        assert product.price.value == 1000
        assert product.updated_at > old_updated_at

    def test_product_update_price(self):
        """Test updating product price."""
        product = Product(name=ProductName("Test Product"), price=Price(1000))
        old_updated_at = product.updated_at

        new_price = Price(2000)
        product.update(price=new_price)

        assert product.name.value == "Test Product"
        assert product.price == new_price
        assert product.updated_at > old_updated_at

    def test_product_update_both_fields(self):
        """Test updating both name and price."""
        product = Product(name=ProductName("Old Name"), price=Price(1000))
        old_updated_at = product.updated_at

        new_name = ProductName("New Name")
        new_price = Price(2000)
        product.update(name=new_name, price=new_price)

        assert product.name == new_name
        assert product.price == new_price
        assert product.updated_at > old_updated_at

    def test_product_update_with_no_fields(self):
        """Test updating product with no fields provided."""
        product = Product(name=ProductName("Test Product"), price=Price(1000))

        with pytest.raises(
            ValueError, match="At least one field must be provided for update"
        ):
            product.update()

    def test_product_is_expensive(self):
        """Test product is_expensive method."""
        expensive_product = Product(
            name=ProductName("Expensive Product"), price=Price(150000)
        )
        cheap_product = Product(
            name=ProductName("Cheap Product"),
            price=Price(50000),
        )

        assert expensive_product.is_expensive() is True
        assert cheap_product.is_expensive() is False
        assert cheap_product.is_expensive(threshold=30000) is True

    def test_product_is_affordable(self):
        """Test product is_affordable method."""
        affordable_product = Product(
            name=ProductName("Affordable Product"), price=Price(50000)
        )
        expensive_product = Product(
            name=ProductName("Expensive Product"), price=Price(150000)
        )
        budget = 100000

        assert affordable_product.is_affordable(budget) is True
        assert expensive_product.is_affordable(budget) is False

    def test_product_get_price_in_yen(self):
        """Test product get_price_in_yen method."""
        product = Product(
            name=ProductName("Test Product"),
            price=Price(150000),
        )

        assert product.get_price_in_yen() == 150000

    def test_product_string_representation(self):
        """Test product string representation."""
        product = Product(name=ProductName("Test Product"), price=Price(1000))

        str_repr = str(product)
        assert "Test Product" in str_repr
        assert "1,000 yen" in str_repr  # Price formats with commas
        assert str(product.id.value) in str_repr
