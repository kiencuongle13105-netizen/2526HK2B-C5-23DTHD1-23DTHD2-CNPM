from sqlalchemy.orm import Session
from app.models.prescription import Prescription, PrescriptionItem
from app.schemas.prescription import PrescriptionCreate

def create_prescription(db: Session, user_id: int, data: PrescriptionCreate):
    # Create main prescription
    db_prescription = Prescription(
        user_id=user_id,
        doctor_name=data.doctor_name
    )
    db.add(db_prescription)
    db.flush() # Get the prescription ID

    # Create items
    for item_data in data.items:
        db_item = PrescriptionItem(
            prescription_id=db_prescription.id,
            drug_name=item_data.drug_name,
            dosage=item_data.dosage,
            frequency=item_data.frequency,
            duration=item_data.duration
        )
        db.add(db_item)
    
    db.commit()
    db.refresh(db_prescription)
    return db_prescription

def update_prescription(db: Session, prescription_id: int, data: PrescriptionCreate):
    db_prescription = db.query(Prescription).filter(Prescription.id == prescription_id).first()
    if not db_prescription:
        return None
    
    db_prescription.doctor_name = data.doctor_name
    
    # Remove old items and add new ones (simpler than updating each)
    db.query(PrescriptionItem).filter(PrescriptionItem.prescription_id == prescription_id).delete()
    
    for item_data in data.items:
        db_item = PrescriptionItem(
            prescription_id=prescription_id,
            drug_name=item_data.drug_name,
            dosage=item_data.dosage,
            frequency=item_data.frequency,
            duration=item_data.duration
        )
        db.add(db_item)
    
    db.commit()
    db.refresh(db_prescription)
    return db_prescription

def get_user_prescriptions(db: Session, user_id: int):
    return db.query(Prescription).filter(Prescription.user_id == user_id).all()
