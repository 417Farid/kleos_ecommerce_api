from sqlalchemy import Column, Integer, String, Float
from app.core.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)
    sport = Column(String)
    price = Column(Float)
    stock = Column(Integer)