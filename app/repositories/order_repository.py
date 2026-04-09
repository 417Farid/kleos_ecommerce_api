from app.models.order import Order
from app.models.order import OrderItem
from app.models.product import Product

def create_order(db, user_id: int, total: float):
    order = Order(user_id=user_id, total=total)
    db.add(order)
    db.flush()
    return order

def create_order_item(db, order_id, product_id, quantity, price):
    item = OrderItem(
        order_id=order_id,
        product_id=product_id,
        quantity=quantity,
        price=price
    )
    db.add(item)

def get_orders_with_items(db, user_id: int):
    return (
        db.query(Order, OrderItem, Product)
        .join(OrderItem, Order.id == OrderItem.order_id)
        .join(Product, OrderItem.product_id == Product.id)
        .filter(Order.user_id == user_id)
        .all()
    )
