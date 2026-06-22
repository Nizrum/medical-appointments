from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi
from fastapi.encoders import jsonable_encoder
from starlette.exceptions import HTTPException as StarletteHTTPException

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
                phone="88888888888",
                role="admin",
                is_active=True,
            )
            db.add(admin_user)
        db.commit()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": jsonable_encoder(exc.errors())},
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 400 and "JSON" in str(exc.detail):
        return JSONResponse(
            status_code=400,
            content={"detail": "Invalid request body - malformed JSON"},
            headers=exc.headers,
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers=exc.headers,
    )


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes,
    )

    error_400 = {"description": "Bad Request"}
    error_401 = {"description": "Unauthorized"}
    error_403 = {"description": "Forbidden"}
    error_404 = {"description": "Not Found"}
    error_409 = {"description": "Conflict"}

    for path, path_item in openapi_schema.get("paths", {}).items():
        for method, operation in path_item.items():
            if method not in ("get", "post", "put", "delete", "patch"):
                continue

            responses = operation.setdefault("responses", {})

            if operation.get("security"):
                responses.setdefault("401", error_401)
                responses.setdefault("403", error_403)

            if method in ("post", "put", "patch"):
                responses.setdefault("400", error_400)

            if "{" in path:
                responses.setdefault("404", error_404)

            if path.startswith("/auth/register") and method == "post":
                responses.setdefault("409", error_409)
            if path == "/auth/me" and method == "put":
                responses.setdefault("409", error_409)

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


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
