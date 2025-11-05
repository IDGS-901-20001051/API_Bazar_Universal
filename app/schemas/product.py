from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class ProductBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    category: str
    brand: Optional[str] = None
    rating: Optional[float] = 0.0
    stock: Optional[int] = 0
    images: Optional[List[str]] = []
    features: Optional[List[str]] = []

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    brand: Optional[str] = None
    rating: Optional[float] = None
    stock: Optional[int] = None
    images: Optional[List[str]] = None
    features: Optional[List[str]] = None

class Product(ProductBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        
    @classmethod
    def from_orm(cls, obj):
        # Handle JSON fields for SQLite compatibility
        import json
        data = {
            'id': obj.id,
            'title': obj.title,
            'description': obj.description,
            'price': obj.price,
            'category': obj.category,
            'brand': obj.brand,
            'rating': obj.rating,
            'stock': obj.stock,
            'created_at': obj.created_at,
            'updated_at': obj.updated_at,
            'images': json.loads(obj.images) if obj.images else [],
            'features': json.loads(obj.features) if obj.features else []
        }
        return cls(**data)

class ProductSearchResponse(BaseModel):
    products: List[Product]
    total: int
    page: int
    per_page: int
    total_pages: int
