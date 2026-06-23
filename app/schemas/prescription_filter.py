from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PrescriptionHistoryFilter(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    doctor_name: Optional[str] = None
    keyword: Optional[str] = None # Search in drug names
