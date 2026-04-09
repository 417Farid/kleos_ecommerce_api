from fastapi import FastAPI
from app.core.database import Base, engine
from app.models import cart, order, product, user
from app.api import auth, cart_routes, order as order_routes, product_routes

Base.metadata.create_all(bind=engine)   

app = FastAPI(title="KLEOS Ecommerce API")
app.include_router(product_routes.router)
app.include_router(auth.router)
app.include_router(cart_routes.router)
app.include_router(order_routes.router)


@app.get("/")
def root():
    return {"message": "KLEOS Ecommerce API"}
