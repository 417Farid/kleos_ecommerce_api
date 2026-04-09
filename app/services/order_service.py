from fastapi import HTTPException
from app.repositories.cart_repository import get_cart_by_user, get_cart_items_with_products
from app.repositories.order_repository import create_order, create_order_item
from app.repositories.order_repository import get_orders_with_items


def create_order_service(db, user_id: int):
    # 1. Obtener carrito
    cart = get_cart_by_user(db, user_id)

    if not cart:
        raise HTTPException(status_code=400, detail="Carrito vacío")

    items = get_cart_items_with_products(db, cart.id)

    if not items:
        raise HTTPException(status_code=400, detail="Carrito vacío")

    total = 0

    # 2. Validar stock + calcular total
    for cart_item, product in items:
        if product.stock < cart_item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Stock insuficiente para {product.name}"
            )

        total += product.price * cart_item.quantity

    # 3. Crear orden
    order = create_order(db, user_id, total)

    # 4. Crear order items + descontar stock
    for cart_item, product in items:
        create_order_item(
            db,
            order.id,
            product.id,
            cart_item.quantity,
            product.price
        )

        # 🔥 descontar stock
        product.stock -= cart_item.quantity

    # 5. Vaciar carrito
    for cart_item, _ in items:
        db.delete(cart_item)

    # 6. Guardar todo
    db.commit()

    return {
        "order_id": order.id,
        "total": total
    }

def get_orders_service(db, user_id: int):
    rows = get_orders_with_items(db, user_id)

    orders_dict = {}

    for order, item, product in rows:
        if order.id not in orders_dict:
            orders_dict[order.id] = {
                "order_id": order.id,
                "total": order.total,
                "created_at": order.created_at.isoformat(),
                "items": [],
                "items_count": 0
            }

        orders_dict[order.id]["items"].append({
            "product_id": product.id,
            "name": product.name,
            "quantity": item.quantity,
            "price": item.price
        })

        orders_dict[order.id]["items_count"] += item.quantity

    return {"orders": list(orders_dict.values())}