from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base
import datetime

class MedicationReminder(Base):
    __tablename__ = "medication_reminders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    drug_id = Column(Integer, ForeignKey("drugs.id"), index=True)
    reminder_time = Column(String) # HH:mm format
    dose_info = Column(String) # e.g., "1 tablet"
    is_enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    user = relationship("User")
    drug = relationship("Drug")
