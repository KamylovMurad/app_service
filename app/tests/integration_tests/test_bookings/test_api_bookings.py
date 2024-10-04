import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("room_id, date_from, date_to, booked_rooms, status_code", *[
    [(1, "2030-05-01", "2030-05-15", i, 200) for i in range(1, 6)] +
    [(1, "2030-05-01", "2030-05-15", 5, 409)] * 2
    ])
async def test_add_and_get_booking(
    authenticated_ac: AsyncClient,
    room_id, date_from,
    date_to,
    status_code,
    booked_rooms,
):
    response = await authenticated_ac.post("/bookings/add_booking", json={
        "room_id": room_id,
        "date_from": date_from,
        "date_to": date_to,
    })
    assert response.status_code == status_code
    response = await authenticated_ac.get("/bookings")
    assert len(response.json()) == booked_rooms


async def test_get_and_delete_bookings(
    authenticated_ac: AsyncClient,
):
    response = await authenticated_ac.get("/bookings")
    response_json = response.json()
    assert len(response_json) == 5
    for booking in response_json:
        booking_id = booking.get('id')
        response = await authenticated_ac.post(f"/bookings/{booking_id}")
        assert response.status_code == 200
    response = await authenticated_ac.get("/bookings")
    response_json = response.json()
    assert len(response_json) == 0
