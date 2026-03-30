from sqlalchemy.orm import Session
from app.repositories.user_repository import get_user_by_email, create_user
from app.core.auth.security import hash_password, verify_password, create_access_token
from fastapi import HTTPException

def register_user(db: Session, email: str, password: str):
    existing_user = get_user_by_email(db, email)

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    try:
        hashed = hash_password(password)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    user = create_user(db, email, hashed)

    return {"message": "User registered successfully"}

def login_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Email or password incorrect")
    
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}
