from datetime import date
import os, sys

import pytest
from unittest.mock import patch, AsyncMock

sys.path.append(os.path.join(os.path.dirname(__file__), "../app"))
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.models import *
    from app.services.anime_service import fetch_anime
    from app.schemas.content_schemas import AnimeSchema
else:
    from db.models import *
    from services.anime_service import fetch_anime
    from schemas.content_schemas import AnimeSchema


@pytest.mark.asyncio
@patch("aiohttp.ClientSession.get")
async def test_get_anime(mock_get, load_mock):
    TITLE = "Jujutsu Kaisen"
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json.return_value = load_mock("anime_info")

    mock_get.return_value.__aenter__.return_value = mock_response
    anime = await fetch_anime(TITLE)
    assert isinstance(anime, AnimeSchema)


@pytest.mark.asyncio
@patch("aiohttp.ClientSession.get")
async def test_get_anime_no_results(mock_get, load_mock):
    TITLE = "Some random text to lower the UWratio score"
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json.return_value = load_mock("anime_info")

    mock_get.return_value.__aenter__.return_value = mock_response
    anime = await fetch_anime(TITLE)
    assert isinstance(anime, dict) and "Anime not found" in anime["msg"]


@pytest.mark.asyncio
@patch("aiohttp.ClientSession.get")
async def test_get_anime_http_error(mock_get):
    TITLE = "Jujutsu Kaisen"
    mock_response = AsyncMock()
    mock_response.status = 404
    mock_response.json.return_value = None

    mock_get.return_value.__aenter__.return_value = mock_response
    anime = await fetch_anime(TITLE)
    assert isinstance(anime, dict) and "404" in anime["msg"]
