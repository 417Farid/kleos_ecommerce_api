from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from app.core.auth.security import SECRET_KEY, ALGORITHM
from app.core.database import SessionLocal
from app.models.user import User

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        print("Decoding token:", token)  # Debugging line
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid user ID in token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid Token or Expired Token")
    
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    db.close()
    
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user

def get_current_admin(user = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return user