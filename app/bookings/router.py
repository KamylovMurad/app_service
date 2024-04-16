from datetime import date

from fastapi import APIRouter, Request, Depends, status
from fastapi.responses import JSONResponse
from app.bookings.dao import BookingsDAO
from app.bookings.schemas import SchemaBooking, SchemaBookingId
from app.users.dependencies import get_user
from app.users.models import Users
from app.exceptions import RoomsConflictException

router = APIRouter(prefix='/bookings', tags=['Bookings'])


@router.post("/add_booking")
async def add_booking(
        request: Request,
        booking: SchemaBooking,
        user: Users = Depends(get_user)
):
    bookings = await BookingsDAO.add(user.id, booking.room_id, booking.date_from, booking.date_to)
    if not bookings:
        raise RoomsConflictException
    return bookings


@router.post("/{booking_id}")
async def delete_booking(booking_id: int, request: Request, user: Users = Depends(get_user)):
    result = await BookingsDAO.delete_booking(booking_id, user.id)
    if result:
        return {"Answer": f"Booking with id {result} deleted"}


@router.get("")
async def get_bookings(user: Users = Depends(get_user)):
    # return await BookingsDAO.get_all(user_id=user.id)
    return await BookingsDAO.get_bookings(user_id=user.id)


@router.get('test')
async def test_bookings(
        room_id: int,
        date_from: date,
        date_to: date
):
    return await BookingsDAO.test_func(room_id, date_from, date_to)
