from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import (
    auth_router,
    patients_router,
    admins_router,
    doctors_router,
    services_router,
)
from .api.auth import get_password_hash, truncate_password
from .config import settings
from .database import engine, Base, SessionLocal
from .models.user import User

app = FastAPI(title="Clinic Appointment System API", version="1.0.0")


def init_database():
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        existing_admin = db.query(User).filter(User.role == "admin").first()
        if existing_admin:
            return

        admin_user = (
            db.query(User).filter(User.email == settings.admin_email).first()
        )
        if admin_user:
            admin_user.role = "admin"
            admin_user.hashed_password = get_password_hash(
                truncate_password(settings.admin_password)
            )
            admin_user.is_active = True
        else:
            admin_user = User(
                email=settings.admin_email,
                hashed_password=get_password_hash(
                    truncate_password(settings.admin_password)
                ),
                full_name="Администратор",
                phone="",
                role="admin",
                is_active=True,
            )
            db.add(admin_user)
        db.commit()


@app.on_event("startup")
def on_startup():
    init_database()


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
