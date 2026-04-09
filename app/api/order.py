from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.core.auth.dependecies import get_current_user
from app.services.order_service import create_order_service, get_orders_service

router = APIRouter(tags=["orders"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/orders")
def create_order(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return create_order_service(db, user.id)

@router.get("/orders")
def get_orders(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return get_orders_service(db, user.id)
