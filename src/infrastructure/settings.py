"""
Application settings configuration.

This module contains the application settings configuration
separate from database settings to avoid conflicts.
"""

from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    """Application settings configuration."""

    # Application settings
    debug: bool = False
    log_level: str = "INFO"
    host: str = "0.0.0.0"
    port: int = 8000

    # Database settings
    database_url: str = "mysql+pymysql://product_user:product_password@localhost:3306/product_management"  # noqa: E501

    # MySQL settings (for Docker)
    mysql_root_password: str = "root_password"
    mysql_database: str = "product_management"
    mysql_user: str = "product_user"
    mysql_password: str = "product_password"

    # Redis settings (for future use)
    redis_url: str = "redis://localhost:6379"

    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
        "extra": "ignore",  # Ignore extra environment variables
    }


# Create global settings instance
app_settings = AppSettings()
