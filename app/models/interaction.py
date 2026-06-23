from sqlalchemy import Column, Integer, String, Text
from app.core.database import Base

class DrugInteraction(Base):
    __tablename__ = "drug_interactions"

    id = Column(Integer, primary_key=True, index=True)
    drug_a_id = Column(Integer, index=True) # Reference to drug.id
    drug_b_id = Column(Integer, index=True) # Reference to drug.id
    severity = Column(String) # Severe, Moderate, Mild, None
    description = Column(Text) # Details of the interaction
    clinical_significance = Column(Text) # What happens clinically
    recommendation = Column(Text) # What to do
