from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SymptomCreate(BaseModel):
    symptoms: str
    medical_history_details: str

class SymptomResponse(BaseModel):
    id: int
    user_id: int
    symptoms: str
    medical_history_details: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
