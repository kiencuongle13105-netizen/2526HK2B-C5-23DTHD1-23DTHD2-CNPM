from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class PaymentStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"

class PaymentMethod(str, Enum):
    CREDIT_CARD = "credit_card"
    PAYPAL = "paypal"
    STRIPE = "stripe"
    VNPAY = "vnpay"

class PaymentCreate(BaseModel):
    amount: float
    currency: str = "VND"
    payment_method: PaymentMethod
    description: str

class PaymentResponse(BaseModel):
    id: int
    user_id: int
    amount: float
    currency: str
    status: PaymentStatus
    transaction_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
