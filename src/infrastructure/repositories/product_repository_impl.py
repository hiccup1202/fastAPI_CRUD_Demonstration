"""
Product Repository implementation.

This module contains the SQLAlchemy implementation of the ProductRepository
interface for the infrastructure layer.
"""

from datetime import datetime
from typing import List, Optional, cast

from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from ...domain.entities.product import Product
from ...domain.repositories.product_repository import ProductRepository
from ...domain.value_objects.price import Price
from ...domain.value_objects.product_id import ProductId
from ...domain.value_objects.product_name import ProductName
from ..database.config import SessionLocal
from ..database.models import ProductModel


class SQLAlchemyProductRepository(ProductRepository):
    """
    SQLAlchemy implementation of ProductRepository.

    This class implements the ProductRepository interface using SQLAlchemy
    for database operations.
    """

    def __init__(self, session: Session):
        """
        Initialize the repository.

        Args:
            session: SQLAlchemy database session
        """
        self.session = session

    async def save(self, product: Product) -> Product:
        """
        Save a product to the database.

        Args:
            product: The product to save

        Returns:
            The saved product with generated ID
        """
        # Convert domain entity to database model
        product_model = ProductModel(
            id=product.id.value if product.id is not None else None,
            name=str(product.name),
            price=product.price.value,
            created_at=product.created_at,
            updated_at=product.updated_at,
        )

        # Save to database
        self.session.add(product_model)
        self.session.commit()
        self.session.refresh(product_model)

        # Convert back to domain entity
        return self._to_domain_entity(product_model)

    async def find_by_id(self, product_id: ProductId) -> Optional[Product]:
        """
        Find a product by its ID.

        Args:
            product_id: The product ID to search for

        Returns:
            The product if found, None otherwise
        """
        product_model = (
            self.session.query(ProductModel)
            .filter(ProductModel.id == product_id.value)
            .first()
        )

        if product_model is None:
            return None

        return self._to_domain_entity(product_model)

    async def find_all(self, skip: int = 0, limit: int = 100) -> List[Product]:
        """
        Find all products with pagination.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of products
        """
        product_models = (
            self.session.query(ProductModel).offset(skip).limit(limit).all()
        )

        return [self._to_domain_entity(model) for model in product_models]

    async def update(self, product: Product) -> Product:
        """
        Update an existing product.

        Args:
            product: The product to update

        Returns:
            The updated product
        """
        if product.id is None:
            raise ValueError("Cannot update product without ID")
        product_model = (
            self.session.query(ProductModel)
            .filter(ProductModel.id == product.id.value)
            .first()
        )

        if product_model is None:
            raise ValueError(f"Product with ID {product.id.value} not found")

        # Update fields
        product_model.name = str(product.name)  # type: ignore[assignment]
        product_model.price = product.price.value  # type: ignore[assignment]
        product_model.updated_at = product.updated_at  # type: ignore

        # Save changes
        self.session.commit()
        self.session.refresh(product_model)

        return self._to_domain_entity(product_model)

    async def delete(self, product_id: ProductId) -> bool:
        """
        Delete a product by its ID.

        Args:
            product_id: The product ID to delete

        Returns:
            True if the product was deleted, False if it didn't exist
        """
        product_model = (
            self.session.query(ProductModel)
            .filter(ProductModel.id == product_id.value)
            .first()
        )

        if product_model is None:
            return False

        self.session.delete(product_model)
        self.session.commit()

        return True

    async def search(
        self,
        name: Optional[str] = None,
        min_price: Optional[int] = None,
        max_price: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Product]:
        """
        Search products by name and/or price range.

        Args:
            name: Product name (case-insensitive partial match), optional
            min_price: Minimum price (inclusive), optional
            max_price: Maximum price (inclusive), optional
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of matching products
        """
        query = self.session.query(ProductModel)

        # Apply filters based on provided criteria
        filters = []

        if name is not None:
            lower_name = func.lower(name)
            name_filter = func.lower(ProductModel.name).contains(lower_name)
            filters.append(name_filter)

        if min_price is not None:
            filters.append(ProductModel.price >= min_price)

        if max_price is not None:
            filters.append(ProductModel.price <= max_price)

        # Apply all filters if any exist
        if filters:
            query = query.filter(and_(*filters))

        # Apply pagination
        product_models = query.offset(skip).limit(limit).all()

        return [self._to_domain_entity(model) for model in product_models]

    def _to_domain_entity(self, model: ProductModel) -> Product:
        """
        Convert database model to domain entity.

        Args:
            model: Database model

        Returns:
            Domain entity
        """
        # Convert model fields to proper types for domain entity
        model_id = cast(int, model.id)
        model_name = cast(str, model.name)
        model_price = cast(int, model.price)
        product_id = ProductId(model_id) if model_id is not None else None
        product_name = ProductName(model_name)
        product_price = Price(model_price)

        # SQLAlchemy models return proper datetime objects at runtime
        created_at = cast(datetime, model.created_at)
        updated_at = cast(datetime, model.updated_at)

        return Product(
            id=product_id,
            name=product_name,
            price=product_price,
            created_at=created_at,
            updated_at=updated_at,
        )


def get_product_repository() -> SQLAlchemyProductRepository:
    """
    Get a product repository instance.

    Returns:
        Product repository instance
    """
    session = SessionLocal()
    return SQLAlchemyProductRepository(session)
