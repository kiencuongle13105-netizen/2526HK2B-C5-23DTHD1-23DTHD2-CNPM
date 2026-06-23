from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.assessment import MedicalAssessmentResponse
from app.services import assessment_service, symptom_service
from app.core.access_control import role_required

router = APIRouter(prefix="/assessment", tags=["Medical Assessment"])

@router.get("/me", response_model=MedicalAssessmentResponse)
def get_my_assessment(
    current_user = Depends(role_required(["patient", "admin"])), 
    db: Session = Depends(get_db)
):
    # Retrieve the most recent symptom record
    record = symptom_service.get_user_symptoms(db, current_user.id)
    if not record:
        raise HTTPException(status_code=404, detail="No medical data found. Please report symptoms first.")
    
    # Analyze data
    assessment = assessment_service.analyze_patient_data(
        symptoms=record["symptoms"], 
        history=record["medical_history_details"]
    )
    
    return {
        "user_id": current_user.id,
        "assessment": assessment
    }
