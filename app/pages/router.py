from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from app.hotels.router import get_hotels_by_city
from app.rooms.router import get_rooms
from app.rooms.schemas import RoomsSchema

router = APIRouter(
    prefix='/pages',
    tags=['Frontend']
)

templates = Jinja2Templates(directory="app/templates")


@router.get("/hotels")
async def ger_hotels_page(
        request: Request,
        hotels=Depends(dependency=get_hotels_by_city)
):
    return templates.TemplateResponse(
        name='hotels.html',
        context={
            'request': request,
            'hotels': hotels
        }
    )


@router.get("/rooms_by_hotel")
async def get_rooms_by_hotels(
        request: Request,
        rooms=Depends(dependency=get_rooms)
):
    rooms = [RoomsSchema.model_validate(room) for room in rooms]
    return templates.TemplateResponse(
        name='rooms.html',
        context={
            'request': request,
            'rooms': rooms
        }
    )