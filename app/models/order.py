from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    total = Column(Integer)

class OrderItem(Base):
    __tablename__ = 'order_items'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer)
    product_id = Column(Integer)
    quantity = Column(Integer)
    price = Column(Integer) 