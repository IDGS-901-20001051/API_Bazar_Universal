import json
import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from sqlalchemy.orm import Session
from app.core.database import engine, SessionLocal
from app.models.product import Product
from app.models.sale import Sale
from app.core.database import Base

def init_db():
    """Initialize database with sample data"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Check if products already exist
        existing_products = db.query(Product).count()
        if existing_products > 0:
            print(f"Database already has {existing_products} products. Skipping initialization.")
            return
        
        # Load products from JSON file
        json_file_path = os.path.join(os.path.dirname(__file__), 'products.json')
        with open(json_file_path, 'r', encoding='utf-8') as f:
            products_data = json.load(f)
        
        # Create products
        print(f"Adding {len(products_data)} products to database...")
        for product_data in products_data:
            # Remove id from data as it will be auto-generated
            product_data.pop('id', None)
            
            # Remove fields that are not in our model
            product_data.pop('thumbnail', None)
            product_data.pop('dimensions', None)
            product_data.pop('reviews', None)
            product_data.pop('meta', None)
            
            # Convert lists to JSON strings for SQLite compatibility
            if 'images' in product_data:
                product_data['images'] = json.dumps(product_data['images'])
            if 'features' in product_data:
                product_data['features'] = json.dumps(product_data['features'])
            if 'tags' in product_data:
                product_data['tags'] = json.dumps(product_data['tags'])
            
            product = Product(**product_data)
            db.add(product)
        
        db.commit()
        print("Database initialized successfully!")
        
        # Add some sample sales
        print("Adding sample sales...")
        sample_sales = [
            {
                "product_id": 1,
                "product_title": "iPhone X",
                "product_image": "https://images.unsplash.com/photo-1512054502232-10a0a035d8c1?w=500",
                "quantity": 1,
                "price": 10200.00,
                "total": 10200.00,
                "status": "Completada"
            },
            {
                "product_id": 4,
                "product_title": "Sony WH-1000XM4",
                "product_image": "https://images.unsplash.com/photo-1484704849700-f032a568e944?w=500",
                "quantity": 2,
                "price": 3500.00,
                "total": 7000.00,
                "status": "Completada"
            },
            {
                "product_id": 8,
                "product_title": "AirPods Pro",
                "product_image": "https://images.unsplash.com/photo-1588423771073-b8903fbb85b5?w=500",
                "quantity": 1,
                "price": 2800.00,
                "total": 2800.00,
                "status": "Completada"
            }
        ]
        
        for sale_data in sample_sales:
            sale = Sale(**sale_data)
            db.add(sale)
        
        db.commit()
        print("Sample sales added successfully!")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
