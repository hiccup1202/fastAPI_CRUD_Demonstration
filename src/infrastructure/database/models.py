"""
Database models.

This module contains the SQLAlchemy models for the infrastructure layer.
"""


from sqlalchemy import BigInteger, Column, DateTime, Integer, Text, func
from sqlalchemy.sql import text

from .config import Base


class ProductModel(Base):
    """
    Product database model.

    This model represents the product table in the database.
    It maps the domain entity to the database schema.
    """

    __tablename__ = "products"

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    name = Column(Text, nullable=False, index=True)
    price = Column(Integer, nullable=False, index=True)
    created_at = Column(
        DateTime,
        nullable=False,
        default=func.current_timestamp,
        server_default=text("CURRENT_TIMESTAMP"),
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        default=func.current_timestamp,
        onupdate=func.current_timestamp,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
    )

    def __repr__(self) -> str:
        """String representation of the model."""
        return (
            f"ProductModel("
            f"id={self.id}, "
            f"name='{self.name}', "
            f"price={self.price}, "
            f"created_at={self.created_at}, "
            f"updated_at={self.updated_at}"
            f")"
        )
