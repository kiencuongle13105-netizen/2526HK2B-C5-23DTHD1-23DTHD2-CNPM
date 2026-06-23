from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.models.prescription import Prescription, PrescriptionItem
from app.schemas.prescription_filter import PrescriptionHistoryFilter

def get_filtered_prescriptions(db: Session, user_id: int, filters: PrescriptionHistoryFilter, skip: int = 0, limit: int = 10):
    query = db.query(Prescription).filter(Prescription.user_id == user_id)
    
    if filters.start_date:
        query = query.filter(Prescription.created_at >= filters.start_date)
    if filters.end_date:
        query = query.filter(Prescription.created_at <= filters.end_date)
    if filters.doctor_name:
        query = query.filter(Prescription.doctor_name.ilike(f"%{filters.doctor_name}%"))
        
    if filters.keyword:
        # Join with items to filter by drug name
        query = query.join(PrescriptionItem).filter(PrescriptionItem.drug_name.ilike(f"%{filters.keyword}%"))
    
    return query.order_by(Prescription.created_at.desc()).offset(skip).limit(limit).all()
