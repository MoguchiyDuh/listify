import os, sys

import pytest
from unittest.mock import patch, AsyncMock

sys.path.append(os.path.join(os.path.dirname(__file__), "../app"))
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.models import *
    from app.schemas.content_schemas import GameSchema
    from app.services.game_service import fetch_game
else:
    from db.models import *
    from schemas.content_schemas import GameSchema
    from services.game_service import fetch_game


@pytest.mark.asyncio
@patch("aiohttp.ClientSession.get")
async def test_fetch_game(mock_get, load_mock):
    TITLE = "The Witcher 3"
    search_mock_response = AsyncMock()
    search_mock_response.status = 200
    search_mock_response.json.return_value = load_mock("game_search")

    info_mock_response = AsyncMock()
    info_mock_response.status = 200
    info_mock_response.json.return_value = load_mock("game_info")

    mock_get.return_value.__aenter__.side_effect = [
        search_mock_response,
        info_mock_response,
    ]

    game = await fetch_game(TITLE)

    assert isinstance(game, GameSchema)


@pytest.mark.asyncio
@patch("aiohttp.ClientSession.get")
async def test_fetch_game_http_error(mock_get):
    TITLE = "The Witcher 3"
    search_mock_response = AsyncMock()
    search_mock_response.status = 404
    search_mock_response.json.return_value = None

    mock_get.return_value.__aenter__.side_effect = [search_mock_response]

    game = await fetch_game(TITLE)
    assert isinstance(game, dict) and "404" in game["msg"]


@pytest.mark.asyncio
@patch("aiohttp.ClientSession.get")
async def test_fetch_game_no_results(mock_get, load_mock):
    TITLE = "Soem random text to lower the UWratio score"
    search_mock_response = AsyncMock()
    search_mock_response.status = 200
    search_mock_response.json.return_value = load_mock("game_search")

    mock_get.return_value.__aenter__.side_effect = [search_mock_response]

    game = await fetch_game(TITLE)
    assert isinstance(game, dict) and "Game not found" in game["msg"]
