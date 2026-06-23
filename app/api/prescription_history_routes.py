from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.prescription import PrescriptionResponse
from app.schemas.prescription_filter import PrescriptionHistoryFilter
from app.services import prescription_history_service
from app.core.access_control import role_required

router = APIRouter(prefix="/prescriptions/history", tags=["Prescription History"])

@router.get("/", response_model=List[PrescriptionResponse])
def get_prescription_history(
    filters: PrescriptionHistoryFilter = Depends(),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user = Depends(role_required(["patient", "doctor", "admin"])), 
    db: Session = Depends(get_db)
):
    return prescription_history_service.get_filtered_prescriptions(
        db=db, 
        user_id=current_user.id, 
        filters=filters, 
        skip=skip, 
        limit=limit
    )
