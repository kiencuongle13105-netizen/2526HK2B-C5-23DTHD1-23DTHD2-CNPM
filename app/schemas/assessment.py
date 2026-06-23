from pydantic import BaseModel
from typing import List, Optional

class AssessmentResult(BaseModel):
    risk_level: str # Low, Moderate, High, Severe
    recommendations: List[str]
    detected_conditions: List[str]
    disclaimer: str = "This is an AI-generated assessment. Please consult a medical professional for a formal diagnosis."

class MedicalAssessmentResponse(BaseModel):
    user_id: int
    assessment: AssessmentResult
