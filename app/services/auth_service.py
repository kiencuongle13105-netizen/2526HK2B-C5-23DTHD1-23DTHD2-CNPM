from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import create_access_token, verify_password, decode_access_token
from app.models.user import User
from app.schemas.auth import Token, UserUpdate
from app.schemas.user import UserResponse

def get_current_user(token: str = Depends(OAuth2PasswordRequestForm), db: Session = Depends(get_db)):
    # This is a simplified version, normally we'd use OAuth2PasswordBearer
    pass

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def create_token(user: User):
    return create_access_token(data={"sub": user.username})
