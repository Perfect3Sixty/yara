from pydantic import BaseModel
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

    class Config:
        orm_mode = True