from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.crud.crud_product import product
from app.schemas.product import Product, ProductCreate, ProductUpdate, ProductSearchResponse
import math

router = APIRouter()

@router.get("/", response_model=List[Product])
def get_products(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all products with pagination"""
    products = product.get_multi(db, skip=skip, limit=limit)
    return [Product.from_orm(p) for p in products]

@router.get("/search", response_model=ProductSearchResponse)
def search_products(
    q: str = Query(..., description="Search query"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """Search products by title, description, category, or brand"""
    skip = (page - 1) * per_page
    
    # Get search results
    products = product.search(db, query=q, skip=skip, limit=per_page)
    
    # Get total count for pagination
    total = product.count_search(db, query=q)
    total_pages = math.ceil(total / per_page)
    
    return ProductSearchResponse(
        products=[Product.from_orm(p) for p in products],
        total=total,
        page=page,
        per_page=per_page,
        total_pages=total_pages
    )

@router.get("/category/{category}", response_model=List[Product])
def get_products_by_category(
    category: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get products by category"""
    products = product.get_by_category(db, category=category, skip=skip, limit=limit)
    return [Product.from_orm(p) for p in products]

@router.get("/{product_id}", response_model=Product)
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific product by ID"""
    db_product = product.get(db, id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return Product.from_orm(db_product)

@router.post("/", response_model=Product)
def create_product(
    product_in: ProductCreate,
    db: Session = Depends(get_db)
):
    """Create a new product"""
    return product.create(db, obj_in=product_in)

@router.put("/{product_id}", response_model=Product)
def update_product(
    product_id: int,
    product_in: ProductUpdate,
    db: Session = Depends(get_db)
):
    """Update a product"""
    db_product = product.get(db, id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product.update(db, db_obj=db_product, obj_in=product_in)

@router.delete("/{product_id}", response_model=Product)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    """Delete a product"""
    db_product = product.get(db, id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product.remove(db, id=product_id)
