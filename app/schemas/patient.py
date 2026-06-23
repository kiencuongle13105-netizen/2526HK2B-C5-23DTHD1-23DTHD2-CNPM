from pydantic import BaseModel
from typing import Optional

class PatientProfileCreate(BaseModel):
    address: str
    phone: str
    birthdate: str
    medical_history: str

class PatientProfileResponse(BaseModel):
    id: int
    user_id: int
    address: str
    phone: str
    birthdate: str
    medical_history: str

    class Config:
        from_attributes = True
