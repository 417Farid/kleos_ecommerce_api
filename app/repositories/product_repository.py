from sqlalchemy.orm import Session
from app.models.product import Product

# Product Repository Layer

## Create a new product
def create_product(db: Session, product_data):
    product = Product(**product_data.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

## Get products with/without optional filters
def get_products_filtered(db: Session, sport=None, min_price=None):
    query = db.query(Product)

    if sport:
        query = query.filter(Product.sport == sport)

    if min_price:
        query = query.filter(Product.price >= min_price)

    return query.all()

## Get product by ID
def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id, Product.is_active == True).first()

## Get all products without filters
def get_products(db: Session):
    return db.query(Product).all()

def get_active_products(db: Session):
    return db.query(Product).filter(Product.is_active == True).all()