from datetime import datetime

from fastapi import Request, Depends
from jose import jwt, JWTError

from app.config import settings
from app.exceptions import (
    TokenMissingException,
    TokenTimeOverException,
    UserConnectionException,
    AdminRoleException,
    BookingException)
from app.users.dao import UsersDAO
from app.users.models import Users


async def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise TokenMissingException
    return token


async def get_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token=token, key=settings.SECRET_KEY, algorithms=settings.ALGORITHM)
    except JWTError:
        raise BookingException(detail="Неверный токен пользователя")
    expire: str = payload.get("exp")
    if not expire or int(expire) < datetime.utcnow().timestamp():
        raise TokenTimeOverException
    user_id: str = payload.get("sub")
    if not user_id:
        raise UserConnectionException
    user = await UsersDAO.get_current_user(id=int(user_id))
    if not user:
        raise UserConnectionException

    return user


async def get_role(user: Users = Depends(get_user)):
    if user.role != 'admin':
        raise AdminRoleException
    return await UsersDAO.get_all()
