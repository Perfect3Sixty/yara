# utils/data_loader.py
import json
from sqlalchemy.orm import Session
from models.product import Product
import re

def extract_price_value(price_str: str) -> float:
    """Extract numerical value from price string."""
    try:
        # Remove any non-numeric characters except decimal points
        numeric_str = re.sub(r'[^\d.]', '', price_str)
        return float(numeric_str)
    except ValueError as e:
        print(f"Error converting price: {price_str}")
        print(f"After cleaning: {numeric_str}")
        raise e

def load_products(db: Session, file_path: str):
    """Load products from JSON file into database."""
    try:
        # Read the file with explicit UTF-8 encoding
        with open(file_path, 'r', encoding='utf-8') as f:
            products_data = json.load(f)
        
        for item in products_data:
            try:
                product = Product(
                    product_name=item['product_name'],
                    price=item['price'],
                    price_value=extract_price_value(item['price']),
                    rating=float(item['rating']),
                    description=item['description'],
                    link=item['link']
                )
                db.add(product)
                print(f"Successfully added product: {item['product_name']}")
            except Exception as e:
                print(f"Error processing product {item['product_name']}: {str(e)}")
                continue
        
        db.commit()
        print("Successfully committed all valid products to database")
    except Exception as e:
        print(f"Error in load_products: {str(e)}")
        db.rollback()
        raise e