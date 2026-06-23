from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.interaction import InteractionAnalysisResponse
from app.services import interaction_service, drug_service

router = APIRouter(prefix="/interactions", tags=["Drug Interactions"])

@router.post("/check", response_model=InteractionAnalysisResponse)
def check_interactions(
    drug_ids: List[int] = Query(..., description="List of drug IDs to check for interactions"), 
    db: Session = Depends(get_db)
):
    if len(drug_ids) < 2:
        # Though not strictly an error, it's impossible to have interaction with < 2 drugs
        return {
            "overall_severity": "None",
            "interactions": [],
            "summary": "Please provide at least two drugs to check for interactions."
        }
    
    return interaction_service.analyze_interactions(db, drug_ids)

@router.post("/seed", response_model=dict)
def seed_interactions(db: Session = Depends(get_db)):
    interaction_service.seed_interaction_database(db)
    return {"message": "Interaction database seeded successfully"}
