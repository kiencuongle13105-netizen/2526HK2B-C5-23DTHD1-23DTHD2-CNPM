from typing import List
from app.schemas.assessment import AssessmentResult

# Mock Knowledge Base for Medical Assessment
# In a real application, this would be a complex medical ontology or a call to a specialized medical AI API
MEDICAL_KNOWLEDGE_BASE = {
    "symptoms": {
        "headache": {"condition": "Migraine/Tension Headache", "risk": "Low"},
        "chest pain": {"condition": "Cardiovascular Issue", "risk": "Severe"},
        "shortness of breath": {"condition": "Respiratory Issue", "risk": "High"},
        "fever": {"condition": "Infection", "risk": "Moderate"},
        "dizziness": {"condition": "Neurological/Circulatory Issue", "risk": "Moderate"},
        "joint pain": {"condition": "Arthritis/Inflammation", "risk": "Low"},
    },
    "history": {
        "diabetes": {"condition": "Diabetes Mellitus", "risk": "Moderate"},
        "hypertension": {"condition": "High Blood Pressure", "risk": "Moderate"},
        "asthma": {"condition": "Asthma", "risk": "High"},
        "kidney disease": {"condition": "Renal Impairment", "risk": "Severe"},
        "liver disease": {"condition": "Hepatic Impairment", "risk": "Severe"},
    }
}

def analyze_patient_data(symptoms: str, history: str) -> AssessmentResult:
    detected_conditions = []
    max_risk = "Low"
    risk_map = {"Low": 1, "Moderate": 2, "High": 3, "Severe": 4}
    inverse_risk_map = {v: k for k, v in risk_map.items()}
    
    current_max_val = 1
    
    # Normalize input
    symptoms_text = symptoms.lower()
    history_text = history.lower()
    
    # Analyze symptoms
    for symptom, info in MEDICAL_KNOWLEDGE_BASE["symptoms"].items():
        if symptom in symptoms_text:
            detected_conditions.append(info["condition"])
            val = risk_map[info["risk"]]
            if val > current_max_val:
                current_max_val = val
                
    # Analyze medical history
    for disease, info in MEDICAL_KNOWLEDGE_BASE["history"].items():
        if disease in history_text:
            detected_conditions.append(info["condition"])
            val = risk_map[info["risk"]]
            if val > current_max_val:
                current_max_val = val
                
    # Determine final risk level
    risk_level = inverse_risk_map[current_max_val]
    
    # Generate recommendations based on risk
    recommendations = []
    if risk_level == "Severe":
        recommendations.append("Seek immediate medical attention at an emergency room.")
    elif risk_level == "High":
        recommendations.append("Schedule an urgent appointment with your primary care physician.")
    elif risk_level == "Moderate":
        recommendations.append("Monitor symptoms and consult a doctor within the next few days.")
    else:
        recommendations.append("Maintain a healthy lifestyle and track symptoms if they persist.")
        
    if detected_conditions:
        recommendations.append(f"Discuss the following detected conditions with your doctor: {', '.join(detected_conditions)}")
    else:
        recommendations.append("No specific high-risk conditions were detected based on the provided data.")

    return AssessmentResult(
        risk_level=risk_level,
        recommendations=recommendations,
        detected_conditions=detected_conditions
    )
