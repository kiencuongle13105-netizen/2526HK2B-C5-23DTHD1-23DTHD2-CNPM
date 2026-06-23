from fastapi import FastAPI
from app.api.user_routes import router as user_router
from app.api.auth_routes import router as auth_router
from app.api.patient_routes import router as patient_router
from app.core.database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Drug Interaction Checker Backend")

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(patient_router)

@app.get("/")
def root():
    return {"message": "Welcome to the Drug Interaction Checker API"}
