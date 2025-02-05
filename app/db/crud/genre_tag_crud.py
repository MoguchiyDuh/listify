from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import logger
from db.models import Genre, Tag


async def add_if_genre_not_exists(genre_name: str, db: AsyncSession) -> Genre:
    """Adds a new genre to the database if it does not already exist.

    Args:
        genre_name (str): The name of the genre to add.
        db (AsyncSession): A SQLAlchemy async session object.

    Returns:
        Genre: The new or existing genre.
    """
    query = select(Genre).filter(Genre.name == genre_name)
    result = await db.execute(query)
    genre = result.scalars().first()
    if genre is None:
        genre = Genre(name=genre_name)
        db.add(genre)
        await db.commit()
        logger.info(f"Genre {genre.id} {genre.name} added to database")
    return genre


async def add_if_tag_not_exists(tag_name: str, db: AsyncSession) -> Tag:
    """Adds a new tag to the database if it does not already exist.

    Args:
        tag_name (str): The name of the tag to add.
        db (AsyncSession): A SQLAlchemy async session object.

    Returns:
        Tag: The new or existing tag.
    """
    query = select(Tag).filter(Tag.name == tag_name)
    result = await db.execute(query)
    tag = result.scalars().first()
    if tag is None:
        tag = Tag(name=tag_name)
        db.add(tag)
        await db.commit()
        logger.info(f"Tag {tag.id} {tag.name} added to database")
    return tag
