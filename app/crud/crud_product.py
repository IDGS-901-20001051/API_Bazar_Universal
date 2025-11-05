from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate

class CRUDProduct:
    def get(self, db: Session, id: int) -> Optional[Product]:
        return db.query(Product).filter(Product.id == id).first()
    
    def get_multi(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Product]:
        return db.query(Product).offset(skip).limit(limit).all()
    
    def get_by_category(
        self, 
        db: Session, 
        category: str, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Product]:
        return db.query(Product).filter(
            Product.category == category
        ).offset(skip).limit(limit).all()
    
    def search(
        self, 
        db: Session, 
        query: str, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Product]:
        return db.query(Product).filter(
            or_(
                Product.title.ilike(f"%{query}%"),
                Product.description.ilike(f"%{query}%"),
                Product.category.ilike(f"%{query}%"),
                Product.brand.ilike(f"%{query}%")
            )
        ).offset(skip).limit(limit).all()
    
    def count_search(self, db: Session, query: str) -> int:
        return db.query(Product).filter(
            or_(
                Product.title.ilike(f"%{query}%"),
                Product.description.ilike(f"%{query}%"),
                Product.category.ilike(f"%{query}%"),
                Product.brand.ilike(f"%{query}%")
            )
        ).count()
    
    def count(self, db: Session) -> int:
        return db.query(Product).count()
    
    def create(self, db: Session, obj_in: ProductCreate) -> Product:
        import json
        obj_in_data = obj_in.dict()
        
        # Convert lists to JSON strings for SQLite compatibility
        if 'images' in obj_in_data and obj_in_data['images']:
            obj_in_data['images'] = json.dumps(obj_in_data['images'])
        if 'features' in obj_in_data and obj_in_data['features']:
            obj_in_data['features'] = json.dumps(obj_in_data['features'])
            
        db_obj = Product(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(
        self, 
        db: Session, 
        db_obj: Product, 
        obj_in: ProductUpdate
    ) -> Product:
        import json
        obj_data = obj_in.dict(exclude_unset=True)
        
        for field, value in obj_data.items():
            if field in ['images', 'features'] and value is not None:
                # Convert lists to JSON strings
                value = json.dumps(value)
            setattr(db_obj, field, value)
            
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def remove(self, db: Session, id: int) -> Product:
        obj = db.query(Product).get(id)
        db.delete(obj)
        db.commit()
        return obj

product = CRUDProduct()
