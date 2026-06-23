from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.symptom import SymptomCreate, SymptomResponse
from app.services import symptom_service
from app.core.access_control import role_required

router = APIRouter(prefix="/symptoms", tags=["Symptoms"])

@router.post("/report", response_model=SymptomResponse)
def report_symptoms(
    data: SymptomCreate, 
    current_user = Depends(role_required(["patient", "admin"])), 
    db: Session = Depends(get_db)
):
    record = symptom_service.create_symptom_record(db, current_user.id, data)
    
    return {
        "id": record.id,
        "user_id": record.user_id,
        "symptoms": symptom_service.encryption_service.decrypt(record.encrypted_symptoms),
        "medical_history_details": symptom_service.encryption_service.decrypt(record.encrypted_medical_history_details),
        "created_at": record.created_at,
        "updated_at": record.updated_at,
    }

@router.get("/me", response_model=SymptomResponse)
def get_my_symptoms(
    current_user = Depends(role_required(["patient", "admin"])), 
    db: Session = Depends(get_db)
):
    record = symptom_service.get_user_symptoms(db, current_user.id)
    if not record:
        raise HTTPException(status_code=404, detail="No symptom records found for this user")
    return record
