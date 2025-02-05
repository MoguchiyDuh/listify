from typing import Literal, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession


from db.connection import get_session
from db.crud.find_content import find_content, find_all_content
from db.crud.anime_crud import add_anime, get_anime
from db.crud.movie_crud import add_movie, get_movie
from db.crud.series_crud import add_series, get_series
from db.crud.game_crud import add_game, get_game
from services.anime_service import fetch_anime
from services.movie_series_service import fetch_movie, fetch_series
from services.game_service import fetch_game

router = APIRouter()


@router.get("/anime")
async def add_anime_endpoint(
    title: str, year: Optional[int] = None, db: AsyncSession = Depends(get_session)
):
    anime = await fetch_anime(title, year)
    if isinstance(anime, dict):
        return anime
    if await get_anime(anime.title, db) is None:
        await add_anime(anime, db)
        return anime
    else:
        return {"msg": "Anime already in database"}


@router.get("/movie")
async def add_movie_endpoint(
    title: str, year: Optional[int] = None, db: AsyncSession = Depends(get_session)
):
    movie = await fetch_movie(title, year)
    if isinstance(movie, dict):
        return movie
    if await get_movie(movie.title, db) is None:
        await add_movie(movie, db)
        return movie
    else:
        return {"msg": "Movie already in database"}


@router.get("/series")
async def add_series_endpoint(
    title: str, year: Optional[int] = None, db: AsyncSession = Depends(get_session)
):
    series = await fetch_series(title, year)
    if isinstance(series, dict):
        return series
    if await get_series(series.title, db) is None:
        await add_series(series, db)
        return series
    else:
        return {"msg": "Series already in database"}


@router.get("/game")
async def add_game_endpoint(
    title: str, year: Optional[int] = None, db: AsyncSession = Depends(get_session)
):
    game = await fetch_game(title, year)
    if isinstance(game, dict):
        return game

    if await get_game(game.title, db) is None:
        await add_game(game, db)
        return game
    else:
        return {"msg": "Game already in database"}


@router.get("/search/{content_type}")
async def all_content_search_endpoint(
    content_type: Literal["anime", "game", "movie", "series"],
    page: Optional[int] = 1,
    page_size: Optional[int] = 10,
    sort: Literal["popularity", "rating", "release_date", "title"] = "popularity",
    sort_order: Literal["desc", "asc"] = "desc",
    db: AsyncSession = Depends(get_session),
):
    content = await find_all_content(
        db=db,
        content_type=content_type,
        page=page,
        page_size=page_size,
        sort=sort,
        sort_order=sort_order,
    )
    return content


@router.get("/search/{content_type}/{content_id}")
async def content_search_endpoint(
    content_type: Literal["anime", "game", "movie", "series"],
    content_id: int,
    db: AsyncSession = Depends(get_session),
):
    content = await find_content(
        db=db, content_type=content_type, content_id=content_id
    )
    return content
