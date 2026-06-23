from pydantic import BaseModel
from typing import Optional

class DrugBase(BaseModel):
    name: str
    generic_name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    indications: Optional[str] = None
    contraindications: Optional[str] = None
    side_effects: Optional[str] = None

class DrugCreate(DrugBase):
    pass

class DrugResponse(DrugBase):
    id: int

    class Config:
        from_attributes = True
