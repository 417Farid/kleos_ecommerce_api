from sqlalchemy.orm import Session
from app.models import product
from app.repositories.cart_repository import create_cart, get_cart_by_user, get_cart_item, create_cart_item, update_cart_item_quantity  
from app.models.product import Product

def create_cart_service(db: Session, cart_data):
    return create_cart(db, cart_data)

def add_to_cart_service(db: Session, user_id: int, item_data):
    cart = get_cart_by_user(db, user_id)
    if not cart:
        cart = create_cart(db, {"user_id": user_id})
    
    product = db.query(Product).filter(Product.id == item_data.product_id).first()
    if not product:
        raise Exception("Product not found")

    if product.stock < item_data.quantity:
        raise Exception("Not enough stock available")

    existing_item = get_cart_item(db, cart.id, item_data.product_id)
    if existing_item:
        return update_cart_item_quantity(db, existing_item, item_data.quantity)
    else:
        return create_cart_item(db, cart.id, item_data.product_id, item_data.quantity)
