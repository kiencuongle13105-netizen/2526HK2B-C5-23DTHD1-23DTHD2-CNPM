from fastapi import HTTPException, status, Depends
from app.core.security import decode_access_token
from app.core.database import get_db
from sqlalchemy.orm import Session
from app.models.user import User

def role_required(allowed_roles: list):
    def role_checker(token: str, db: Session = Depends(get_db)):
        payload = decode_access_token(token)
        if not payload:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        
        user = db.query(User).filter(User.username == payload["sub"]).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail=f"Role {user.role} does not have access to this resource"
            )
        return user
    return role_checker
