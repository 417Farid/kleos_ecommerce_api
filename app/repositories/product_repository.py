from sqlalchemy.orm import Session
from app.models.product import Product

# Product Repository Layer

## Create a new product
def create_product(db: Session, product_data: dict):
    product = Product(**product_data)
    db.add(product)
    return product

## Get products with/without optional filters
def get_products_filtered(db: Session, sport=None, min_price=None):
    query = db.query(Product).filter(Product.is_active == True)

    if sport:
        query = query.filter(Product.sport.ilike(f"%{sport}%"))

    if min_price is not None:
        query = query.filter(Product.price >= min_price)

    return query.all()

## Get product by ID
def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id, Product.is_active == True).first()

def get_product_by_id_any_status(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

## Get all products without filters
def get_products(db: Session):
    return db.query(Product).all()

def get_active_products(db: Session):
    return db.query(Product).filter(Product.is_active == True).all()
