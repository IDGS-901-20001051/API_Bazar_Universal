from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.crud.crud_sale import sale
from app.schemas.sale import Sale, SaleCreate, SaleStats, SalesSummary

router = APIRouter()

@router.get("/", response_model=SalesSummary)
def get_sales(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all sales with summary statistics"""
    sales = sale.get_multi(db, skip=skip, limit=limit)
    
    # Get statistics
    total_sales = sale.count(db)
    total_items = sale.get_total_items(db)
    total_amount = sale.get_total_amount(db)
    
    stats = SaleStats(
        total_sales=total_sales,
        total_items=total_items,
        total_amount=total_amount
    )
    
    return SalesSummary(sales=sales, stats=stats)

@router.get("/stats", response_model=SaleStats)
def get_sales_stats(db: Session = Depends(get_db)):
    """Get sales statistics only"""
    total_sales = sale.count(db)
    total_items = sale.get_total_items(db)
    total_amount = sale.get_total_amount(db)
    
    return SaleStats(
        total_sales=total_sales,
        total_items=total_items,
        total_amount=total_amount
    )

@router.get("/{sale_id}", response_model=Sale)
def get_sale(
    sale_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific sale by ID"""
    db_sale = sale.get(db, id=sale_id)
    if db_sale is None:
        raise HTTPException(status_code=404, detail="Sale not found")
    return db_sale

@router.post("/", response_model=Sale)
def create_sale(
    sale_in: SaleCreate,
    db: Session = Depends(get_db)
):
    """Create a new sale (purchase)"""
    try:
        return sale.create(db, obj_in=sale_in)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{sale_id}", response_model=Sale)
def delete_sale(
    sale_id: int,
    db: Session = Depends(get_db)
):
    """Delete a sale"""
    db_sale = sale.get(db, id=sale_id)
    if db_sale is None:
        raise HTTPException(status_code=404, detail="Sale not found")
    return sale.remove(db, id=sale_id)
