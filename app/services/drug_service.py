from sqlalchemy.orm import Session
from app.models.drug import Drug
from app.schemas.drug import DrugCreate

def search_drugs(db: Session, query: str):
    # Search by name or generic name (case-insensitive)
    return db.query(Drug).filter(
        (Drug.name.ilike(f"%{query}%")) | 
        (Drug.generic_name.ilike(f"%{query}%"))
    ).limit(20).all()

def create_drug(db: Session, drug_data: DrugCreate):
    db_drug = Drug(**drug_data.dict())
    db.add(db_drug)
    db.commit()
    db.refresh(db_drug)
    return db_drug

def seed_drug_database(db: Session):
    # Initial set of common drugs for testing
    sample_drugs = [
        {"name": "Paracetamol", "generic_name": "Acetaminophen", "category": "Analgesic", "description": "Pain reliever and fever reducer."},
        {"name": "Aspirin", "generic_name": "Acetylsalicylic acid", "category": "NSAID", "description": "Pain reliever and anti-inflammatory."},
        {"name": "Amoxicillin", "generic_name": "Amoxicillin", "category": "Antibiotic", "description": "Penicillin-type antibiotic."},
        {"name": "Metformin", "generic_name": "Metformin", "category": "Antidiabetic", "description": "Used for type 2 diabetes."},
        {"name": "Lisinopril", "generic_name": "Lisinopril", "category": "ACE Inhibitor", "description": "Used for hypertension."},
        {"name": "Atorvastatin", "generic_name": "Atorvastatin", "category": "Statin", "description": "Lowers cholesterol."},
        {"name": "Warfarin", "generic_name": "Warfarin", "category": "Anticoagulant", "description": "Prevents blood clots."},
        {"name": "Sertraline", "generic_name": "Sertraline", "category": "SSRI", "description": "Used for depression and anxiety."},
    ]
    
    for drug in sample_drugs:
        # Avoid duplicates
        exists = db.query(Drug).filter(Drug.name == drug["name"]).first()
        if not exists:
            db.add(Drug(**drug))
    
    db.commit()
