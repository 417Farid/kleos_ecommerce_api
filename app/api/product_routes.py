from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.product_schema import ProductCreate
from app.core.database import SessionLocal
from app.core.auth.dependecies import get_current_admin
from app.services.product_service import (
    create_product_service,
    get_product_by_id_service,
    get_products_filtered_service,
    get_products_service,
)

router = APIRouter(prefix="/products", tags=["products"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("")
def create_product(product: ProductCreate, db: Session = Depends(get_db), user = Depends(get_current_admin)):
    return create_product_service(db, product)

@router.get("")
def get_products(
    sport: str = None,
    min_price: float = None,
    db: Session = Depends(get_db)
):
    return get_products_filtered_service(db, sport, min_price)

@router.get("/all")
def get_all_products(db: Session = Depends(get_db)):
    return get_products_service(db)

@router.get("/{product_id}")
def get_product_by_id(
    product_id: int,
    db: Session = Depends(get_db)
):
    return get_product_by_id_service(db, product_id)
