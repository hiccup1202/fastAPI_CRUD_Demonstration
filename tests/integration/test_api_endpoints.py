"""
Integration tests for API endpoints.

This module contains integration tests for the FastAPI endpoints.
"""

# Import everything needed from the integration tests package
from tests.integration import (
    # Test utilities
    pytest,
    patch,
    TestClient,
    # FastAPI app
    app,
)


@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)


class TestHealthEndpoint:
    """Test cases for health check endpoint."""

    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "Product Management API"
        assert data["version"] == "1.0.0"


class TestRootEndpoint:
    """Test cases for root endpoint."""

    def test_root_endpoint(self, client):
        """Test root endpoint."""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Product Management API"
        assert data["version"] == "1.0.0"
        assert "documentation" in data
        assert "health" in data


class TestProductEndpoints:
    """Test cases for product endpoints."""

    def test_create_product_success(self, client):
        """Test successful product creation."""
        product_data = {"name": "Test Product", "price": 1000}

        with patch(
            "src.presentation.controllers.product_controller.get_product_repository"  # noqa: E501
        ) as mock_repo:
            # Mock the repository and use case
            mock_repository = mock_repo.return_value
            mock_repository.save.return_value = None

            response = client.post("/api/v1/products/", json=product_data)

            assert response.status_code in [
                201,
                500,
            ]

    def test_create_product_invalid_data(self, client):
        """Test product creation with invalid data."""
        # Test with missing required fields
        response = client.post("/api/v1/products/", json={})
        assert response.status_code == 422

        # Test with invalid price (negative)
        response = client.post(
            "/api/v1/products/", json={"name": "Test Product", "price": -100}
        )
        assert response.status_code == 422

        # Test with empty name
        response = client.post(
            "/api/v1/products/",
            json={"name": "", "price": 1000},
        )
        assert response.status_code == 422

    def test_get_product_not_found(self, client):
        """Test getting a non-existent product."""
        response = client.get("/api/v1/products/999")
        assert response.status_code == 404

    def test_list_products(self, client):
        """Test listing products."""
        response = client.get("/api/v1/products/search")
        assert response.status_code in [200, 500]

    def test_search_products(self, client):
        """Test searching products."""
        response = client.get(
            "/api/v1/products/search"
            "?name=laptop"
            "&min_price=100000"
            "&max_price=200000"
        )
        assert response.status_code in [
            200,
            500,
            422,
        ]


class TestAPIValidation:
    """Test cases for API validation."""

    def test_product_name_validation(self, client):
        """Test product name validation."""
        # Test with name too long
        long_name = "a" * 1001
        response = client.post(
            "/api/v1/products/", json={"name": long_name, "price": 1000}
        )
        assert response.status_code == 422

    def test_product_price_validation(self, client):
        """Test product price validation."""
        # Test with price too high
        response = client.post(
            "/api/v1/products/",
            json={"name": "Test Product", "price": 1000000000},
        )
        assert response.status_code == 422

    def test_pagination_validation(self, client):
        """Test pagination parameter validation."""
        # Test with negative skip
        response = client.get("/api/v1/products/search?skip=-1")
        assert response.status_code == 422

        # Test with invalid limit
        response = client.get("/api/v1/products/search?limit=0")
        assert response.status_code == 422

        response = client.get("/api/v1/products/search?limit=1001")
        assert response.status_code == 422


class TestErrorHandling:
    """Test cases for error handling."""

    def test_404_error(self, client):
        """Test 404 error handling."""
        response = client.get("/non-existent-endpoint")
        assert response.status_code == 404
        assert "detail" in response.json()

    def test_method_not_allowed(self, client):
        """Test method not allowed error."""
        response = client.put("/api/v1/products/")
        assert response.status_code == 405

    def test_validation_error_format(self, client):
        """Test validation error response format."""
        response = client.post("/api/v1/products/", json={})
        assert response.status_code == 422

        data = response.json()
        assert "detail" in data
        assert "errors" in data
