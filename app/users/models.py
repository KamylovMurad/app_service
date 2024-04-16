from typing import Optional

from sqlalchemy import Column, String
from app.db import Model
from sqlalchemy.orm import validates
from sqlalchemy.orm import Mapped, mapped_column


class Users(Model):
    __tablename__ = 'users'

    email: Mapped[str]
    name: Mapped[Optional[str]]
    password: Mapped[str]
    role: Mapped[Optional[str]] = mapped_column(default="client")

    @validates('email')
    def validate_email(self, key, value):
        assert '@' in value, f"Email address for column {key} must contain @ symbol"
        return value