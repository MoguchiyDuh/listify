import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
import pytest

from db.models import *
from schemas import *
from services.user_service import (
    get_current_user,
    get_user,
    authenticate_user,
    update_user_profile,
    delete_user_profile,
    register_user,
)


@pytest_asyncio.fixture
async def test_user(async_db_session: AsyncSession):
    user_schema = UserCreate(
        username="John Doe", email="john.doe@example.com", password="123456"
    )
    user = await register_user(async_db_session, user_schema)
    async_db_session.add(user)
    await async_db_session.commit()
    yield user


@pytest.mark.asyncio
async def test_get_user(async_db_session: AsyncSession, test_user: User):
    fetched_user = await get_user(async_db_session, test_user.id)
    assert fetched_user == test_user


@pytest.mark.asyncio
async def test_authenticate_user(async_db_session: AsyncSession, test_user: User):
    token = await authenticate_user(async_db_session, test_user.email, "123456")
    print("Test token:", token)
    assert isinstance(token, str)


@pytest.mark.asyncio
async def test_get_current_user(async_db_session: AsyncSession, test_user: User):
    token = await authenticate_user(async_db_session, test_user.email, "123456")
    current_user = await get_current_user(async_db_session, token)
    assert current_user == test_user


@pytest.mark.asyncio
async def test_update_user(async_db_session: AsyncSession, test_user: User):
    update_schema = UserUpdate(
        username="John Johnson", email="john.johnson@example.com", password="654321"
    )
    updated_user = await update_user_profile(async_db_session, test_user, update_schema)
    assert updated_user


@pytest.mark.asyncio
async def test_delete_user(async_db_session: AsyncSession, test_user: User):
    await delete_user_profile(async_db_session, test_user, "123456")
    assert await get_user(async_db_session, test_user.id) is None
