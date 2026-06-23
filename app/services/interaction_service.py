from sqlalchemy.orm import Session
from app.models.drug import Drug
from app.models.interaction import DrugInteraction
from app.schemas.interaction import InteractionAnalysisResponse, InteractionDetail

def analyze_interactions(db: Session, drug_ids: list[int]) -> InteractionAnalysisResponse:
    found_interactions = []
    max_risk_val = 0
    risk_map = {"None": 0, "Mild": 1, "Moderate": 2, "Severe": 3}
    inverse_risk_map = {v: k for k, v in risk_map.items()}
    
    # Compare all pairs of drugs
    for i in range(len(drug_ids)):
        for j in range(i + 1, len(drug_ids)):
            drug_a_id = drug_ids[i]
            drug_b_id = drug_ids[j]
            
            # Search in both directions (A-B or B-A)
            interaction = db.query(DrugInteraction).filter(
                ((DrugInteraction.drug_a_id == drug_a_id) & (DrugInteraction.drug_b_id == drug_b_id)) |
                ((DrugInteraction.drug_a_id == drug_b_id) & (DrugInteraction.drug_b_id == drug_a_id))
            ).first()
            
            if interaction:
                drug_a = db.query(Drug).filter(Drug.id == drug_a_id).first()
                drug_b = db.query(Drug).filter(Drug.id == drug_b_id).first()
                
                found_interactions.append(InteractionDetail(
                    drug_a=drug_a.name,
                    drug_b=drug_b.name,
                    severity=interaction.severity,
                    description=interaction.description,
                    clinical_significance=interaction.clinical_significance,
                    recommendation=interaction.recommendation
                ))
                
                # Update overall severity
                risk_val = risk_map.get(interaction.severity, 0)
                if risk_val > max_risk_val:
                    max_risk_val = risk_val
    
    overall_severity = inverse_risk_map[max_risk_val]
    
    # Generate summary
    if not found_interactions:
        summary = "No significant interactions detected between the selected drugs."
    elif overall_severity == "Severe":
        summary = "DANGER: Severe interactions detected. Immediate medical consultation required."
    elif overall_severity == "Moderate":
        summary = "Warning: Moderate interactions detected. Please consult your doctor for dosage adjustments."
    else:
        summary = "Caution: Mild interactions detected. Generally safe but should be monitored."
        
    return InteractionAnalysisResponse(
        overall_severity=overall_severity,
        interactions=found_interactions,
        summary=summary
    )

def seed_interaction_database(db: Session):
    # Get sample drugs to create interaction pairs
    drugs = db.query(Drug).all()
    if len(drugs) < 2:
        return
    
    # Create some mock interactions between common drugs
    # e.g., Aspirin and Warfarin (Severe)
    aspirin = next((d for d in drugs if d.name == "Aspirin"), None)
    warfarin = next((d for d in drugs if d.name == "Warfarin"), None)
    
    if aspirin and warfarin:
        interaction = DrugInteraction(
            drug_a_id=aspirin.id,
            drug_b_id=warfarin.id,
            severity="Severe",
            description="Increased risk of bleeding due to combined anticoagulant effects.",
            clinical_significance="Potentially life-threatening hemorrhage.",
            recommendation="Avoid concurrent use. Use alternative therapy or strictly monitor INR."
        )
        db.add(interaction)
    
    # e.g., Metformin and contrast dye (Moderate)
    metformin = next((d for d in drugs if d.name == "Metformin"), None)
    if metformin and len(drugs) > 1:
        other_drug = drugs[0] if drugs[0].id != metformin.id else drugs[1]
        interaction = DrugInteraction(
            drug_a_id=metformin.id,
            drug_b_id=other_drug.id,
            severity="Moderate",
            description="Potential for lactic acidosis in patients with renal impairment.",
            clinical_significance="Metabolic acidosis.",
            recommendation="Temporary discontinuation of metformin before imaging procedures with contrast."
        )
        db.add(interaction)
        
    db.commit()
