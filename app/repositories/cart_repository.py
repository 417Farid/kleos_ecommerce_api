from sqlalchemy.orm import Session
from app.models.cart import Cart, CartItem

def get_cart_by_user(db: Session, user_id: int):
    return db.query(Cart).filter(Cart.user_id == user_id).first()

def create_cart(db: Session, cart_data):
    cart = Cart(**cart_data.dict())
    db.add(cart)
    db.commit()
    db.refresh(cart)
    return cart

def get_cart_item(db: Session, cart_id: int, product_id: int):
    return db.query(CartItem).filter(CartItem.cart_id == cart_id, CartItem.product_id == product_id).first()

def create_cart_item(db: Session, cart_id:int, product_id: int, quantity: int):
    item = CartItem(cart_id=cart_id, product_id=product_id, quantity=quantity)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def update_cart_item_quantity(db: Session, item: CartItem, quantity: int):
    item.quantity += quantity
    db.commit()
    db.refresh(item)
    return item
