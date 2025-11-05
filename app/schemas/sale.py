from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class SaleBase(BaseModel):
    product_id: int
    quantity: int = 1

class SaleCreate(SaleBase):
    pass

class Sale(BaseModel):
    id: int
    product_id: int
    product_title: str
    product_image: Optional[str] = None
    quantity: int
    price: float
    total: float
    status: str = "Completada"
    date: datetime

    class Config:
        orm_mode = True

class SaleStats(BaseModel):
    total_sales: int
    total_items: int
    total_amount: float

class SalesSummary(BaseModel):
    sales: List[Sale]
    stats: SaleStats
