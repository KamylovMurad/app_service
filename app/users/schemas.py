from typing import Any, Optional

from pydantic import BaseModel, EmailStr, field_validator


class SchemaEmailUser(BaseModel):
    email: EmailStr


class SchemaUser(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    password: str

    @field_validator("email")
    def validate_field(cls, value):
        if not value.endswith(".ru") and not value.endswith(".com"):  # or not value.endswith(".com")
            raise ValueError("Email должен заканчиваться на '.ru' или '.com'")
        return value


class SchemaAboutUser(BaseModel):
    email: EmailStr
    name: str


class SchemaUserV2(BaseModel):
    role: Optional[str] = None
    id: int
    email: EmailStr
    name: Optional[str] = None
    password: str



    @field_validator("email")
    def validate_field(cls, value):
        if not value.endswith(".ru") and not value.endswith(".com"):  # or not value.endswith(".com")
            raise ValueError("Email должен заканчиваться на '.ru' или '.com'")
        return value