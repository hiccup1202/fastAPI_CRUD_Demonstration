"""
Unit tests for application use cases.

This module contains unit tests for the application layer use cases.
"""

# Import everything needed from the unit tests package
from tests.unit import (
    # Test utilities
    pytest,
    AsyncMock,
    datetime,
    # Domain objects
    Product,
    Price,
    ProductId,
    ProductName,
    # Create Product
    CreateProductUseCase,
    CreateProductRequest,
    CreateProductResponse,
    # Delete Product
    DeleteProductUseCase,
    DeleteProductRequest,
    DeleteProductResponse,
    # Get Product
    GetProductUseCase,
    GetProductRequest,
    GetProductResponse,
    # Search Products
    SearchProductsUseCase,
    SearchProductsRequest,
    SearchProductsResponse,
    # Update Product
    UpdateProductUseCase,
    UpdateProductRequest,
    UpdateProductResponse,
)


class TestCreateProductUseCase:
    """Test cases for CreateProductUseCase."""

    @pytest.mark.asyncio
    async def test_create_product_success(self):
        """Test successful product creation."""
        # Arrange
        mock_repository = AsyncMock()
        use_case = CreateProductUseCase(mock_repository)

        request = CreateProductRequest(name="Test Product", price=1000)

        # Mock the saved product
        saved_product = Product(
            id=ProductId(123),
            name=ProductName("Test Product"),
            price=Price(1000),
            created_at=datetime(2024, 1, 1, 12, 0, 0),
            updated_at=datetime(2024, 1, 1, 12, 0, 0),
        )
        mock_repository.save.return_value = saved_product

        # Act
        response = await use_case.execute(request)

        # Assert
        assert isinstance(response, CreateProductResponse)
        assert response.id == 123
        assert response.name == "Test Product"
        assert response.price == 1000
        assert response.created_at == "2024-01-01T12:00:00"
        assert response.updated_at == "2024-01-01T12:00:00"

        mock_repository.save.assert_called_once()
        saved_product_arg = mock_repository.save.call_args[0][0]
        assert saved_product_arg.name.value == "Test Product"
        assert saved_product_arg.price.value == 1000


class TestGetProductUseCase:
    """Test cases for GetProductUseCase."""

    @pytest.mark.asyncio
    async def test_get_product_success(self):
        """Test successful product retrieval."""
        # Arrange
        mock_repository = AsyncMock()
        use_case = GetProductUseCase(mock_repository)

        request = GetProductRequest(product_id=123)

        # Mock the found product
        found_product = Product(
            id=ProductId(123),
            name=ProductName("Test Product"),
            price=Price(1000),
            created_at=datetime(2024, 1, 1, 12, 0, 0),
            updated_at=datetime(2024, 1, 1, 12, 0, 0),
        )
        mock_repository.find_by_id.return_value = found_product

        # Act
        response = await use_case.execute(request)

        # Assert
        assert isinstance(response, GetProductResponse)
        assert response.id == 123
        assert response.name == "Test Product"
        assert response.price == 1000
        assert response.created_at == "2024-01-01T12:00:00"
        assert response.updated_at == "2024-01-01T12:00:00"

        mock_repository.find_by_id.assert_called_once_with(ProductId(123))

    @pytest.mark.asyncio
    async def test_get_product_not_found(self):
        """Test product retrieval when product not found."""
        # Arrange
        mock_repository = AsyncMock()
        use_case = GetProductUseCase(mock_repository)

        request = GetProductRequest(product_id=999)
        mock_repository.find_by_id.return_value = None

        # Act
        response = await use_case.execute(request)

        # Assert
        assert response is None
        mock_repository.find_by_id.assert_called_once_with(ProductId(999))


class TestUpdateProductUseCase:
    """Test cases for UpdateProductUseCase."""

    @pytest.mark.asyncio
    async def test_update_product_success(self):
        """Test successful product update."""
        # Arrange
        mock_repository = AsyncMock()
        use_case = UpdateProductUseCase(mock_repository)

        request = UpdateProductRequest(
            product_id=123, name="Updated Product", price=2000
        )

        # Mock the existing product
        existing_product = Product(
            id=ProductId(123),
            name=ProductName("Old Product"),
            price=Price(1000),
            created_at=datetime(2024, 1, 1, 12, 0, 0),
            updated_at=datetime(2024, 1, 1, 12, 0, 0),
        )
        mock_repository.find_by_id.return_value = existing_product

        # Mock the updated product
        updated_product = Product(
            id=ProductId(123),
            name=ProductName("Updated Product"),
            price=Price(2000),
            created_at=datetime(2024, 1, 1, 12, 0, 0),
            updated_at=datetime(2024, 1, 1, 13, 0, 0),
        )
        mock_repository.update.return_value = updated_product

        # Act
        response = await use_case.execute(request)

        # Assert
        assert isinstance(response, UpdateProductResponse)
        assert response.id == 123
        assert response.name == "Updated Product"
        assert response.price == 2000

        mock_repository.find_by_id.assert_called_once_with(ProductId(123))
        mock_repository.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_product_not_found(self):
        """Test product update when product not found."""
        # Arrange
        mock_repository = AsyncMock()
        use_case = UpdateProductUseCase(mock_repository)

        request = UpdateProductRequest(product_id=999, name="Updated Product")
        mock_repository.find_by_id.return_value = None

        # Act
        response = await use_case.execute(request)

        # Assert
        assert response is None
        mock_repository.find_by_id.assert_called_once_with(ProductId(999))
        mock_repository.update.assert_not_called()


class TestDeleteProductUseCase:
    """Test cases for DeleteProductUseCase."""

    @pytest.mark.asyncio
    async def test_delete_product_success(self):
        """Test successful product deletion."""
        # Arrange
        mock_repository = AsyncMock()
        use_case = DeleteProductUseCase(mock_repository)

        request = DeleteProductRequest(product_id=123)
        mock_repository.delete.return_value = True

        # Act
        response = await use_case.execute(request)

        # Assert
        assert isinstance(response, DeleteProductResponse)
        assert response.success is True
        assert "deleted" in response.message

        mock_repository.delete.assert_called_once_with(ProductId(123))

    @pytest.mark.asyncio
    async def test_delete_product_not_found(self):
        """Test product deletion when product not found."""
        # Arrange
        mock_repository = AsyncMock()
        use_case = DeleteProductUseCase(mock_repository)

        request = DeleteProductRequest(product_id=999)
        mock_repository.delete.return_value = False

        # Act
        response = await use_case.execute(request)

        # Assert
        assert isinstance(response, DeleteProductResponse)
        assert response.success is False
        assert "not found" in response.message

        mock_repository.delete.assert_called_once_with(ProductId(999))


class TestSearchProductsUseCase:
    """Test cases for SearchProductsUseCase."""

    @pytest.mark.asyncio
    async def test_search_by_name_and_price_range(self):
        """Test search by name and price range."""
        # Arrange
        mock_repository = AsyncMock()
        use_case = SearchProductsUseCase(mock_repository)

        request = SearchProductsRequest(
            name="laptop", min_price=100000, max_price=200000, skip=0, limit=10
        )

        # Mock the search results
        products = [
            Product(
                id=ProductId(1),
                name=ProductName("Laptop Computer"),
                price=Price(150000),
                created_at=datetime(2024, 1, 1, 12, 0, 0),
                updated_at=datetime(2024, 1, 1, 12, 0, 0),
            )
        ]
        mock_repository.search.return_value = products

        # Act
        response = await use_case.execute(request)

        # Assert
        assert isinstance(response, SearchProductsResponse)
        assert len(response.products) == 1
        assert response.total_count == 1
        assert response.search_criteria["name"] == "laptop"
        assert response.search_criteria["min_price"] == 100000
        assert response.search_criteria["max_price"] == 200000

        mock_repository.search.assert_called_once_with(
            name="laptop", min_price=100000, max_price=200000, skip=0, limit=10
        )

    @pytest.mark.asyncio
    async def test_search_by_name_only(self):
        """Test search by name only."""
        # Arrange
        mock_repository = AsyncMock()
        use_case = SearchProductsUseCase(mock_repository)

        request = SearchProductsRequest(name="laptop", skip=0, limit=10)

        products = []
        mock_repository.search.return_value = products

        # Act
        response = await use_case.execute(request)

        # Assert
        assert isinstance(response, SearchProductsResponse)
        assert len(response.products) == 0
        assert response.search_criteria["name"] == "laptop"

        mock_repository.search.assert_called_once_with(
            name="laptop", min_price=None, max_price=None, skip=0, limit=10
        )

    @pytest.mark.asyncio
    async def test_search_by_price_range_only(self):
        """Test search by price range only."""
        # Arrange
        mock_repository = AsyncMock()
        use_case = SearchProductsUseCase(mock_repository)

        request = SearchProductsRequest(
            min_price=100000, max_price=200000, skip=0, limit=10
        )

        products = []
        mock_repository.search.return_value = products

        # Act
        response = await use_case.execute(request)

        # Assert
        assert isinstance(response, SearchProductsResponse)
        assert len(response.products) == 0
        assert response.search_criteria["min_price"] == 100000
        assert response.search_criteria["max_price"] == 200000

        mock_repository.search.assert_called_once_with(
            name=None, min_price=100000, max_price=200000, skip=0, limit=10
        )

    @pytest.mark.asyncio
    async def test_search_no_criteria(self):
        """Test search with no criteria (returns all products)."""
        # Arrange
        mock_repository = AsyncMock()
        use_case = SearchProductsUseCase(mock_repository)

        request = SearchProductsRequest(skip=0, limit=10)

        products = []
        mock_repository.find_all.return_value = products

        # Act
        response = await use_case.execute(request)

        # Assert
        assert isinstance(response, SearchProductsResponse)
        assert len(response.products) == 0
        assert len(response.search_criteria) == 0

        mock_repository.find_all.assert_called_once_with(skip=0, limit=10)
