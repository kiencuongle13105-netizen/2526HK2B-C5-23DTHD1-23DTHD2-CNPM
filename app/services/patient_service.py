from sqlalchemy.orm import Session
from app.models.patient import PatientProfile
from app.schemas.patient import PatientProfileCreate
from app.core.encryption import encryption_service

def create_patient_profile(db: Session, user_id: int, profile_data: PatientProfileCreate):
    encrypted_profile = PatientProfile(
        user_id=user_id,
        encrypted_address=encryption_service.encrypt(profile_data.address),
        encrypted_phone=encryption_service.encrypt(profile_data.phone),
        encrypted_birthdate=encryption_service.encrypt(profile_data.birthdate),
        encrypted_medical_history=encryption_service.encrypt(profile_data.medical_history)
    )
    db.add(encrypted_profile)
    db.commit()
    db.refresh(encrypted_profile)
    return encrypted_profile

def get_patient_profile(db: Session, user_id: int):
    profile = db.query(PatientProfile).filter(PatientProfile.user_id == user_id).first()
    if not profile:
        return None
    
    # Decrypt data for response
    return {
        "id": profile.id,
        "user_id": profile.user_id,
        "address": encryption_service.decrypt(profile.encrypted_address),
        "phone": encryption_service.decrypt(profile.encrypted_phone),
        "birthdate": encryption_service.decrypt(profile.encrypted_birthdate),
        "medical_history": encryption_service.decrypt(profile.encrypted_medical_history),
    }
