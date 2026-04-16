from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import (
    auth_router,
    patients_router,
    admins_router,
    doctors_router,
    services_router,
)
from .database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Clinic Appointment System API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(patients_router)
app.include_router(admins_router)
app.include_router(doctors_router)
app.include_router(services_router)


@app.get("/")
def root():
    return {"message": "Clinic Management System API", "status": "running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
