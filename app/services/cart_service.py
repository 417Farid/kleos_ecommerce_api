from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.cart_repository import create_cart, get_cart_by_user, get_cart_item, create_cart_item, remove_cart_item, update_cart_item_quantity, get_cart_items_with_products
from app.models.product import Product

def create_cart_service(db: Session, cart_data):
    return create_cart(db, cart_data)

def add_to_cart_service(db: Session, user_id: int, item_data):
    cart = get_cart_by_user(db, user_id)
    if not cart:
        cart = create_cart(db, {"user_id": user_id})

    product = db.query(Product).filter(Product.id == item_data.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if item_data.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than 0")

    if product.stock < item_data.quantity:
        raise HTTPException(status_code=400, detail="Not enough stock available")

    existing_item = get_cart_item(db, cart.id, item_data.product_id)
    if existing_item:
        return update_cart_item_quantity(db, existing_item, item_data.quantity)
    else:
        return create_cart_item(db, cart.id, item_data.product_id, item_data.quantity)

def get_cart_service(db, user_id: int):
    cart = get_cart_by_user(db, user_id)

    if not cart:
        return {"items": []}
    
    items = get_cart_items_with_products(db, cart.id)

    result = []

    for cart_item, product in items:
        result.append({
            "product_id": product.id,
            "name": product.name,
            "price": product.price,
            "quantity": cart_item.quantity
        })
    return {"items": result}

def remove_item_from_cart_service(db: Session, user_id: int, product_id: int):
    cart = get_cart_by_user(db, user_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    success = remove_cart_item(db, cart.id, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found in cart")
    return {"detail": "Item removed from cart"}