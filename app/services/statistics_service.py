from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.user import User
from app.models.prescription import Prescription
from app.models.symptom import SymptomRecord
from app.models.patient import PatientProfile
from app.schemas.statistics import PatientStatsResponse

def get_overall_statistics(db: Session):
    # 1. Total Patients
    total_patients = db.query(User).filter(User.role == "patient").count()
    
    # 2. Patients by Role
    role_counts = db.query(User.role, func.count(User.id)).group_by(User.role).all()
    patients_by_role = {role: count for role, count in role_counts}
    
    # 3. Total Prescriptions
    total_prescriptions = db.query(Prescription).count()
    
    # 4. Total Symptoms Reported
    total_symptoms = db.query(SymptomRecord).count()
    
    # 5. Disease Distribution (from Patient Profiles)
    # We decrypt the medical history and count occurrences of common diseases
    profiles = db.query(PatientProfile).all()
    disease_counts = {}
    
    from app.core.encryption import encryption_service
    
    # Common diseases to track
    common_diseases = ["Diabetes", "Hypertension", "Asthma", "Heart Disease", "Kidney Disease", "Liver Disease"]
    
    for profile in profiles:
        history = encryption_service.decrypt(profile.encrypted_medical_history).lower()
        for disease in common_diseases:
            if disease.lower() in history:
                disease_counts[disease] = disease_counts.get(disease, 0) + 1
                
    return PatientStatsResponse(
        total_patients=total_patients,
        patients_by_role=patients_by_role,
        total_prescriptions=total_prescriptions,
        total_symptoms_reported=total_symptoms,
        disease_distribution=disease_counts
    )
