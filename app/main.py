from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine, SessionLocal

# -----------------------------
# Import Models
# -----------------------------
from app.models.patient import Patient
from app.models.assessment import Assessment
from app.models.prediction import Prediction
from app.models.alert import Alert
from app.models.intervention import Intervention
from app.models.user import User

# -----------------------------
# Import Routers
# -----------------------------
from app.routes.patients import router as patient_router
from app.routes.assessments import router as assessment_router
from app.routes.predictions import router as prediction_router
from app.routes.alerts import router as alert_router
from app.routes.interventions import router as intervention_router
from app.routes.dashboard import router as dashboard_router
from app.routes.users import router as user_router
from app.routes.auth import router as auth_router

# -----------------------------
# Import Admin Initialization
# -----------------------------
from app.services.init_admin import create_default_admin

# -----------------------------
# Create Database Tables
# -----------------------------
Base.metadata.create_all(bind=engine)

# -----------------------------
# Create Default Admin
# -----------------------------
db = SessionLocal()

try:
    create_default_admin(db)
finally:
    db.close()

# -----------------------------
# FastAPI Application
# -----------------------------
app = FastAPI(
    title="MG AI Remote Monitoring API",
    version="1.0.0",
    description="""
AI-Based Remote Monitoring System
for Myasthenia Gravis (MG)

Features

• Patient Management
• Clinical Assessments
• AI Prediction Engine
• Alert Management
• Intervention Tracking
• Dashboard Analytics
• JWT Authentication
• Role-Based Authorization
"""
)

# ====================================================
# CORS CONFIGURATION (FLEXIBLE LOCAL DEV ORIGINS)
# ====================================================

origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:5175",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    "http://127.0.0.1:5175",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ====================================================
# REGISTER ROUTERS
# ====================================================

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(patient_router)
app.include_router(assessment_router)
app.include_router(prediction_router)
app.include_router(alert_router)
app.include_router(intervention_router)
app.include_router(dashboard_router)

# -----------------------------
# Root Endpoint
# -----------------------------
@app.get("/")
def root():
    return {
        "application": "MG AI Remote Monitoring API",
        "version": "1.0.0",
        "status": "Running"
    }

# -----------------------------
# Health Check
# -----------------------------
@app.get("/health")
def health():
    return {
        "status": "Healthy",
        "database": "Connected",
        "authentication": "Enabled",
        "model_stage": "Development"
    }