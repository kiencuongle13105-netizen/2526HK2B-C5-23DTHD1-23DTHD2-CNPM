from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.prescription_stats import PrescriptionTimeStatsResponse
from app.services import prescription_stats_service
from app.core.access_control import role_required

router = APIRouter(prefix="/stats/prescriptions", tags=["Prescription Statistics"])

@router.get("/time-series", response_model=PrescriptionTimeStatsResponse)
def get_prescription_time_stats(
    interval: str = Query("month", enum=["day", "month", "year"]),
    current_user = Depends(role_required(["admin", "doctor"])), 
    db: Session = Depends(get_db)
):
    return prescription_stats_service.get_prescription_time_stats(db, interval)
