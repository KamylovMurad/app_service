from typing import Optional

from fastapi import HTTPException, status


class BookingException(HTTPException):
    detail = ""
    status_code = 404

    def __init__(self, detail: Optional[str] = None):
        super().__init__(status_code=self.status_code, detail=detail or self.detail)


class TokenMissingException(BookingException):
    detail = "Пользователь не авторизован"
    status_code = status.HTTP_401_UNAUTHORIZED


class TokenTimeOverException(BookingException):
    detail = "Время жизни токена окончено или отсутствует"
    status_code = status.HTTP_401_UNAUTHORIZED


class UserConnectionException(BookingException):
    detail = "Пользователь с указанными данными не найден"
    status_code = status.HTTP_401_UNAUTHORIZED


class AdminRoleException(BookingException):
    detail = "У вас недостаточно прав"
    status_code = status.HTTP_406_NOT_ACCEPTABLE


class UserExistsException(BookingException):
    detail = "Пользователь с указанной почтой уже зарегестрирован"
    status_code = status.HTTP_400_BAD_REQUEST


class RoomsConflictException(BookingException):
    detail = "Свободные комнаты отсутсвуют"
    status_code = status.HTTP_409_CONFLICT


class HotelNotFoundException(BookingException):
    detail = "Отель с указанным id не найден"
    status_code = status.HTTP_404_NOT_FOUND


class IncorrectEmailOrPasswordException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверная почта или пароль"