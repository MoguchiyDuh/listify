from typing import Union
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import logger
from schemas.content_schemas import AnimeSchema
from db.models import Anime
from db.crud.genre_tag_crud import add_if_genre_not_exists, add_if_tag_not_exists


async def get_anime(title: Union[str, int], db: AsyncSession) -> Union[Anime, None]:
    """Get anime by title

    Args:
        title (Union[str, int]): Title or id of anime to search for.
        db (AsyncSession): Database session.

    Returns:
        Union[Anime, None]: Anime if found, otherwise None.
    """
    if isinstance(title, int):
        query = select(Anime).filter(Anime.id == title)
    else:
        query = select(Anime).filter(Anime.title == title)
    result = await db.execute(query)
    anime = result.scalars().first()
    return anime


async def add_anime(anime_schema: AnimeSchema, db: AsyncSession) -> Anime:
    """Add anime to database.

    Args:
        anime_schema (AnimeSchema): Anime schema.
        db (AsyncSession): Database session.

    Returns:
        Anime: Newly created anime.
    """
    anime_dict = anime_schema.model_dump(exclude_none=True, exclude_unset=True)
    anime_dict["genres"] = [
        await add_if_genre_not_exists(genre, db) for genre in anime_schema.genres
    ]
    anime_dict["tags"] = [
        await add_if_tag_not_exists(tag, db) for tag in anime_schema.tags
    ]

    anime = Anime(**anime_dict)

    db.add(anime)
    await db.commit()
    logger.info(f"Anime {anime.id} {anime.title} added to database")
    return anime
