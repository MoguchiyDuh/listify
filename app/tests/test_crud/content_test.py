import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
import pytest

from db.models import *
from schemas import *
from db.crud.content_crud import add_content, get_content, get_content_by_type


# @pytest.mark.asyncio
# async def test_create_anime(async_db_session: AsyncSession, load_mock):
#     anime_schema = AnimeSchema.model_validate(
#         load_mock("anime_db.json"), from_attributes=True
#     )
#     print(anime_schema)
# content = await add_content(async_db_session, anime_schema)
# print(content)
# assert content
