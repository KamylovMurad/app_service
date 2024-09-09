from typing import Optional, List, TYPE_CHECKING

from sqlalchemy import Column, String

from app.db import Model
from sqlalchemy.orm import validates
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from bookings.models import Bookings


class Users(Model):
    __tablename__ = 'users'

    email: Mapped[str]
    name: Mapped[Optional[str]]
    password: Mapped[str]
    role: Mapped[Optional[str]] = mapped_column(default="client")
    bookings: Mapped[List["Bookings"]] = relationship(back_populates='user')

    @validates('email')
    def validate_email(self, key, value):
        assert '@' in value, f"Email address for column {key} must contain @ symbol"
        return value

    def __str__(self):
        return f'{self.email}'
