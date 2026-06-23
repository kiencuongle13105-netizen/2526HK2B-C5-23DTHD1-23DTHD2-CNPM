from pydantic import BaseModel
from typing import Dict, List

class PatientStatsResponse(BaseModel):
    total_patients: int
    patients_by_role: Dict[str, int]
    total_prescriptions: int
    total_symptoms_reported: int
    disease_distribution: Dict[str, int] # e.g., {"Diabetes": 10, "Hypertension": 5}
