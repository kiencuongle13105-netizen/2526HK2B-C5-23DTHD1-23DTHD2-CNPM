from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class NotificationBase(BaseModel):
    user_id: int
    title: str
    message: str
    is_read: bool = False
    created_at: datetime = datetime.now()

class NotificationCreate(BaseModel):
    title: str
    message: str

class NotificationResponse(NotificationBase):
    id: int

    class Config:
        from_attributes = True
