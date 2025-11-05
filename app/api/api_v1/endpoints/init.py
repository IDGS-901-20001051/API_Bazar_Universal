from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.product import Product
from app.models.sale import Sale
import json
import os

router = APIRouter()

@router.post("/init-database")
def init_database(db: Session = Depends(get_db)):
    """Initialize database with sample data"""
    try:
        # Check if products already exist
        existing_products = db.query(Product).count()
        if existing_products > 0:
            return {
                "message": f"Database already has {existing_products} products. Skipping initialization.",
                "products_count": existing_products
            }
        
        # Load products from JSON file (from data directory)
        json_file_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data', 'products.json')
        
        if not os.path.exists(json_file_path):
            raise HTTPException(status_code=404, detail="Products JSON file not found")
        
        with open(json_file_path, 'r', encoding='utf-8') as f:
            products_data = json.load(f)
        
        # Create products
        products_added = 0
        for product_data in products_data:
            # Remove id from data as it will be auto-generated
            product_data.pop('id', None)
            
            # Remove fields that are not in our model
            product_data.pop('thumbnail', None)
            product_data.pop('dimensions', None)
            product_data.pop('reviews', None)
            product_data.pop('meta', None)
            
            # Convert lists to JSON strings for PostgreSQL compatibility
            if 'images' in product_data:
                product_data['images'] = json.dumps(product_data['images'])
            if 'features' in product_data:
                product_data['features'] = json.dumps(product_data['features'])
            if 'tags' in product_data:
                product_data['tags'] = json.dumps(product_data['tags'])
            
            product = Product(**product_data)
            db.add(product)
            products_added += 1
        
        db.commit()
        
        # Add some sample sales
        sample_sales = [
            {
                "product_id": 1,
                "product_title": "Essence Mascara Lash Princess",
                "product_image": "https://cdn.dummyjson.com/products/images/beauty/Essence%20Mascara%20Lash%20Princess/1.png",
                "quantity": 1,
                "price": 9.99,
                "total": 9.99,
                "status": "Completada"
            },
            {
                "product_id": 2,
                "product_title": "Eyeshadow Palette with Mirror",
                "product_image": "https://cdn.dummyjson.com/products/images/beauty/Eyeshadow%20Palette%20with%20Mirror/1.png",
                "quantity": 2,
                "price": 19.99,
                "total": 39.98,
                "status": "Completada"
            },
            {
                "product_id": 6,
                "product_title": "Calvin Klein CK One",
                "product_image": "https://cdn.dummyjson.com/products/images/fragrances/Calvin%20Klein%20CK%20One/1.png",
                "quantity": 1,
                "price": 49.99,
                "total": 49.99,
                "status": "Completada"
            }
        ]
        
        sales_added = 0
        for sale_data in sample_sales:
            sale = Sale(**sale_data)
            db.add(sale)
            sales_added += 1
        
        db.commit()
        
        return {
            "message": "Database initialized successfully!",
            "products_added": products_added,
            "sales_added": sales_added,
            "status": "success"
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error initializing database: {str(e)}")
