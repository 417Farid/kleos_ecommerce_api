from sqlalchemy.orm import Session
from app.models.cart import Cart, CartItem
from app.models.product import Product

def get_cart_by_user(db: Session, user_id: int):
    return db.query(Cart).filter(Cart.user_id == user_id).first()

def create_cart(db: Session, cart_data):
    payload = cart_data if isinstance(cart_data, dict) else cart_data.dict()
    cart = Cart(**payload)
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

def get_cart_items_with_products(db, cart_id: int):
    return (
        db.query(CartItem, Product)
        .join(Product, CartItem.product_id == Product.id)
        .filter(CartItem.cart_id == cart_id)
        .all()
    )

def remove_cart_item(db: Session, cart_id: int, product_id: int):
    item = get_cart_item(db, cart_id, product_id)
    if item:
        db.delete(item)
        db.commit()
        return True
    return False

