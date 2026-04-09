import os
from datetime import datetime, timedelta
import hashlib

import bcrypt
from jose import jwt
from dotenv import load_dotenv

SHA256_BCRYPT_PREFIX = "bcrypt_sha256$"

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-env")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def _prehash_password(password: str) -> bytes:
    return hashlib.sha256(password.encode("utf-8")).hexdigest().encode("ascii")

def hash_password(password):
    hashed = bcrypt.hashpw(_prehash_password(password), bcrypt.gensalt())
    return f"{SHA256_BCRYPT_PREFIX}{hashed.decode('utf-8')}"

def verify_password(plain_password, hashed_password):
    if hashed_password.startswith(SHA256_BCRYPT_PREFIX):
        current_hash = hashed_password[len(SHA256_BCRYPT_PREFIX):].encode("utf-8")
        return bcrypt.checkpw(_prehash_password(plain_password), current_hash)

    # Compatibilidad con hashes bcrypt antiguos ya guardados en la BD.
    try:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
    except ValueError:
        return False

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
