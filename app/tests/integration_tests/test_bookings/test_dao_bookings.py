from datetime import datetime

from app.bookings.dao import BookingsDAO
import pytest


@pytest.mark.parametrize("user_id, room_id, date_from, date_to", [
    (2, 2, "09-08-2024", "12-08-2024"),
    (1, 4, "10-11-2024", "17-11-2024"),
])
async def test_crud_bookings(user_id, room_id, date_from, date_to):
    date_from = datetime.strptime(date_from, "%d-%m-%Y")
    date_to = datetime.strptime(date_to, "%d-%m-%Y")
    new_booking = await BookingsDAO.add(
        user_id=user_id,
        room_id=room_id,
        date_from=date_from,
        date_to=date_to,
    )
    new_booking = await BookingsDAO.get_by_id(model_id=new_booking.id)
    assert new_booking is not None
    assert new_booking.room_id == room_id
    deleted_booking = await BookingsDAO.delete_booking(booking_id=new_booking.id, user_id=user_id)
    assert deleted_booking == new_booking.id

