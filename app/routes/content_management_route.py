from typing import Literal, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession


from db.connection import get_session
from services.anime_service import fetch_anime
from services.movie_series_service import fetch_movie, fetch_series
from services.game_service import fetch_game

router = APIRouter()


@router.get("/anime")
async def get_anime(title: str, year: Optional[int] = None):
    return await fetch_anime(title, year)


@router.get("/movie")
async def get_movie(title: str, year: Optional[int] = None):
    return await fetch_movie(title, year)


@router.get("/series")
async def get_series(title: str, year: Optional[int] = None):
    return await fetch_series(title, year)


@router.get("/game")
async def get_game(title: str, year: Optional[int] = None):
    return await fetch_game(title, year)
