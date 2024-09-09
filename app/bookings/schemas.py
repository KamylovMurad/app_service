from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel

from app.users.schemas import SchemaEmailUser


class SchemaBooking(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class SchemaEmailBooking(BaseModel):
    room_id: int
    date_from: date
    date_to: date
    user: SchemaEmailUser

class SchemaBookingSuccess(BaseModel):
    room_id: int
    date_from: date
    date_to: date
    price: Optional[Decimal] = None
    total_days: Optional[int] = None
    total_cost: Optional[Decimal] = None

    class Config:
        from_attributes = True


class SchemaBookingId(BaseModel):
    booking_id: int
