
from sqlalchemy import Column, Integer, String, Float, Text
from services.postgres import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(255), index=True)
    price = Column(String(50))  
    price_value = Column(Float)  
    rating = Column(Float)
    description = Column(Text)
    link = Column(String(512))