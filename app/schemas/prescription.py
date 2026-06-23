from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class PrescriptionItemBase(BaseModel):
    drug_name: str
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    duration: Optional[str] = None

class PrescriptionItemCreate(PrescriptionItemBase):
    pass

class PrescriptionItemResponse(PrescriptionItemBase):
    id: int
    prescription_id: int

    class Config:
        from_attributes = True

class PrescriptionBase(BaseModel):
    doctor_name: str

class PrescriptionCreate(PrescriptionBase):
    items: List[PrescriptionItemCreate]

class PrescriptionResponse(PrescriptionBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    items: List[PrescriptionItemResponse]

    class Config:
        from_attributes = True
