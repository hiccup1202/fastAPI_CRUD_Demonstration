"""
Product Controller.

This module contains the FastAPI controller for product endpoints.
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field

from ...application import (
    CreateProductRequest,
    CreateProductUseCase,
    DeleteProductRequest,
    DeleteProductUseCase,
    GetProductRequest,
    GetProductUseCase,
    SearchProductsRequest,
    SearchProductsUseCase,
    UpdateProductRequest,
    UpdateProductUseCase,
)
from ...infrastructure import get_product_repository


# Pydantic models for API requests and responses
class CreateProductRequestModel(BaseModel):
    """Request model for creating a product."""

    name: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="Product name",
    )
    price: int = Field(
        ...,
        ge=0,
        le=999999999,
        description="Product price in yen",
    )


class ProductResponseModel(BaseModel):
    """Response model for product data."""

    id: int = Field(..., description="Product ID")
    name: str = Field(..., description="Product name")
    price: int = Field(..., description="Product price in yen")
    created_at: str = Field(..., description="Creation timestamp")
    updated_at: str = Field(..., description="Last update timestamp")

    model_config = {"from_attributes": True}


class UpdateProductRequestModel(BaseModel):
    """Request model for updating a product."""

    name: Optional[str] = Field(
        None, min_length=1, max_length=1000, description="Product name"
    )
    price: Optional[int] = Field(
        None, ge=0, le=999999999, description="Product price in yen"
    )


class DeleteProductResponseModel(BaseModel):
    """Response model for deleting a product."""

    success: bool = Field(
        ...,
        description="Whether the deletion was successful",
    )
    message: str = Field(
        ...,
        description="Response message",
    )


class ProductSearchResponseModel(BaseModel):
    """Response model for product search."""

    products: List[ProductResponseModel] = Field(
        ..., description="List of matching products"
    )
    total_count: int = Field(
        ...,
        description="Total number of matching products",
    )
    skip: int = Field(..., description="Number of records skipped")
    limit: int = Field(..., description="Maximum number of records returned")
    search_criteria: dict = Field(..., description="Search criteria used")


# Create router
router = APIRouter(prefix="/api/v1/products", tags=["products"])


@router.get("/search", response_model=ProductSearchResponseModel)
async def search_products(
    name: Optional[str] = Query(
        None,
        description="Product name (partial match)",
    ),
    min_price: Optional[int] = Query(
        None, ge=0, description="Minimum price (inclusive)"
    ),
    max_price: Optional[int] = Query(
        None, ge=0, description="Maximum price (inclusive)"
    ),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(
        100, ge=1, le=1000, description="Maximum number of records to return"
    ),
    product_repository=Depends(get_product_repository),
) -> ProductSearchResponseModel:
    """
    Search products by name and/or price range, or list all products.

    This endpoint can be used for both searching and listing:
    - With search criteria: Returns products matching the criteria

    Args:
        name: Product name to search for (case-insensitive partial match)
        min_price: Minimum price (inclusive)
        max_price: Maximum price (inclusive)
        skip: Number of records to skip
        limit: Maximum number of records to return
        product_repository: Product repository dependency

    Returns:
        List of products with search criteria and pagination info
    """
    try:
        use_case = SearchProductsUseCase(product_repository)
        response = await use_case.execute(
            SearchProductsRequest(
                name=name,
                min_price=min_price,
                max_price=max_price,
                skip=skip,
                limit=limit,
            )
        )

        return ProductSearchResponseModel(
            products=[
                ProductResponseModel(
                    id=product.id,
                    name=product.name,
                    price=product.price,
                    created_at=product.created_at,
                    updated_at=product.updated_at,
                )
                for product in response.products
            ],
            total_count=response.total_count,
            skip=response.skip,
            limit=response.limit,
            search_criteria=response.search_criteria,
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/", response_model=ProductResponseModel, status_code=201)
async def create_product(
    request: CreateProductRequestModel,
    product_repository=Depends(get_product_repository),
) -> ProductResponseModel:
    """
    Create a new product.

    Args:
        request: Product creation request
        product_repository: Product repository dependency

    Returns:
        Created product data

    Raises:
        HTTPException: If the request data is invalid
    """
    try:
        use_case = CreateProductUseCase(product_repository)
        response = await use_case.execute(
            CreateProductRequest(name=request.name, price=request.price)
        )

        return ProductResponseModel(
            id=response.id,
            name=response.name,
            price=response.price,
            created_at=response.created_at,
            updated_at=response.updated_at,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{product_id}", response_model=ProductResponseModel)
async def get_product(
    product_id: int, product_repository=Depends(get_product_repository)
) -> ProductResponseModel:
    """
    Get a product by ID.

    Args:
        product_id: Product ID
        product_repository: Product repository dependency

    Returns:
        Product data

    Raises:
        HTTPException: If the product is not found
    """
    try:
        use_case = GetProductUseCase(product_repository)
        response = await use_case.execute(
            GetProductRequest(product_id=product_id),
        )

        if response is None:
            raise HTTPException(
                status_code=404,
                detail=f"Product with ID {product_id} not found",
            )

        return ProductResponseModel(
            id=response.id,
            name=response.name,
            price=response.price,
            created_at=response.created_at,
            updated_at=response.updated_at,
        )
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put("/{product_id}", response_model=ProductResponseModel)
async def update_product(
    product_id: int,
    request: UpdateProductRequestModel,
    product_repository=Depends(get_product_repository),
) -> ProductResponseModel:
    """
    Update an existing product.

    Args:
        product_id: Product ID
        request: Product update request
        product_repository: Product repository dependency

    Returns:
        Updated product data

    Raises:
        HTTPException: If the product is not found or request data is invalid
    """
    try:
        use_case = UpdateProductUseCase(product_repository)
        response = await use_case.execute(
            UpdateProductRequest(
                product_id=product_id, name=request.name, price=request.price
            )
        )

        if response is None:
            raise HTTPException(
                status_code=404,
                detail=f"Product with ID {product_id} not found",
            )

        return ProductResponseModel(
            id=response.id,
            name=response.name,
            price=response.price,
            created_at=response.created_at,
            updated_at=response.updated_at,
        )
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/{product_id}", response_model=DeleteProductResponseModel)
async def delete_product(
    product_id: int, product_repository=Depends(get_product_repository)
) -> DeleteProductResponseModel:
    """
    Delete an existing product.

    Args:
        product_id: Product ID
        product_repository: Product repository dependency

    Returns:
        Deletion result
    """
    try:
        use_case = DeleteProductUseCase(product_repository)
        response = await use_case.execute(
            DeleteProductRequest(product_id=product_id),
        )

        if response is None:
            raise HTTPException(
                status_code=404,
                detail=f"Product with ID {product_id} not found",
            )

        return DeleteProductResponseModel(
            success=response.success, message=response.message
        )
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")
