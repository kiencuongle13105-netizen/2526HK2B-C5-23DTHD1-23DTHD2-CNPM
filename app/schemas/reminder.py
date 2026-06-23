from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ReminderBase(BaseModel):
    drug_id: int
    reminder_time: str # HH:mm
    dose_info: str
    is_enabled: Optional[bool] = True

class ReminderCreate(ReminderBase):
    pass

class ReminderResponse(ReminderBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True
