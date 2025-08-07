"""Custom exception classes.

This module defines custom exceptions used throughout the application.
"""

from typing import Any, Dict, Optional


class BusinessLogicError(Exception):
    """Exception raised for business logic violations."""

    def __init__(
        self,
        message: str,
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize the business logic error.

        Args:
            message: Human-readable error message
            error_code: Machine-readable error code
            details: Additional error details
        """
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)


class ResourceNotFoundError(Exception):
    """Exception raised when a requested resource is not found."""

    def __init__(
        self,
        resource_type: str,
        resource_id: Any,
        message: Optional[str] = None,
    ):
        """
        Initialize the resource not found error.

        Args:
            resource_type: The type of resource that was not found
            resource_id: The identifier of the resource
            message: Optional custom message
        """
        self.resource_type = resource_type
        self.resource_id = resource_id
        self.message = (
            message or f"{resource_type} with ID {resource_id} not found"
        )  # noqa: E501
        super().__init__(self.message)


class ValidationError(Exception):
    """Exception raised for validation errors."""

    def __init__(
        self,
        message: str,
        field: Optional[str] = None,
        value: Optional[Any] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize the validation error.

        Args:
            message: Human-readable error message
            field: The field that failed validation
            value: The invalid value
            details: Additional validation details
        """
        self.message = message
        self.field = field
        self.value = value
        self.details = details or {}
        super().__init__(self.message)


class AuthenticationError(Exception):
    """Exception raised for authentication failures."""

    def __init__(self, message: str = "Authentication failed"):
        """
        Initialize the authentication error.

        Args:
            message: Human-readable error message
        """
        self.message = message
        super().__init__(self.message)


class AuthorizationError(Exception):
    """Exception raised for authorization failures."""

    def __init__(self, message: str = "Insufficient permissions"):
        """
        Initialize the authorization error.

        Args:
            message: Human-readable error message
        """
        self.message = message
        super().__init__(self.message)


class ExternalServiceError(Exception):
    """Exception raised when external service calls fail."""

    def __init__(
        self,
        service_name: str,
        message: str,
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize the external service error.

        Args:
            service_name: Name of the external service
            message: Human-readable error message
            status_code: HTTP status code from the service
            response_data: Response data from the service
        """
        self.service_name = service_name
        self.message = message
        self.status_code = status_code
        self.response_data = response_data or {}
        super().__init__(self.message)
