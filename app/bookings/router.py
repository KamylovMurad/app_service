import smtplib

import asyncio
import datetime

from asyncio import sleep
from datetime import date, timezone

from fastapi import APIRouter, Request, Depends, status
from fastapi.responses import JSONResponse
from app.bookings.dao import BookingsDAO
from app.bookings.schemas import SchemaBooking, SchemaBookingId, SchemaBookingSuccess
from app.bookings.tasks import send_booking_confirmation_email
from app.config import settings
from app.email_templates import remind_booking_reservation_template
from app.users.dependencies import get_user
from app.users.models import Users
from app.exceptions import RoomsConflictException
from app.users.schemas import SchemaEmailUser

router = APIRouter(prefix='/bookings', tags=['Bookings'])


@router.post("/add_booking")
async def add_booking(
        request: Request,
        booking: SchemaBooking,
        user: Users = Depends(get_user)
) -> SchemaBookingSuccess:
    bookings = await BookingsDAO.add(user.id, booking.room_id, booking.date_from, booking.date_to)
    if not bookings:
        raise RoomsConflictException
    booking = SchemaBookingSuccess.model_validate(bookings)
    send_booking_confirmation_email.delay(booking.model_dump(), user.email)
    return bookings


@router.post("/{booking_id}")
async def delete_booking(booking_id: int, request: Request, user: Users = Depends(get_user)):
    result = await BookingsDAO.delete_booking(booking_id, user.id)
    if result:
        return {"Answer": f"Booking with id {result} deleted"}


@router.get("")
async def get_bookings(user: Users = Depends(get_user)):
    return await BookingsDAO.get_bookings(user_id=user.id)

