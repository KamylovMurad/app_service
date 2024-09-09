import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("email, password, status_code", [
    ("kotopes@mail.ru", "1234", 201),
    ("kotopes@mail.ru", "1234", 400),
    ("1234", "1234", 422),
])
async def test_register_user(ac: AsyncClient, email, password, status_code):
    response = await ac.post(url="/auth/register", json={
        "email": email,
        "password": password,
    })
    assert response.status_code == status_code


@pytest.mark.parametrize("email, password, status_code", [
    ("test@test.com", "test", 202),
    ("kot@ir.com", "1234", 401),
    ("1234", "1234", 422),
])
async def test_login_user(ac: AsyncClient,  email, password, status_code):
    response = await ac.post(url="/auth/login", json={
        "email": email,
        "password": password,
    })

    assert response.status_code == status_code
