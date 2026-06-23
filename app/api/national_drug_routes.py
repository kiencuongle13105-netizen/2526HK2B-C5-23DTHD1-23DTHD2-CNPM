from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.national_drug import DrugSyncResponse
from app.services.national_drug_service import NationalDrugAPIClient, sync_national_drug_db
from app.core.access_control import role_required

router = APIRouter(prefix="/national-drugs", tags=["National Drug API"])

@router.post("/sync", response_model=DrugSyncResponse)
async def sync_drugs(
    current_user = Depends(role_required(["admin"])), 
    db: Session = Depends(get_db)
):
    client = NationalDrugAPIClient()
    # Fetch data from national API
    drug_data = await client.fetch_all_drugs()
    
    # Sync with local database
    result = sync_national_drug_db(db, drug_data)
    return result
