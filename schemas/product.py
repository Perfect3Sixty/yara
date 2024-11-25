# schemas/product.py
from pydantic import BaseModel, Field
from typing import Optional

class ProductBase(BaseModel):
    product_name: str
    price: str
    rating: float
    description: str
    link: str

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    price_value: float
        
class ProductInfo(BaseModel):
    """Data structure for product information"""
    product_name: str = Field(description="Name of the product")
    price: str = Field(description="Current price of the product")
    original_price: Optional[str] = Field(description="Original price before discount if available")
    discount: Optional[str] = Field(description="Discount percentage if available")
    rating: Optional[str] = Field(description="Product rating if available")
    image_url: Optional[str] = Field(description="URL of the product image")
    product_url: Optional[str] = Field(description="URL of the product page")
    description: Optional[str] = Field(description="Product description or key features")
    brand: Optional[str] = Field(description="Brand name of the product")
    platform: str = Field(description="E-commerce platform (e.g., Amazon, Nykaa)")
