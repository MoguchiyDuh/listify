import asyncio
import json
import os, sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import pytest
import pytest_asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from core.config import TEST_DB_URL, ASYNC_TEST_DB_URL
from db.connection import Base


# Fixture for event loop(p.s. i know that it's deprecated, but my tests don't work without it whatsoever)
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# Sync engine and session
sync_engine = create_engine(TEST_DB_URL)
SyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)

# Async engine and session
async_engine = create_async_engine(ASYNC_TEST_DB_URL)
AsyncSessionLocal = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)


@pytest.fixture
def sync_db_session():
    # Create all tables for sync engine
    Base.metadata.create_all(bind=sync_engine)

    # Create a new sync session
    session = SyncSessionLocal()
    try:
        yield session
    finally:
        # Rollback and close the session
        session.rollback()
        session.close()

    # Drop all tables after the test
    Base.metadata.drop_all(bind=sync_engine)


# Fixture for async session
@pytest_asyncio.fixture
async def async_db_session():
    # Create all tables for async engine
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Create a new async session
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            # Rollback and close the session
            await session.rollback()
            await session.close()

    # Drop all tables after the test
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
def load_mock() -> dict:
    def _load(mock_name: str) -> dict:
        mocks_path = os.path.join(os.path.dirname(__file__), "mock_content")

        # Search recursively for the file in all subdirectories
        for root, _, files in os.walk(mocks_path):
            if mock_name in files:
                with open(os.path.join(root, mock_name), "r", encoding="utf-8") as f:
                    if mock_name.endswith(".json"):
                        return json.load(f)
                    else:
                        return f.read()

        raise FileNotFoundError(
            f"{mock_name} not found in {mocks_path} or its subdirectories"
        )

    return _load
