from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import ASYNC_DB_URL

Base = declarative_base()
engine = create_async_engine(ASYNC_DB_URL)

# sessionmaker(class_=AsyncSession) used in both synchronous and asynchronous operations
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session():
    async with async_session() as session:
        yield session
