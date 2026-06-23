from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.patient import PatientProfileCreate, PatientProfileResponse
from app.services import patient_service
from app.core.access_control import role_required

router = APIRouter(prefix="/patients", tags=["Patients"])

@router.post("/profile", response_model=PatientProfileResponse)
def create_profile(
    profile: PatientProfileCreate, 
    current_user = Depends(role_required(["patient", "admin"])), 
    db: Session = Depends(get_db)
):
    profile_obj = patient_service.create_patient_profile(db, current_user.id, profile)
    
    return {
        "id": profile_obj.id,
        "user_id": profile_obj.user_id,
        "address": patient_service.encryption_service.decrypt(profile_obj.encrypted_address),
        "phone": patient_service.encryption_service.decrypt(profile_obj.encrypted_phone),
        "birthdate": patient_service.encryption_service.decrypt(profile_obj.encrypted_birthdate),
        "medical_history": patient_service.encryption_service.decrypt(profile_obj.encrypted_medical_history),
    }
