from typing import Union
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import logger
from schemas.content_schemas import GameSchema
from db.models import Game
from db.crud.genre_tag_crud import add_if_genre_not_exists, add_if_tag_not_exists


async def get_game(title: Union[str, int], db: AsyncSession) -> Union[Game, None]:
    """Get game by title

    Args:
        title (Union[str, int]): Title or id of game to search for.
        db (AsyncSession): Database session.

    Returns:
        Union[Game, None]: Game if found, otherwise None.
    """
    if isinstance(title, int):
        query = select(Game).filter(Game.id == title)
    else:
        query = select(Game).filter(Game.title == title)
    result = await db.execute(query)
    game = result.scalars().first()
    return game


async def add_game(game_schema: GameSchema, db: AsyncSession) -> Game:
    """Add game to database.

    Args:
        game_schema (GameSchema): Game schema.
        db (AsyncSession): Database session.

    Returns:
        Game: Newly created game.
    """
    game_dict = game_schema.model_dump(exclude_none=True, exclude_unset=True)
    game_dict["genres"] = [
        await add_if_genre_not_exists(genre, db) for genre in game_schema.genres
    ]
    game_dict["tags"] = [
        await add_if_tag_not_exists(tag, db) for tag in game_schema.tags
    ]

    game = Game(**game_dict)

    db.add(game)
    await db.commit()
    logger.info(f"Game {game.id} {game.title} added to database")
    return game
