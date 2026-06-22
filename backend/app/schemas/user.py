from pydantic import BaseModel, EmailStr, Field, ConfigDict, AfterValidator, field_validator
from datetime import datetime
from typing import Annotated, Optional
import email_validator


def normalize_email(value: str) -> str:
    if not value or not isinstance(value, str):
        raise ValueError("invalid email address")
    try:
        validated = email_validator.validate_email(
            value, check_deliverability=False
        )
        return validated.ascii_email
    except email_validator.EmailNotValidError as exc:
        raise ValueError(str(exc)) from exc


def sanitize_text(value: Optional[str]) -> Optional[str]:
    if value is None or not isinstance(value, str):
        return value
    cleaned = value.encode("utf-8", errors="ignore").decode("utf-8")
    return cleaned.replace("\x00", "")


AsciiEmailStr = Annotated[EmailStr, AfterValidator(normalize_email)]


class UserBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: AsciiEmailStr
    full_name: str = Field(..., min_length=1, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    role: str = Field(..., pattern="^patient$")

    @field_validator("full_name", "phone", mode="before")
    @classmethod
    def sanitize_string_fields(cls, value: Optional[str]) -> Optional[str]:
        return sanitize_text(value)


class UserCreate(UserBase):
    password: str = Field(..., min_length=4, max_length=72)


class UserLogin(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: AsciiEmailStr
    password: str = Field(..., min_length=1, max_length=72)


class UserUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: Optional[AsciiEmailStr] = None
    full_name: Optional[str] = Field(None, min_length=1, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    password: Optional[str] = Field(None, min_length=4, max_length=72)

    @field_validator("full_name", "phone", mode="before")
    @classmethod
    def sanitize_string_fields(cls, value: Optional[str]) -> Optional[str]:
        return sanitize_text(value)


class UserResponse(BaseModel):
    id: int
    email: AsciiEmailStr
    full_name: str
    phone: Optional[str] = None
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserRoleUpdate(BaseModel):
    role: str = Field(..., pattern="^(patient|doctor|admin)$")


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
