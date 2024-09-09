from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field

from app.hotels.schemas import SchemaHotel


class RoomsImages(BaseModel):
    name: str
    path: str

    class Config:
        from_attributes = True


class RoomsSchema(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: str
    price: Decimal
    services: list[str]
    quantity_rooms: int
    hotel: SchemaHotel
    images: list[RoomsImages]

    class Config:
        from_attributes = True


class OneRoomsSchema(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: str
    price: Decimal
    services: list[str]
    quantity_rooms: int


class RoomsQueryParams(BaseModel):
    hotel_id: Optional[int] = Field(default=None)
    name: Optional[str] = Field(default=None)
    price: Optional[Decimal] = Field(default=None)
    quantity_rooms: Optional[int] = Field(default=None)

# class RoomsQueryParams1:
#
#     def __init__(
#             self,
#             hotel_id: int = Query(default=None),
#             name: str = Query(default=None),
#             price: Decimal = Query(default=None),
#             quantity_rooms: int = Query(default=None)
#     ):
#         self.hotel_id = hotel_id
#         self.name = name
#         self.price = price
#         self.quantity_rooms = quantity_rooms
