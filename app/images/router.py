from pathlib import Path

from fastapi import APIRouter, UploadFile
import shutil

from app.hotels.dao import HotelsDAO
from app.images.dao import ImageRoomsDAO
from app.rooms.dao import RoomsDAO

router = APIRouter(
    prefix='/images',
    tags=['Load image']
)


@router.post("/hotels")
async def add_hotel_image(file: UploadFile, name: int, hotel_id: int):
    hotel = await HotelsDAO.get_one_or_none(id=hotel_id)
    if hotel:
        await HotelsDAO.update_image_id(hotel, name)
        with open(file=f"app/static/images/hotels/{name}.jpeg", mode="wb") as file_object:
            shutil.copyfileobj(fsrc=file.file, fdst=file_object)
        return "Фотография сохранена"
    return "Отель с данным id не найден"


@router.post("/rooms/{room_id}")
async def add_room_image(
        room_id: int,
        file: UploadFile,
):
    room = await RoomsDAO.get_one_room(id=room_id)
    if room:
        file_path = Path(f'app/static/images/rooms/{room_id}/{file.filename}')
        if file_path.exists():
            return 'Данный файл уже существует'
        file_path.parent.mkdir(exist_ok=True, parents=True)
        with open(file_path, 'wb') as file_object:
            shutil.copyfileobj(fsrc=file.file, fdst=file_object)
        file_path_on_save = Path(f'images/rooms/{room_id}/{file.filename}')
        await ImageRoomsDAO.add(name=file.filename, path=file_path_on_save.as_posix(), room_id=room_id)
        return "Файл создан"
    return 'Номер с данным id не найден'
    # print(list(Path(f'app/static/images/rooms/{room_id}').glob('*.jp*g')))
