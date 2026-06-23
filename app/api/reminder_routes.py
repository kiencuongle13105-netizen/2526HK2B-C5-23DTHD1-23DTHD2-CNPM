from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.reminder import ReminderCreate, ReminderResponse
from app.services import reminder_service
from app.core.access_control import role_required

router = APIRouter(prefix="/reminders", tags=["Medication Reminders"])

@router.post("/create", response_model=ReminderResponse)
def create_reminder(
    data: ReminderCreate, 
    current_user = Depends(role_required(["patient", "admin"])), 
    db: Session = Depends(get_db)
):
    return reminder_service.create_reminder(db, current_user.id, data)

@router.get("/me", response_model=List[ReminderResponse])
def get_my_reminders(
    current_user = Depends(role_required(["patient", "admin"])), 
    db: Session = Depends(get_db)
):
    return reminder_service.get_user_reminders(db, current_user.id)

@router.get("/now", response_model=List[ReminderResponse])
def get_current_reminders(
    current_user = Depends(role_required(["patient", "admin"])), 
    db: Session = Depends(get_db)
):
    return reminder_service.get_reminders_for_current_time(db, current_user.id)

@router.delete("/{reminder_id}")
def delete_reminder(
    reminder_id: int, 
    current_user = Depends(role_required(["patient", "admin"])), 
    db: Session = Depends(get_db)
):
    result = reminder_service.delete_reminder(db, reminder_id, current_user.id)
    if not result:
        raise HTTPException(status_code=404, detail="Reminder not found or not authorized")
    return {"message": "Reminder deleted successfully"}
