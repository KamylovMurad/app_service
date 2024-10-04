from datetime import datetime

import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("hotel_id, date_from, date_to, status_code", [
    (1, "2022-06-06", "2022-06-05", 400),
    (1, "2022-06-04", "2022-06-05", 200),
])
async def test_get_rooms_by_hotel(authenticated_ac: AsyncClient, hotel_id, date_from, date_to, status_code):
    response = await authenticated_ac.get(f"/hotels/{hotel_id}/rooms", params={
        "date_from": date_from,
        "date_to": date_to
    })

    assert response.status_code == status_code


@pytest.mark.parametrize("hotel_id, date_from, date_to, status_code", [
    (1, "2022-06-05", "2022-03-06", 400),
    (1, "2022-06-03", "2022-05-04", 400),
])
async def test_check_out_more_than_30_days(authenticated_ac: AsyncClient, hotel_id, date_from, date_to, status_code):
    response = await authenticated_ac.get(f"/hotels/{hotel_id}/rooms", params={
        "date_from": date_from,
        "date_to": date_to
    })

    date_from = datetime.strptime(date_from, "%Y-%m-%d")
    date_to = datetime.strptime(date_to, "%Y-%m-%d")
    assert response.status_code == status_code
    assert (date_from - date_to).days >= 30
