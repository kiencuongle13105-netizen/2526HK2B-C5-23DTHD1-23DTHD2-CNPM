from fastapi import FastAPI
from app.api.user_routes import router as user_router
from app.api.auth_routes import router as auth_router
from app.api.patient_routes import router as patient_router
from app.api.symptom_routes import router as symptom_router
from app.api.assessment_routes import router as assessment_router
from app.api.prescription_routes import router as prescription_router
from app.api.prescription_history_routes import router as prescription_history_router
from app.api.drug_routes import router as drug_router
from app.api.interaction_routes import router as interaction_router
from app.api.reminder_routes import router as reminder_router
from app.api.notification_routes import router as notification_router
from app.api.statistics_routes import router as statistics_router
from app.api.prescription_stats_routes import router as prescription_stats_router
from app.api.national_drug_routes import router as national_drug_router
from app.core.database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Drug Interaction Checker Backend")

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(patient_router)
app.include_router(symptom_router)
app.include_router(assessment_router)
app.include_router(prescription_router)
app.include_router(prescription_history_router)
app.include_router(drug_router)
app.include_router(interaction_router)
app.include_router(reminder_router)
app.include_router(notification_router)
app.include_router(statistics_router)
app.include_router(prescription_stats_router)
app.include_router(national_drug_router)

@app.get("/")
def root():
    return {"message": "Welcome to the Drug Interaction Checker API"}
