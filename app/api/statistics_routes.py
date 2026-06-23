from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.statistics import PatientStatsResponse
from app.services import statistics_service
from app.core.access_control import role_required

router = APIRouter(prefix="/stats", tags=["Statistics"])

@router.get("/patients", response_model=PatientStatsResponse)
def get_patient_statistics(
    current_user = Depends(role_required(["admin", "doctor"])), 
    db: Session = Depends(get_db)
):
    return statistics_service.get_overall_statistics(db)
