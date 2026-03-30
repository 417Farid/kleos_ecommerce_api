from fastapi import FastAPI
from app.core.database import Base, engine
from app.models import product, user
from app.api import product_routes , auth

Base.metadata.create_all(bind=engine)   

app = FastAPI(title="KLEOS Ecommerce API")
app.include_router(product_routes.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "KLEOS Ecommerce API"}
