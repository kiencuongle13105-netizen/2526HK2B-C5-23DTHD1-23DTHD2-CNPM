from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.prescription import PrescriptionCreate, PrescriptionResponse
from app.services import prescription_service
from app.core.access_control import role_required

router = APIRouter(prefix="/prescriptions", tags=["Prescriptions"])

@router.post("/create", response_model=PrescriptionResponse)
def create_prescription(
    data: PrescriptionCreate, 
    current_user = Depends(role_required(["patient", "doctor", "admin"])), 
    db: Session = Depends(get_db)
):
    return prescription_service.create_prescription(db, current_user.id, data)

@router.put("/update/{prescription_id}", response_model=PrescriptionResponse)
def update_prescription(
    prescription_id: int,
    data: PrescriptionCreate, 
    current_user = Depends(role_required(["patient", "doctor", "admin"])), 
    db: Session = Depends(get_db)
):
    updated = prescription_service.update_prescription(db, prescription_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Prescription not found")
    
    # Ensure the user owns this prescription
    if updated.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to edit this prescription")
        
    return updated

@router.get("/me", response_model=list[PrescriptionResponse])
def get_my_prescriptions(
    current_user = Depends(role_required(["patient", "doctor", "admin"])), 
    db: Session = Depends(get_db)
):
    return prescription_service.get_user_prescriptions(db, current_user.id)
