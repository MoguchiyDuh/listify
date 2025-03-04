import pytest
from unittest.mock import patch, AsyncMock

from schemas import AnimeSchema
from services import fetch_anime


@pytest.mark.asyncio
@patch("aiohttp.ClientSession.get")
async def test_fetch_anime(mock_get, load_mock):
    TITLE = "Jujutsu Kaisen"
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json.return_value = load_mock("anime_info.json")

    mock_get.return_value.__aenter__.return_value = mock_response
    anime = await fetch_anime(TITLE)
    assert isinstance(anime, AnimeSchema)
    print(anime.model_dump())


@pytest.mark.asyncio
@patch("aiohttp.ClientSession.get")
async def test_get_anime_http_error(mock_get):
    TITLE = "Jujutsu Kaisen"
    mock_response = AsyncMock()
    mock_response.status = 503
    mock_response.json.return_value = None

    mock_get.return_value.__aenter__.return_value = mock_response
    anime = await fetch_anime(TITLE)
    assert isinstance(anime, dict)
