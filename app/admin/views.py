from sqladmin import ModelView

from app.bookings.models import Bookings
from app.hotels.models import Hotels
from app.rooms.models import Rooms, ImageRooms
from app.users.models import Users


class UserAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.name, Users.email]
    can_delete = False
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"
    column_details_exclude_list = [Users.password]


class BookingsAdmin(ModelView, model=Bookings):
    column_list = [c.name for c in Bookings.__table__.c] + [Bookings.user, Bookings.room]
    name = "Бронь"
    name_plural = "Брони"
    icon = "fa-solid fa-book"


class HotelsAdmin(ModelView, model=Hotels):
    column_list = [c.name for c in Hotels.__table__.c]
    name = "Отель"
    name_plural = "Отели"
    icon = "fa-solid fa-hotel"


class RoomsAdmin(ModelView, model=Rooms):
    column_list = [c.name for c in Rooms.__table__.c]
    name = "Номер"
    name_plural = "Номера"
    icon = "fa-solid fa-bed"


class ImageRoomsAdmin(ModelView, model=ImageRooms):
    column_list = [ImageRooms.room, ImageRooms.name, ImageRooms.path]
    name = "Картинка"
    name_plural = "Картинки"
    icon = "fa-solid fa-image"