from sqlalchemy.orm import Session
from app.models.symptom import SymptomRecord
from app.schemas.symptom import SymptomCreate
from app.core.encryption import encryption_service

def create_symptom_record(db: Session, user_id: int, data: SymptomCreate):
    encrypted_record = SymptomRecord(
        user_id=user_id,
        encrypted_symptoms=encryption_service.encrypt(data.symptoms),
        encrypted_medical_history_details=encryption_service.encrypt(data.medical_history_details)
    )
    db.add(encrypted_record)
    db.commit()
    db.refresh(encrypted_record)
    return encrypted_record

def get_user_symptoms(db: Session, user_id: int):
    record = db.query(SymptomRecord).filter(SymptomRecord.user_id == user_id).order_by(SymptomRecord.created_at.desc()).first()
    if not record:
        return None
    
    return {
        "id": record.id,
        "user_id": record.user_id,
        "symptoms": encryption_service.decrypt(record.encrypted_symptoms),
        "medical_history_details": encryption_service.decrypt(record.encrypted_medical_history_details),
        "created_at": record.created_at,
        "updated_at": record.updated_at,
    }
