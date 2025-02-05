from db.models import Anime, Game, Movie, Series
from typing import Literal, Union
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def find_content(
    db: AsyncSession,
    content_type: Literal["anime", "game", "movie", "series"],
    content_id: int,
) -> Union[Anime, Game, Movie, Series, None]:
    """Find a content by its id and type.

    Args:
        db (AsyncSession): The database session.
        content_type (Literal["anime", "game", "movie", "series"]): The type of the content to find.
        content_id (int): The id of the content to find.

    Returns:
        Union[Anime, Game, Movie, Series, None]: The found content or None if not found.
    """
    match content_type:
        case "anime":
            content_model = Anime
        case "game":
            content_model = Game
        case "movie":
            content_model = Movie
        case "series":
            content_model = Series
        case _:
            return None

    result = await db.execute(
        select(content_model).filter(content_model.id == content_id)
    )
    content = result.scalars().first()
    return content


async def find_all_content(
    db: AsyncSession,
    content_type: Literal["anime", "game", "movie", "series"],
    page: int = 1,
    page_size: int = 10,
    sort: Literal["popularity", "rating", "release_date", "title"] = "popularity",
    sort_order: Literal["desc", "asc"] = "desc",
):
    match content_type:
        case "anime":
            content_model = Anime
        case "game":
            content_model = Game
        case "movie":
            content_model = Movie
        case "series":
            content_model = Series
        case _:
            return []

    query = select(content_model).order_by(getattr(content_model, sort))
    if sort_order == "desc":
        query = query.order_by(getattr(content_model, sort).desc())

    result = await db.execute(query)
    contents = result.scalars().all()
    return contents
