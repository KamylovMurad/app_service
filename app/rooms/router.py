from fastapi import APIRouter, Depends
from app.rooms.dao import RoomsDAO
from app.rooms.schemas import RoomsSchema, RoomsQueryParams, OneRoomsSchema

router = APIRouter(prefix='/rooms', tags=['Rooms'])


@router.get("")
async def get_rooms(query: RoomsQueryParams = Depends()) -> list[RoomsSchema]:
    result = await RoomsDAO.test_all(**query.dict(exclude_none=True))
    return result


@router.get("/room")
async def get_room() -> OneRoomsSchema:
    result = await RoomsDAO.get_by_id(model_id=11)
    return result


@router.get("/one")
async def get_one_or_none() -> RoomsSchema:
    result = await RoomsDAO.get_one_room(quantity_rooms=5)
    return result
