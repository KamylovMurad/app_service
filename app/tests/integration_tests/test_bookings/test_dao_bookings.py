from datetime import datetime

from app.bookings.dao import BookingsDAO
import pytest


@pytest.mark.parametrize("user_id, room_id, date_from, date_to", [
    (2, 2, "09-08-2024", "12-08-2024"),
])
async def test_add_and_get_booking(user_id, room_id, date_from, date_to):
    date_from = datetime.strptime(date_from, "%d-%m-%Y")
    date_to = datetime.strptime(date_to, "%d-%m-%Y")
    new_booking = await BookingsDAO.add(
        user_id=user_id,
        room_id=room_id,
        date_from=date_from,
        date_to=date_to,
    )

    new_booking = BookingsDAO.get_by_id(model_id=new_booking.id)
    assert new_booking is not None
