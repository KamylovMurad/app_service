import pytest
from app.users.dao import UsersDAO
from app.users.schemas import SchemaUserV2


@pytest.mark.parametrize("user_id, email, exists",[
    (1, "test@test.com", True),
    (2, "artem@example.com", True),
    (8, "test@test.com", False),

])
async def test_get_current_user(user_id, email, exists):
    user = await UsersDAO.get_one_or_none(id=user_id)
    if exists:
        assert user
        assert user.id == user_id
        assert user.email == email
    elif not exists:
        assert not user
