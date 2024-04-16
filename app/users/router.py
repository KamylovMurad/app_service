from fastapi import APIRouter, status, Response, Depends
from fastapi.responses import JSONResponse

from app.exceptions import UserConnectionException, UserExistsException
from app.users.auth import get_password_hash, authenticate, create_access_token
from app.users.dao import UsersDAO
from app.users.dependencies import get_token, get_user, get_role
from app.users.models import Users
from app.users.schemas import SchemaUser, SchemaAboutUser

router = APIRouter(
    prefix="/auth",
    tags=["Auth & Authorization"]
)


@router.post("/register")
async def register_user(user_data: SchemaUser):
    existing_user = await UsersDAO.get_one_or_none(email=user_data.email)
    if existing_user:
        raise UserExistsException
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(email=user_data.email, password=hashed_password, name=user_data.name)
    return JSONResponse(content={"content": "Пользователь успешно создан"}, status_code=status.HTTP_201_CREATED)


@router.post("/register_admin")
async def register_admin_user(user_data: SchemaUser):
    existing_user = await UsersDAO.get_one_or_none(email=user_data.email)
    if existing_user:
        raise UserExistsException
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(email=user_data.email, password=hashed_password, name=user_data.name, role='admin')
    return JSONResponse(content={"content": "Админ пользователь успешно создан"}, status_code=status.HTTP_201_CREATED)


@router.post("/login", status_code=status.HTTP_202_ACCEPTED)
async def login_user(response: Response, user_data: SchemaUser):
    user = await authenticate(user_data.email, user_data.password)
    if not user:
        raise UserConnectionException
    access_token = create_access_token({'sub': str(user.id), 'name': str(user.name)})
    response.set_cookie("booking_access_token", value=access_token, httponly=True)
    return {"access_token": access_token}


@router.post("/logout")
async def logout_user(response: Response, a=Depends(get_token)):
    response.delete_cookie(key="booking_access_token")
    return {"detail": "Вы успешно вышли"}


@router.get("/me")
async def read_my_user(user: Users = Depends(get_user)) -> SchemaAboutUser:
    return SchemaAboutUser(email=user.email, name=str(user.name))


@router.get("/all_users")
async def read_all_users(users: Users = Depends(get_role)):
    return users
