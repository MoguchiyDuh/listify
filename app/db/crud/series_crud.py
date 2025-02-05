from typing import Union
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import logger
from schemas.content_schemas import SeriesSchema
from db.models import Series
from db.crud.genre_tag_crud import add_if_genre_not_exists


async def get_series(title: Union[str, int], db: AsyncSession) -> Union[Series, None]:
    """Get series by title

    Args:
        title (Union[str, int]): Title or id of series to search for.
        db (AsyncSession): Database session.

    Returns:
        Union[Series, None]: Series if found, otherwise None.
    """
    if isinstance(title, int):
        query = select(Series).filter(Series.id == title)
    else:
        query = select(Series).filter(Series.title == title)
    result = await db.execute(query)
    series = result.scalars().first()
    return series


async def add_series(series_schema: SeriesSchema, db: AsyncSession) -> Series:
    """Add series to database.

    Args:
        series_schema (SeriesSchema): Series schema.
        db (AsyncSession): Database session.

    Returns:
        Series: Newly created series.
    """
    series_dict = series_schema.model_dump(exclude_none=True, exclude_unset=True)
    series_dict["genres"] = [
        await add_if_genre_not_exists(genre, db) for genre in series_schema.genres
    ]

    series = Series(**series_dict)

    db.add(series)
    await db.commit()
    logger.info(f"Series {series.id} {series.title} added to database.")
    return series
