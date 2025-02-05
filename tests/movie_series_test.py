import os, sys
import json
import pytest
from unittest.mock import patch, AsyncMock

sys.path.append(os.path.join(os.path.dirname(__file__), "../app"))
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.models import *
    from app.schemas.content_schemas import MovieSchema, SeriesSchema
    from app.services.movie_series_service import fetch_movie, fetch_series
else:
    from db.models import *
    from schemas.content_schemas import MovieSchema, SeriesSchema
    from services.movie_series_service import fetch_movie, fetch_series


@pytest.mark.asyncio
@patch("aiohttp.ClientSession.get")
async def test_fetch_movie(mock_get, load_mock):
    TITLE = "Terminator"
    search_mock_response = AsyncMock()
    search_mock_response.status = 200
    search_mock_response.json.return_value = load_mock("movie_search")

    info_mock_response = AsyncMock()
    info_mock_response.status = 200
    info_mock_response.json.return_value = load_mock("movie_info")

    mock_get.return_value.__aenter__.side_effect = [
        search_mock_response,
        info_mock_response,
    ]

    movie = await fetch_movie(TITLE)
    assert isinstance(movie, MovieSchema)


@pytest.mark.asyncio
@patch("aiohttp.ClientSession.get")
async def test_fetch_movie_http_error(mock_get):
    TITLE = "Terminator"
    search_mock_response = AsyncMock()
    search_mock_response.status = 404
    search_mock_response.json.return_value = None

    mock_get.return_value.__aenter__.side_effect = [search_mock_response]

    movie = await fetch_movie(TITLE)
    assert isinstance(movie, dict) and "404" in movie["msg"]


@pytest.mark.asyncio
@patch("aiohttp.ClientSession.get")
async def test_fetch_movie_no_results(mock_get, load_mock):
    TITLE = "Some random text to lower the fuzz.UWratio"
    search_mock_response = AsyncMock()
    search_mock_response.status = 200
    search_mock_response.json.return_value = load_mock("movie_search")

    mock_get.return_value.__aenter__.side_effect = [search_mock_response]

    movie = await fetch_movie(TITLE)
    assert isinstance(movie, dict) and "Movie not found" in movie["msg"]


@pytest.mark.asyncio
@patch("aiohttp.ClientSession.get")
async def test_fetch_series(mock_get, load_mock):
    TITLE = "Squid Game"
    search_mock_response = AsyncMock()
    search_mock_response.status = 200
    search_mock_response.json.return_value = load_mock("series_search")

    info_mock_response = AsyncMock()
    info_mock_response.status = 200
    info_mock_response.json.return_value = load_mock("series_info")

    mock_get.return_value.__aenter__.side_effect = [
        search_mock_response,
        info_mock_response,
    ]

    series = await fetch_series(TITLE)

    assert isinstance(series, SeriesSchema)


@pytest.mark.asyncio
@patch("aiohttp.ClientSession.get")
async def test_fetch_series_http_error(mock_get):
    TITLE = "Squid Game"
    search_mock_response = AsyncMock()
    search_mock_response.status = 404
    search_mock_response.json.return_value = None

    mock_get.return_value.__aenter__.side_effect = [search_mock_response]

    series = await fetch_movie(TITLE)
    assert isinstance(series, dict) and "404" in series["msg"]


@pytest.mark.asyncio
@patch("aiohttp.ClientSession.get")
async def test_fetch_series_no_results(mock_get, load_mock):
    TITLE = "Some random text to lower the fuzz.UWratio"
    search_mock_response = AsyncMock()
    search_mock_response.status = 200
    search_mock_response.json.return_value = load_mock("series_search")

    mock_get.return_value.__aenter__.side_effect = [search_mock_response]

    movie = await fetch_series(TITLE)
    assert isinstance(movie, dict) and "Series not found" in movie["msg"]
