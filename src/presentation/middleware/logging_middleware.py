"""Logging middleware configuration.

This module handles request/response logging middleware for the application.
"""

import time
from typing import Callable
from uuid import uuid4

import structlog
from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = structlog.get_logger()


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging HTTP requests and responses."""

    async def dispatch(
        self,
        request: Request,
        call_next: Callable,
    ) -> Response:
        """
        Process the request and log relevant information.

        Args:
            request: The incoming HTTP request
            call_next: The next middleware or route handler

        Returns:
            The HTTP response
        """
        # Generate unique request ID
        request_id = str(uuid4())
        start_time = time.time()

        # Add request ID to the request state
        request.state.request_id = request_id

        # Log incoming request
        logger.info(
            "Incoming request",
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            query_params=dict(request.query_params),
            client_ip=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
        )

        # Process the request
        try:
            response = await call_next(request)
            process_time = time.time() - start_time

            # Log successful response
            logger.info(
                "Request completed",
                request_id=request_id,
                method=request.method,
                path=request.url.path,
                status_code=response.status_code,
                process_time_ms=round(process_time * 1000, 2),
            )

            # Add request ID to response headers
            response.headers["X-Request-ID"] = request_id

            return response

        except Exception as exc:
            process_time = time.time() - start_time

            # Log error
            logger.error(
                "Request failed",
                request_id=request_id,
                method=request.method,
                path=request.url.path,
                error=str(exc),
                process_time_ms=round(process_time * 1000, 2),
                exc_info=True,
            )

            # Re-raise the exception to be handled by error handlers
            raise


class PerformanceLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging slow requests."""

    def __init__(self, app, slow_request_threshold: float = 1.0):
        """
        Initialize the performance logging middleware.

        Args:
            app: The ASGI application
            slow_request_threshold: Threshold in seconds
        """
        super().__init__(app)
        self.slow_request_threshold = slow_request_threshold

    async def dispatch(
        self,
        request: Request,
        call_next: Callable,
    ) -> Response:
        """
        Process the request and log performance metrics.

        Args:
            request: The incoming HTTP request
            call_next: The next middleware or route handler

        Returns:
            The HTTP response
        """
        start_time = time.time()

        response = await call_next(request)

        process_time = time.time() - start_time

        # Log slow requests
        if process_time > self.slow_request_threshold:
            logger.warning(
                "Slow request detected",
                method=request.method,
                path=request.url.path,
                process_time_ms=round(process_time * 1000, 2),
                threshold_ms=round(self.slow_request_threshold * 1000, 2),
            )

        return response


def setup_logging_middleware(app: FastAPI) -> None:
    """
    Configure logging middleware for the FastAPI application.

    Args:
        app: The FastAPI application instance
    """
    logger.info("Setting up logging middleware")

    # Add request logging middleware
    app.add_middleware(RequestLoggingMiddleware)

    # Add performance logging middleware
    app.add_middleware(
        PerformanceLoggingMiddleware,
        slow_request_threshold=1.0,
    )

    logger.info("Logging middleware configured successfully")


def setup_simple_logging_middleware(app: FastAPI) -> None:
    """
    Configure simple logging middleware for development.

    Args:
        app: The FastAPI application instance
    """

    @app.middleware("http")
    async def simple_log_requests(request: Request, call_next):
        """Simple request logging for development."""
        logger.info(
            "Request",
            method=request.method,
            path=request.url.path,
        )

        response = await call_next(request)

        logger.info(
            "Response",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
        )

        return response
