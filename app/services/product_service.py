from sqlalchemy.orm import Session
from app.repositories.product_repository import (
    create_product,
    get_product_by_id,
    get_product_by_id_any_status,
    get_products_filtered,
    get_products,
)
from fastapi import HTTPException
from datetime import datetime

# Product Service Layer

## Create a new product
def create_product_service(db: Session, product_data):
    product_payload = product_data.model_dump()
    product = create_product(db, product_payload)
    db.commit()
    db.refresh(product)
    return product

## Get products with/without optional filters
def get_products_filtered_service(db: Session, sport=None, min_price=None):
    return get_products_filtered(db, sport, min_price)

## Get product by ID
def get_product_by_id_service(db: Session, product_id: int):
    return get_product_by_id(db, product_id)

## Get all products without filters
def get_products_service(db: Session):
    return get_products(db)

## Update product
def update_product_service(db, product_id: int, update_data):
    product = get_product_by_id(db, product_id)

    ## Validate if product exists
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    ## Allow fields
    allow_fields = ['name', 'category', 'sport', 'price', 'stock']

    ## Update only provided fields
    for key, value in update_data.model_dump(exclude_unset=True).items():
        if key not in allow_fields:
            continue

        if value is None:
            continue

        if key in ["price", "stock"] and value < 0:
            raise HTTPException(status_code=400, detail="Invalid value provided")

        if key == "price" and value <= 0:
            raise HTTPException(status_code=400, detail="Price must be a positive value")

        setattr(product, key, value)

    db.commit()
    db.refresh(product) 

    return product

## Delete product
def delete_product_service(db, product_id: int):
    product = get_product_by_id(db, product_id)

    ## Validate if product exists
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if not product.is_active:
        raise HTTPException(status_code=400, detail="Product already deleted")
    
    product.is_active = False
    product.deleted_at = datetime.utcnow()

    db.commit()
    db.refresh(product)

    return {"message": "Product deactivated successfully"}  

def restore_product_service(db, product_id: int):
    product = get_product_by_id_any_status(db, product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.is_active:
        raise HTTPException(status_code=400, detail="Product is already active")

    product.is_active = True
    product.deleted_at = None

    db.commit()
    db.refresh(product)

    return {"message": "Product restored"}
