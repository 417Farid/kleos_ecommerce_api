from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.auth.dependecies import get_current_user
from app.schemas import UserCreate, UserLogin
from app.core.database import SessionLocal
from app.services.auth_service import register_user, login_user

router = APIRouter(prefix="/auth", tags=["auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    return register_user(db, user.email, user.password)  

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    return login_user(db, user.email, user.password)

@router.get("/me")
def get_me(user = Depends(get_current_user)):
    return {"id": user.id, "email": user.email}