from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
import datetime

class PatientProfile(Base):
    __tablename__ = "patient_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, index=True)
    
    # Encrypted Fields
    encrypted_address = Column(String)
    encrypted_phone = Column(String)
    encrypted_birthdate = Column(String)
    encrypted_medical_history = Column(String)
    
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship("User", back_populates="profile")

# Add relationship to User model (manually via a separate file or by editing user.py)
# Since we cannot easily add relationship to existing class without re-importing, 
# we will handle it in the service layer or by editing user.py.
