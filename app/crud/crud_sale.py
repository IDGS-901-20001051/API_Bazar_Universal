from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.sale import Sale
from app.models.product import Product
from app.schemas.sale import SaleCreate

class CRUDSale:
    def get(self, db: Session, id: int) -> Optional[Sale]:
        return db.query(Sale).filter(Sale.id == id).first()
    
    def get_multi(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Sale]:
        return db.query(Sale).order_by(Sale.date.desc()).offset(skip).limit(limit).all()
    
    def count(self, db: Session) -> int:
        return db.query(Sale).count()
    
    def get_total_amount(self, db: Session) -> float:
        result = db.query(Sale.total).all()
        return sum(sale.total for sale in result) if result else 0.0
    
    def get_total_items(self, db: Session) -> int:
        result = db.query(Sale.quantity).all()
        return sum(sale.quantity for sale in result) if result else 0
    
    def create(self, db: Session, obj_in: SaleCreate) -> Sale:
        # Get product info
        product = db.query(Product).filter(Product.id == obj_in.product_id).first()
        if not product:
            raise ValueError("Product not found")
        
        # Calculate total
        total = product.price * obj_in.quantity
        
        # Create sale
        db_obj = Sale(
            product_id=obj_in.product_id,
            product_title=product.title,
            product_image=product.images[0] if product.images else None,
            quantity=obj_in.quantity,
            price=product.price,
            total=total
        )
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def remove(self, db: Session, id: int) -> Sale:
        obj = db.query(Sale).get(id)
        db.delete(obj)
        db.commit()
        return obj

sale = CRUDSale()
