import httpx
import asyncio
from sqlalchemy.orm import Session
from app.models.drug import Drug
from app.schemas.national_drug import NationalDrugData, DrugSyncResponse
from app.core.config import settings

class NationalDrugAPIClient:
    def __init__(self):
        # Mock URL: In reality, this would be a real government drug API
        self.base_url = "https://api.nationaldrugdb.gov/v1" 
        self.api_key = "DEMO_KEY_12345"

    async def fetch_drug_data(self, drug_name: str):
        """Fetch a single drug's data from national API"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/drugs/{drug_name}", 
                    headers={"X-API-KEY": self.api_key},
                    timeout=10.0
                )
                if response.status_code == 200:
                    return NationalDrugData(**response.json())
                return None
        except Exception as e:
            print(f"Error fetching drug {drug_name}: {e}")
            return None

    async def fetch_all_drugs(self):
        """Fetch all drugs from national API (Mocked)"""
        # Since there's no real API, we'll simulate the response
        # in a real scenario, we'd use pagination to fetch thousands of records
        await asyncio.sleep(1) # Simulate network delay
        return [
            {"drug_id": "ND001", "name": "Paracetamol", "generic_name": "Acetaminophen", "category": "Analgesics"},
            {"drug_id": "ND002", "name": "Aspirin", "generic_name": "Acetylsalicylic acid", "category": "Antiplatelets"},
        ]

def sync_national_drug_db(db: Session, drug_data_list: list):
    """
    Sync fetched data into the local Drug model.
    Updates if drug exists (by name), creates otherwise.
    """
    synced_count = 0
    updated_count = 0
    errors = []

    for data in drug_data_list:
        try:
            # Normalize data to match NationalDrugData schema
            drug_info = NationalDrugData(**data)
            
            drug = db.query(Drug).filter(Drug.name == drug_info.name).first()
            if drug:
                drug.generic_name = drug_info.generic_name
                drug.category = drug_info.category
                drug.indications = drug_info.indications
                drug.contraindications = drug_info.contraindications
                drug.side_effects = drug_info.side_effects
                updated_count += 1
            else:
                new_drug = Drug(
                    name=drug_info.name,
                    generic_name=drug_info.generic_name,
                    category=drug_info.category,
                    indications=drug_info.indications,
                    contraindications=drug_info.contraindications,
                    side_effects=drug_info.side_effects
                )
                db.add(new_drug)
                synced_count += 1
        except Exception as e:
            errors.append(f"Error syncing {data.get('name', 'Unknown')}: {str(e)}")

    db.commit()
    return DrugSyncResponse(synced_count=synced_count, updated_count=updated_count, errors=errors)
