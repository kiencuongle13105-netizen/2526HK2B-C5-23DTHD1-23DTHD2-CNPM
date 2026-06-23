import uuid
from sqlalchemy.orm import Session
from app.models.payment import Payment
from app.schemas.payment import PaymentCreate, PaymentStatus

class PaymentGatewayClient:
    """
    Mock Client for Payment Gateways (Stripe/PayPal/VNPAY).
    In a real scenario, this would use the respective SDKs.
    """
    def process_payment(self, amount: float, currency: str, method: str) -> dict:
        # Simulate payment processing
        import random
        success = random.random() > 0.1 # 90% success rate
        
        return {
            "transaction_id": f"TXN_{uuid.uuid4().hex[:12].upper()}",
            "status": "completed" if success else "failed",
            "amount": amount,
            "currency": currency
        }

def create_payment(db: Session, user_id: int, data: PaymentCreate):
    gateway = PaymentGatewayClient()
    
    # 1. Initial record as pending
    db_payment = Payment(
        user_id=user_id,
        amount=data.amount,
        currency=data.currency,
        payment_method=data.payment_method,
        description=data.description,
        status="pending"
    )
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    
    # 2. Process through gateway
    result = gateway.process_payment(data.amount, data.currency, data.payment_method)
    
    # 3. Update payment status based on gateway response
    db_payment.transaction_id = result["transaction_id"]
    db_payment.status = result["status"]
    db.commit()
    db.refresh(db_payment)
    
    return db_payment

def get_user_payments(db: Session, user_id: int):
    return db.query(Payment).filter(Payment.user_id == user_id).order_by(Payment.created_at.desc()).all()
