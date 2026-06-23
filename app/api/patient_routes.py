from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.patient import PatientProfileCreate, PatientProfileResponse
from app.services import patient_service
from app.api.auth_routes import get_me # Hypothetical helper

router = APIRouter(prefix="/patients", tags=["Patients"])

@router.post("/profile", response_model=PatientProfileResponse)
def create_profile(profile: PatientProfileCreate, token: str, db: Session = Depends(get_db)):
    # Validating token and getting user_id (simplified for UAZ-52)
    # In real implementation, we'd use a proper dependency
    from app.core.security import decode_access_token
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    from app.models.user import User
    user = db.query(User).filter(User.username == payload["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    profile_obj = patient_service.create_patient_profile(db, user.id, profile)
    
    return {
        "id": profile_obj.id,
        "user_id": profile_obj.user_id,
        "address": patient_service.encryption_service.decrypt(profile_obj.encrypted_address),
        "phone": patient_service.encryption_service.decrypt(profile_obj.encrypted_phone),
        "birthdate": patient_service.encryption_service.decrypt(profile_obj.encrypted_birthdate),
        "medical_history": patient_service.encryption_service.decrypt(profile_obj.encrypted_medical_history),
    }
