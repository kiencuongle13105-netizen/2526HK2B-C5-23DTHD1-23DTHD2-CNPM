from datetime import datetime, timedelta
from typing import Any, Union
from jose import JWTError, jwt
from app.core.config import settings

# Use a secret key from config (will create config file next)
SECRET_KEY = "SUPER_SECRET_KEY_CHANGE_ME" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode_data = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode_data.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode_data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload if payload.get("sub") else None
    except JWTError:
        return None
