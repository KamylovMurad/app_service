from datetime import date

from pydantic import BaseModel


class SchemaBooking(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class SchemaBookingId(BaseModel):
    booking_id: int
