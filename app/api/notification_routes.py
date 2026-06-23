from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.notification import NotificationCreate, NotificationResponse
from app.services import notification_service
from app.core.access_control import role_required

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.post("/send", response_model=NotificationResponse)
def send_notification(
    data: NotificationCreate, 
    user_id: int,
    current_user = Depends(role_required(["admin"])), 
    db: Session = Depends(get_db)
):
    # Only admin can manually send notifications to users
    return notification_service.create_notification(db, user_id, data)

@router.get("/me", response_model=List[NotificationResponse])
def get_my_notifications(
    current_user = Depends(role_required(["patient", "doctor", "admin"])), 
    db: Session = Depends(get_db)
):
    return notification_service.get_user_notifications(db, current_user.id)

@router.patch("/{notification_id}/read")
def mark_notification_read(
    notification_id: int, 
    current_user = Depends(role_required(["patient", "doctor", "admin"])), 
    db: Session = Depends(get_db)
):
    result = notification_service.mark_as_read(db, notification_id, current_user.id)
    if not result:
        raise HTTPException(status_code=404, detail="Notification not found")
    return {"message": "Notification marked as read"}
