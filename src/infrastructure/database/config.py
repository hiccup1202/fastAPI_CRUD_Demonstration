"""
Database configuration.

This module contains the database configuration and setup
for the infrastructure layer.
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import QueuePool

from ..settings import app_settings

# Database settings
db_settings = type(
    "DatabaseSettings",
    (),
    {
        "database_url": app_settings.database_url,
        "echo": False,
        "pool_size": 10,
        "max_overflow": 20,
        "pool_timeout": 30,
        "pool_recycle": 3600,
    },
)()

# Create engine
engine = create_engine(
    db_settings.database_url,
    echo=db_settings.echo,
    poolclass=QueuePool,
    pool_size=db_settings.pool_size,
    max_overflow=db_settings.max_overflow,
    pool_timeout=db_settings.pool_timeout,
    pool_recycle=db_settings.pool_recycle,
    pool_pre_ping=True,
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()


def get_database_session():
    """
    Get a database session.

    Returns:
        Database session
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_database_url() -> str:
    """
    Get the database URL from environment or settings.

    Returns:
        Database URL string
    """
    return os.getenv("DATABASE_URL", db_settings.database_url)
