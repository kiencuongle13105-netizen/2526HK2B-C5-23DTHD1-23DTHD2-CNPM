from sqlalchemy.orm import Session
from app.models.reminder import MedicationReminder
from app.schemas.reminder import ReminderCreate
from datetime import datetime

def create_reminder(db: Session, user_id: int, data: ReminderCreate):
    db_reminder = MedicationReminder(
        user_id=user_id,
        drug_id=data.drug_id,
        reminder_time=data.reminder_time,
        dose_info=data.dose_info,
        is_enabled=data.is_enabled
    )
    db.add(db_reminder)
    db.commit()
    db.refresh(db_reminder)
    return db_reminder

def get_user_reminders(db: Session, user_id: int):
    return db.query(MedicationReminder).filter(
        MedicationReminder.user_id == user_id, 
        MedicationReminder.is_enabled == True
    ).order_by(MedicationReminder.reminder_time).all()

def get_reminders_for_current_time(db: Session, user_id: int):
    current_time = datetime.now().strftime("%H:%M")
    return db.query(MedicationReminder).filter(
        MedicationReminder.user_id == user_id,
        MedicationReminder.reminder_time == current_time,
        MedicationReminder.is_enabled == True
    ).all()

def delete_reminder(db: Session, reminder_id: int, user_id: int):
    reminder = db.query(MedicationReminder).filter(
        MedicationReminder.id == reminder_id,
        MedicationReminder.user_id == user_id
    ).first()
    if reminder:
        db.delete(reminder)
        db.commit()
    return reminder
