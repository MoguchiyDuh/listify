from typing import Union
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import logger
from schemas.content_schemas import MovieSchema
from db.models import Movie
from db.crud.genre_tag_crud import add_if_genre_not_exists


async def get_movie(title: Union[str, int], db: AsyncSession) -> Union[Movie, None]:
    """Get movie by title

    Args:
        title (Union[str,int]): Title or id of movie to search for.
        db (AsyncSession): Database session.

    Returns:
        Union[Movie, None]: Movie if found, otherwise None.
    """
    if isinstance(title, int):
        query = select(Movie).filter(Movie.id == title)
    else:
        query = select(Movie).filter(Movie.title == title)
    result = await db.execute(query)
    movie = result.scalars().first()
    return movie


async def add_movie(movie_schema: MovieSchema, db: AsyncSession) -> Movie:
    """Add movie to database.

    Args:
        movie_schema (MovieSchema): Movie schema.
        db (AsyncSession): Database session.

    Returns:
        Movie: Newly created movie.
    """
    movie_dict = movie_schema.model_dump(exclude_none=True, exclude_unset=True)
    movie_dict["genres"] = [
        await add_if_genre_not_exists(genre, db) for genre in movie_schema.genres
    ]

    movie = Movie(**movie_dict)

    db.add(movie)
    await db.commit()
    logger.info(f"Movie {movie.id} {movie.title} added to database.")
    return movie
