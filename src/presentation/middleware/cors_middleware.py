"""CORS middleware configuration.

This module handles Cross-Origin Resource Sharing (CORS) middleware setup.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import structlog

logger = structlog.get_logger()


def setup_cors_middleware(app: FastAPI) -> None:
    """
    Configure CORS middleware for the FastAPI application.

    Args:
        app: The FastAPI application instance
    """
    logger.info("Setting up CORS middleware")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    logger.info("CORS middleware configured successfully")


def setup_production_cors_middleware(
    app: FastAPI,
    allowed_origins: list[str],
) -> None:
    """
    Configure CORS middleware with production-safe settings.

    Args:
        app: The FastAPI application instance
        allowed_origins: List of allowed origins for CORS
    """
    logger.info(
        "Setting up production CORS middleware",
        allowed_origins=allowed_origins,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=[
            "Content-Type",
            "Authorization",
            "Accept",
            "Origin",
            "X-Requested-With",
        ],
        expose_headers=["X-Total-Count"],
    )

    logger.info("Production CORS middleware configured successfully")
