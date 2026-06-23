from pydantic import BaseModel
from typing import List, Dict
from datetime import date

class TimeSeriesDataPoint(BaseModel):
    period: str # e.g., "2026-06" or "2026-06-23"
    count: int

class PrescriptionTimeStatsResponse(BaseModel):
    total_prescriptions: int
    stats: List[TimeSeriesDataPoint]
    trend: str # "increasing", "decreasing", "stable"
