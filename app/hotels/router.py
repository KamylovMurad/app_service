from datetime import date

import sqlalchemy.exc
from fastapi import APIRouter
from fastapi import Depends
from fastapi_cache.decorator import cache

from app.exceptions import HotelNotFoundException
from app.hotels.dao import HotelsDAO
from app.hotels.schemas import HotelSearchArgs

router = APIRouter(prefix='/hotels', tags=['Hotels'])


@router.get("")
@cache(expire=30)
async def get_all():
    return await HotelsDAO.get_all()


@router.get("/{hotel_id}/rooms")
@cache(expire=30)
async def get_rooms_by_hotel(hotel_id: int, date_from: date, date_to: date):
    return await HotelsDAO.get_rooms_by_hotel(hotel_id, date_from, date_to)


@router.get("/{city}")
@cache(expire=30)
async def get_hotels_by_city(
        city: str,
        search_args: HotelSearchArgs = Depends()
):
    return await HotelsDAO.get_hotel_by_city(city, search_args.date_from, search_args.date_to)


@router.get("/id/{hotel_id}")
@cache(expire=30)
async def get_hotel(hotel_id: int):
    try:
        return await HotelsDAO.get_by_id(model_id=hotel_id)
    except sqlalchemy.exc.NoResultFound:
        raise HotelNotFoundException
