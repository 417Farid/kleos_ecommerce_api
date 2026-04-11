from sqlalchemy import Boolean, Column, DateTime, Integer, String, Float
from app.core.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)
    sport = Column(String)
    price = Column(Float)
    stock = Column(Integer)

    is_active = Column(Boolean, default=True)
    deleted_at = Column(DateTime, nullable=True)