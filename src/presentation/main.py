"""
Main application.

This module sets up the App with separated middleware and error handling.
"""

from contextlib import asynccontextmanager

import structlog
import uvicorn
from fastapi import FastAPI

from ..infrastructure import engine, Base
from ..infrastructure.settings import app_settings
from .controllers import product_router
from .error_handlers import setup_exception_handlers
from .middleware import setup_cors_middleware, setup_logging_middleware

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer(),
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.

    Handles startup and shutdown events for the FastAPI application.
    """
    # Startup
    logger.info("Starting Product Management API")

    # Create database tables
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error("Failed to create database tables", error=str(e))
        raise

    yield

    # Shutdown
    logger.info("Shutting down Product Management API")


# Create FastAPI application
app = FastAPI(
    title="Product Management API",
    description="A full-stack product management system",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# Setup middleware
setup_cors_middleware(app)
setup_logging_middleware(app)

# Setup exception handlers
setup_exception_handlers(app)


# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint.

    Returns:
        Health status of the application
    """
    return {
        "status": "healthy",
        "service": "Product Management API",
        "version": "1.0.0",
    }


# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint.

    Returns:
        API information and links
    """
    return {
        "message": "Product Management API",
        "version": "1.0.0",
        "description": "A full-stack product management system",
        "documentation": "/docs",
        "redoc": "/redoc",
        "health": "/health",
    }


# Include routers
app.include_router(product_router)


if __name__ == "__main__":
    # Get configuration from settings
    host = app_settings.host
    port = app_settings.port
    reload = app_settings.debug

    # Run the application
    uvicorn.run(
        "src.presentation.main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info",
    )
