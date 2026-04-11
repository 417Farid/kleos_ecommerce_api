from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.services.cart_service import add_to_cart_service, get_cart_service, remove_item_from_cart_service, update_cart_item_service
from app.core.auth.dependecies import get_current_user
from app.schemas.cart_schema import CartItemCreate, CartItemUpdate

router = APIRouter(prefix="/cart", tags=["cart"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/items")
def add_item_to_cart(
    item: CartItemCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    cart_item = add_to_cart_service(db, user.id, item)
    return {
        "message": f"Added {item.quantity} of product {item.product_id} to cart",
        "item_id": cart_item.id,
    }

@router.get("")
def get_cart(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return get_cart_service(db, user.id)

@router.delete("/items/{product_id}")
def remove_item_from_cart(
    product_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return remove_item_from_cart_service(db, user.id, product_id)

@router.put("/items/")
def update_cart_item(
    data: CartItemUpdate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    cart_item = update_cart_item_service(db, user.id, data)
    return cart_item