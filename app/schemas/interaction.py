from pydantic import BaseModel
from typing import List, Optional

class InteractionDetail(BaseModel):
    drug_a: str
    drug_b: str
    severity: str
    description: str
    clinical_significance: Optional[str] = None
    recommendation: Optional[str] = None

class InteractionAnalysisResponse(BaseModel):
    overall_severity: str # Severe, Moderate, Mild, None
    interactions: List[InteractionDetail]
    summary: str
