from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.payment import PaymentCreate, PaymentResponse
from app.services import payment_service
from app.core.access_control import role_required

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("/checkout", response_model=PaymentResponse)
def process_checkout(
    data: PaymentCreate, 
    current_user = Depends(role_required(["patient", "doctor", "admin"])), 
    db: Session = Depends(get_db)
):
    return payment_service.create_payment(db, current_user.id, data)

@router.get("/me", response_model=List[PaymentResponse])
def get_my_payment_history(
    current_user = Depends(role_required(["patient", "doctor", "admin"])), 
    db: Session = Depends(get_db)
):
    return payment_service.get_user_payments(db, current_user.id)
