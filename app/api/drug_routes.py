from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.drug import DrugResponse, DrugCreate
from app.services import drug_service

router = APIRouter(prefix="/drugs", tags=["Drug Database"])

@router.get("/search", response_model=List[DrugResponse])
def search_drugs(
    q: str = Query(..., min_length=1, description="Search drug by name or generic name"), 
    db: Session = Depends(get_db)
):
    return drug_service.search_drugs(db, q)

@router.post("/seed", response_model=List[DrugResponse])
def seed_database(db: Session = Depends(get_db)):
    drug_service.seed_drug_database(db)
    return drug_service.search_drugs(db, "") # Return all seeded drugs
