from fastapi import APIRouter, Depends

from app.db import async_session_maker
from app.rooms.dao import RoomsDAO
from app.rooms.models import Rooms
from app.rooms.schemas import RoomsSchema, RoomsQueryParams, OneRoomsSchema

router = APIRouter(prefix='/rooms', tags=['Rooms'])


@router.get("")
async def get_rooms(query: RoomsQueryParams = Depends()) -> list[RoomsSchema]:
    result = await RoomsDAO.get_room_with_images(**query.model_dump(exclude_none=True))
    return result


@router.get("/room")
async def get_room() -> OneRoomsSchema:
    result = await RoomsDAO.get_by_id(model_id=11)
    return result


@router.get("/one")
async def get_one_or_none():
    result = await RoomsDAO.get_one_room(id=5)
    return result


from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload
from fastapi.encoders import jsonable_encoder

@router.get("/example/orm")
async def get_noorm():
    async with async_session_maker() as session:
        query = (
            select(Rooms)
            .options(joinedload(Rooms.hotel))
            .options(selectinload(Rooms.images))
            .options(selectinload(Rooms.bookings))
        )
        res = await session.execute(query)
        res = res.scalars().all()
        res = jsonable_encoder(res)
        return res