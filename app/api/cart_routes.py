from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.services.cart_service import add_product_to_cart_service

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/cart/items")
def add_item_to_cart(cart_id: int, product_id: int, quantity: int, db: Session = Depends(get_db)):
    add_product_to_cart_service(db, cart_id, product_id, quantity)
    return {"message": f"Added {quantity} of product {product_id} to cart {cart_id}"}

