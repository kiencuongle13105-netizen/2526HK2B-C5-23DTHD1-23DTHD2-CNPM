from pydantic import BaseModel
from typing import Optional, List

class NationalDrugData(BaseModel):
    drug_id: str
    name: str
    generic_name: Optional[str] = None
    category: Optional[str] = None
    indications: Optional[str] = None
    contraindications: Optional[str] = None
    side_effects: Optional[str] = None
    manufacturer: Optional[str] = None
    approval_date: Optional[str] = None

class DrugSyncResponse(BaseModel):
    synced_count: int
    updated_count: int
    errors: List[str]
