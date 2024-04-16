from datetime import date
from typing import Optional

from fastapi import Query
from pydantic import BaseModel, Field


class SchemaHotel(BaseModel):
    # address: str
    # name: str
    # stars: int = Field(gt=0, lt=6, default=None)
    # has_spa: bool = Field(default=False)
    name: str
    location: str
    # services: str
    rooms_quantity: int
    image_id: int


# @dataclass
# class HotelSearchArgs:
#     location: str
#     date_from: date
#     date_to: date
#     has_spa: bool = Query(default=None),
#     stars: int = Query(default=None, ge=1, le=5)

# class HotelSearchArgs:
#     def __init__(
#             self,
#             location: str,
#             date_from: date,
#             date_to: date,
#             has_spa: bool = Query(default=None),
#             stars: int = Query(default=None, ge=1, le=5)
#     ):
#         self.location = location
#         self.date_from = date_from
#         self.date_to = date_to
#         self.has_spa = has_spa
#         self.stars = stars


class HotelSearchArgs(BaseModel):
    # location: str
    date_from: date
    date_to: date
    has_spa: Optional[bool] = Field(default=None)
    stars: Optional[int] = Field(default=None, ge=1, le=5)
