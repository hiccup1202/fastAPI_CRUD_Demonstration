"""Exception handlers for the FastAPI application.

This module provides centralized exception handling for all types of errors.
"""

import structlog
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from .custom_exceptions import (
    AuthenticationError,
    AuthorizationError,
    BusinessLogicError,
    ExternalServiceError,
    ResourceNotFoundError,
    ValidationError,
)

logger = structlog.get_logger()


def setup_exception_handlers(app: FastAPI) -> None:
    """
    Configure all exception handlers for the FastAPI application.

    Args:
        app: The FastAPI application instance
    """
    logger.info("Setting up exception handlers")

    # Register all custom exception handlers
    app.exception_handler(StarletteHTTPException)(http_exception_handler)
    app.exception_handler(RequestValidationError)(validation_exception_handler)
    app.exception_handler(BusinessLogicError)(business_logic_exception_handler)
    app.exception_handler(ResourceNotFoundError)(
        resource_not_found_exception_handler,
    )
    app.exception_handler(ValidationError)(custom_validation_exception_handler)
    app.exception_handler(AuthenticationError)(
        authentication_exception_handler,
    )
    app.exception_handler(AuthorizationError)(authorization_exception_handler)
    app.exception_handler(ExternalServiceError)(
        external_service_exception_handler,
    )
    app.exception_handler(Exception)(general_exception_handler)

    logger.info("Exception handlers configured successfully")


async def http_exception_handler(
    request: Request,
    exc: StarletteHTTPException,
) -> JSONResponse:
    """
    Handle HTTP exceptions from Starlette/FastAPI.

    Args:
        request: The HTTP request
        exc: The HTTP exception

    Returns:
        JSON response with error details
    """
    request_id = getattr(request.state, "request_id", None)

    logger.warning(
        "HTTP exception occurred",
        request_id=request_id,
        status_code=exc.status_code,
        detail=exc.detail,
        path=request.url.path,
        method=request.method,
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "HTTP Exception",
            "detail": exc.detail,
            "status_code": exc.status_code,
            "request_id": request_id,
        },
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    """
    Handle FastAPI validation exceptions.

    Args:
        request: The HTTP request
        exc: The validation exception

    Returns:
        JSON response with validation error details
    """
    request_id = getattr(request.state, "request_id", None)

    logger.warning(
        "Validation error occurred",
        request_id=request_id,
        errors=exc.errors(),
        path=request.url.path,
        method=request.method,
    )

    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation Error",
            "detail": "Request validation failed",
            "errors": exc.errors(),
            "request_id": request_id,
        },
    )


async def business_logic_exception_handler(
    request: Request,
    exc: BusinessLogicError,
) -> JSONResponse:
    """
    Handle business logic exceptions.

    Args:
        request: The HTTP request
        exc: The business logic exception

    Returns:
        JSON response with business logic error details
    """
    request_id = getattr(request.state, "request_id", None)

    logger.warning(
        "Business logic error occurred",
        request_id=request_id,
        message=exc.message,
        error_code=exc.error_code,
        details=exc.details,
        path=request.url.path,
        method=request.method,
    )

    content = {
        "error": "Business Logic Error",
        "detail": exc.message,
        "request_id": request_id,
    }

    if exc.error_code:
        content["error_code"] = exc.error_code

    if exc.details:
        content["details"] = exc.details

    return JSONResponse(
        status_code=400,
        content=content,
    )


async def resource_not_found_exception_handler(
    request: Request,
    exc: ResourceNotFoundError,
) -> JSONResponse:
    """
    Handle resource not found exceptions.

    Args:
        request: The HTTP request
        exc: The resource not found exception

    Returns:
        JSON response with not found error details
    """
    request_id = getattr(request.state, "request_id", None)

    logger.warning(
        "Resource not found",
        request_id=request_id,
        resource_type=exc.resource_type,
        resource_id=exc.resource_id,
        path=request.url.path,
        method=request.method,
    )

    return JSONResponse(
        status_code=404,
        content={
            "error": "Resource Not Found",
            "detail": exc.message,
            "resource_type": exc.resource_type,
            "resource_id": str(exc.resource_id),
            "request_id": request_id,
        },
    )


async def custom_validation_exception_handler(
    request: Request,
    exc: ValidationError,
) -> JSONResponse:
    """
    Handle custom validation exceptions.

    Args:
        request: The HTTP request
        exc: The validation exception

    Returns:
        JSON response with validation error details
    """
    request_id = getattr(request.state, "request_id", None)

    logger.warning(
        "Custom validation error occurred",
        request_id=request_id,
        message=exc.message,
        field=exc.field,
        value=exc.value,
        details=exc.details,
        path=request.url.path,
        method=request.method,
    )

    content = {
        "error": "Validation Error",
        "detail": exc.message,
        "request_id": request_id,
    }

    if exc.field:
        content["field"] = exc.field

    if exc.details:
        content["details"] = exc.details

    return JSONResponse(
        status_code=422,
        content=content,
    )


async def authentication_exception_handler(
    request: Request,
    exc: AuthenticationError,
) -> JSONResponse:
    """
    Handle authentication exceptions.

    Args:
        request: The HTTP request
        exc: The authentication exception

    Returns:
        JSON response with authentication error details
    """
    request_id = getattr(request.state, "request_id", None)

    logger.warning(
        "Authentication error occurred",
        request_id=request_id,
        message=exc.message,
        path=request.url.path,
        method=request.method,
    )

    return JSONResponse(
        status_code=401,
        content={
            "error": "Authentication Error",
            "detail": exc.message,
            "request_id": request_id,
        },
    )


async def authorization_exception_handler(
    request: Request,
    exc: AuthorizationError,
) -> JSONResponse:
    """
    Handle authorization exceptions.

    Args:
        request: The HTTP request
        exc: The authorization exception

    Returns:
        JSON response with authorization error details
    """
    request_id = getattr(request.state, "request_id", None)

    logger.warning(
        "Authorization error occurred",
        request_id=request_id,
        message=exc.message,
        path=request.url.path,
        method=request.method,
    )

    return JSONResponse(
        status_code=403,
        content={
            "error": "Authorization Error",
            "detail": exc.message,
            "request_id": request_id,
        },
    )


async def external_service_exception_handler(
    request: Request,
    exc: ExternalServiceError,
) -> JSONResponse:
    """
    Handle external service exceptions.

    Args:
        request: The HTTP request
        exc: The external service exception

    Returns:
        JSON response with external service error details
    """
    request_id = getattr(request.state, "request_id", None)

    logger.error(
        "External service error occurred",
        request_id=request_id,
        service_name=exc.service_name,
        message=exc.message,
        status_code=exc.status_code,
        response_data=exc.response_data,
        path=request.url.path,
        method=request.method,
    )

    return JSONResponse(
        status_code=502,
        content={
            "error": "External Service Error",
            "detail": f"'{exc.service_name}' error: {exc.message}",
            "service_name": exc.service_name,
            "request_id": request_id,
        },
    )


async def general_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """
    Handle all other unhandled exceptions.

    Args:
        request: The HTTP request
        exc: The unhandled exception

    Returns:
        JSON response with generic error details
    """
    request_id = getattr(request.state, "request_id", None)

    logger.error(
        "Unexpected error occurred",
        request_id=request_id,
        error=str(exc),
        error_type=type(exc).__name__,
        path=request.url.path,
        method=request.method,
        exc_info=True,
    )

    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": "An unexpected error occurred",
            "request_id": request_id,
        },
    )
