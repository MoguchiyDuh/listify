import json
import os, sys

import pytest, pytest_asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

sys.path.append(os.path.join(os.path.dirname(__file__), "../app"))
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.core.config import TEST_DB_URL, ASYNC_TEST_DB_URL
    from app.db.connection import Base
    from app.db.models import *
else:
    from core.config import TEST_DB_URL, ASYNC_TEST_DB_URL
    from db.connection import Base
    from db.models import *


@pytest.fixture(scope="session")
def test_engine():
    engine = create_engine(TEST_DB_URL)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="session")
def session(test_engine):
    SessionLocal = sessionmaker(bind=test_engine)
    s = SessionLocal()
    yield s
    s.close()


@pytest_asyncio.fixture(scope="session")
async def async_test_engine():
    engine = create_async_engine(ASYNC_TEST_DB_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="session")
async def async_session(async_test_engine):
    async_session = sessionmaker(bind=async_test_engine, class_=AsyncSession)
    async with async_session() as session:
        yield session


@pytest.fixture
def load_mock() -> dict:
    def _load(mock_name) -> dict:
        mocks_path = os.path.join(os.path.dirname(__file__), "mock_data")
        with open(
            os.path.join(mocks_path, f"{mock_name}.json"), "r", encoding="utf-8"
        ) as file:
            return json.load(file)

    return _load
