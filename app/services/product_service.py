from sqlalchemy.orm import Session
from app.repositories.product_repository import create_product, get_product_by_id, get_products_filtered, get_products

def create_product_service(db: Session, product_data):
    return create_product(db, product_data)

def get_products_filtered_service(db: Session, sport=None, min_price=None):
    return get_products_filtered(db, sport, min_price)

def get_product_by_id_service(db: Session, product_id: int):
    return get_product_by_id(db, product_id)

def get_products_service(db: Session):
    return get_products(db)