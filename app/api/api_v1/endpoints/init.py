from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.product import Product
from app.models.sale import Sale
import json
import os

router = APIRouter()

def get_fallback_products_data():
    """Fallback product data in case JSON file is not found"""
    return [
        {
            "title": "Essence Mascara Lash Princess",
            "description": "The Essence Mascara Lash Princess is a popular mascara known for its volumizing and lengthening effects. Achieve dramatic lashes with this long-lasting and cruelty-free formula.",
            "category": "beauty",
            "price": 9.99,
            "discountPercentage": 7.17,
            "rating": 4.94,
            "stock": 5,
            "tags": ["beauty", "mascara"],
            "brand": "Essence",
            "sku": "RCH45Q1A",
            "weight": 2,
            "warrantyInformation": "1 month warranty",
            "shippingInformation": "Ships in 1 month",
            "availabilityStatus": "Low Stock",
            "returnPolicy": "30 days return policy",
            "minimumOrderQuantity": 24,
            "images": ["https://cdn.dummyjson.com/products/images/beauty/Essence%20Mascara%20Lash%20Princess/1.png"]
        },
        {
            "title": "Eyeshadow Palette with Mirror",
            "description": "The Eyeshadow Palette with Mirror offers a versatile range of eyeshadow shades for creating stunning eye looks. With a built-in mirror, it's convenient for on-the-go makeup application.",
            "category": "beauty",
            "price": 19.99,
            "discountPercentage": 5.5,
            "rating": 3.28,
            "stock": 44,
            "tags": ["beauty", "eyeshadow"],
            "brand": "Glamour Beauty",
            "sku": "MVCFH27F",
            "weight": 3,
            "warrantyInformation": "1 year warranty",
            "shippingInformation": "Ships in 2 weeks",
            "availabilityStatus": "In Stock",
            "returnPolicy": "30 days return policy",
            "minimumOrderQuantity": 32,
            "images": ["https://cdn.dummyjson.com/products/images/beauty/Eyeshadow%20Palette%20with%20Mirror/1.png"]
        },
        {
            "title": "Calvin Klein CK One",
            "description": "CK One by Calvin Klein is a classic unisex fragrance, known for its fresh and clean scent. It's a versatile fragrance suitable for everyday wear.",
            "category": "fragrances",
            "price": 49.99,
            "discountPercentage": 0.32,
            "rating": 4.85,
            "stock": 17,
            "tags": ["fragrances", "perfumes"],
            "brand": "Calvin Klein",
            "sku": "DZM2JQZE",
            "weight": 5,
            "warrantyInformation": "5 year warranty",
            "shippingInformation": "Ships overnight",
            "availabilityStatus": "In Stock",
            "returnPolicy": "No return policy",
            "minimumOrderQuantity": 20,
            "images": ["https://cdn.dummyjson.com/products/images/fragrances/Calvin%20Klein%20CK%20One/1.png"]
        },
        {
            "title": "Annibale Colombo Bed",
            "description": "The Annibale Colombo Bed is a luxurious and elegant bed frame, crafted with high-quality materials for a comfortable and stylish bedroom.",
            "category": "furniture",
            "price": 1899.99,
            "discountPercentage": 0.29,
            "rating": 4.14,
            "stock": 47,
            "tags": ["furniture", "beds"],
            "brand": "Annibale Colombo",
            "sku": "4KMDTZWF",
            "weight": 3,
            "warrantyInformation": "2 year warranty",
            "shippingInformation": "Ships overnight",
            "availabilityStatus": "In Stock",
            "returnPolicy": "7 days return policy",
            "minimumOrderQuantity": 1,
            "images": ["https://cdn.dummyjson.com/products/images/furniture/Annibale%20Colombo%20Bed/1.png"]
        },
        {
            "title": "Apple",
            "description": "Fresh and crisp apples, perfect for snacking or incorporating into various recipes.",
            "category": "groceries",
            "price": 1.99,
            "discountPercentage": 1.97,
            "rating": 2.96,
            "stock": 9,
            "tags": ["fruits"],
            "sku": "QTROUV79",
            "weight": 8,
            "warrantyInformation": "2 year warranty",
            "shippingInformation": "Ships in 2 weeks",
            "availabilityStatus": "In Stock",
            "returnPolicy": "60 days return policy",
            "minimumOrderQuantity": 44,
            "images": ["https://cdn.dummyjson.com/products/images/groceries/Apple/1.png"]
        }
    ]

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
        # Try multiple possible paths for the JSON file
        possible_paths = [
            os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data', 'products.json'),
            os.path.join(os.getcwd(), 'data', 'products.json'),
            os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'data', 'products.json'),
            'data/products.json',
            './data/products.json'
        ]
        
        json_file_path = None
        for path in possible_paths:
            if os.path.exists(path):
                json_file_path = path
                break
        
        if not json_file_path:
            # If file not found, use hardcoded data as fallback
            products_data = get_fallback_products_data()
        else:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                products_data = json.load(f)
        
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
