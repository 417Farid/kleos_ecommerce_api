from sqlalchemy.orm import Session
from app.models.product import Product

def create_product(db: Session, product_data):
    product = Product(**product_data.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def get_products_filtered(db: Session, sport=None, min_price=None):
    query = db.query(Product)

    if sport:
        query = query.filter(Product.sport == sport)

    if min_price:
        query = query.filter(Product.price >= min_price)

    return query.all()

def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def get_products(db: Session):
    return db.query(Product).all()
