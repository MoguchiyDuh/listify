import pytest
from unittest.mock import patch, AsyncMock

from services import fetch_movie, fetch_series
from schemas import MovieSchema, SeriesSchema

MOVIE_TITLE = "Terminator"


@pytest.mark.asyncio
@patch("aiohttp.ClientSession.get")
async def test_fetch_movie(mock_get, load_mock):
    search_mock_response = AsyncMock()
    search_mock_response.status = 200
    search_mock_response.json.return_value = load_mock("movie_search.json")

    info_mock_response = AsyncMock()
    info_mock_response.status = 200
    info_mock_response.json.return_value = load_mock("movie_info.json")

    mock_get.return_value.__aenter__.side_effect = [
        search_mock_response,
        info_mock_response,
    ]

    movie = await fetch_movie(MOVIE_TITLE)
    assert isinstance(movie, MovieSchema)


@pytest.mark.asyncio
@patch("aiohttp.ClientSession.get")
async def test_fetch_movie_http_error(mock_get):
    search_mock_response = AsyncMock()
    search_mock_response.status = 503
    search_mock_response.json.return_value = None

    mock_get.return_value.__aenter__.side_effect = [search_mock_response]

    movie = await fetch_movie(MOVIE_TITLE)
    assert isinstance(movie, dict)


SERIES_TITLE = "Squid Game"


@pytest.mark.asyncio
@patch("aiohttp.ClientSession.get")
async def test_fetch_series(mock_get, load_mock):
    search_mock_response = AsyncMock()
    search_mock_response.status = 200
    search_mock_response.json.return_value = load_mock("series_search.json")

    info_mock_response = AsyncMock()
    info_mock_response.status = 200
    info_mock_response.json.return_value = load_mock("series_info.json")

    mock_get.return_value.__aenter__.side_effect = [
        search_mock_response,
        info_mock_response,
    ]

    series = await fetch_series(SERIES_TITLE)

    assert isinstance(series, SeriesSchema)


@pytest.mark.asyncio
@patch("aiohttp.ClientSession.get")
async def test_fetch_series_http_error(mock_get):
    search_mock_response = AsyncMock()
    search_mock_response.status = 503
    search_mock_response.json.return_value = None

    mock_get.return_value.__aenter__.side_effect = [search_mock_response]

    series = await fetch_movie(SERIES_TITLE)
    assert isinstance(series, dict)
