import pytest
from unittest.mock import patch, AsyncMock

from services import get_steam_online, fetch_game
from schemas import GameSchema

TITLE = "The Witcher 3"


@pytest.mark.asyncio
@patch("aiohttp.ClientSession.get")
async def test_get_steam_online(mock_get, load_mock):
    steam_id_search_response = AsyncMock()
    steam_id_search_response.status = 200
    steam_id_search_response.json.return_value = load_mock("steam_id_search.json")

    steam_online_response = AsyncMock()
    steam_online_response.status = 200
    steam_online_response.text.return_value = load_mock("steam_online.html")

    mock_get.return_value.__aenter__.side_effect = [
        steam_id_search_response,
        steam_online_response,
    ]
    steam_online = await get_steam_online(TITLE)
    assert steam_online == 21497


@pytest.mark.asyncio
@patch("aiohttp.ClientSession.get")
async def test_steam_id_http_error(mock_get):
    steam_id_search_response = AsyncMock()
    steam_id_search_response.status = 503
    steam_id_search_response.json.return_value = None

    mock_get.return_value.__aenter__.side_effect = [steam_id_search_response]

    game_online = await get_steam_online(TITLE)
    assert game_online is None


@pytest.mark.asyncio
@patch("aiohttp.ClientSession.get")
async def test_steam_online_http_error(mock_get, load_mock):
    steam_id_search_response = AsyncMock()
    steam_id_search_response.status = 200
    steam_id_search_response.json.return_value = load_mock("steam_id_search.json")

    steam_online_response = AsyncMock()
    steam_online_response.status = 503
    steam_online_response.text.return_value = None

    mock_get.return_value.__aenter__.side_effect = [
        steam_id_search_response,
        steam_online_response,
    ]
    game_online = await get_steam_online(TITLE)
    assert game_online is None


@pytest.mark.asyncio
@patch("aiohttp.ClientSession.get")
async def test_steam_id_no_result(mock_get):
    steam_id_search_response = AsyncMock()
    steam_id_search_response.status = 200
    steam_id_search_response.json.return_value = []

    mock_get.return_value.__aenter__.side_effect = [steam_id_search_response]
    steam_online = await get_steam_online(TITLE)
    assert steam_online is None


@pytest.mark.asyncio
@patch("aiohttp.ClientSession.get")
async def test_fetch_game(mock_get, load_mock):
    responses = [
        ("game_search.json", 200),
        ("game_info.json", 200),
        ("steam_id_search.json", 200),
        ("steam_online.html", 200),
    ]

    mock_responses = []
    for file, status in responses:
        mock_response = AsyncMock()
        mock_response.status = status
        if file.endswith(".json"):
            mock_response.json.return_value = load_mock(file)
        else:
            mock_response.text.return_value = load_mock(file)

        mock_responses.append(mock_response)

    mock_get.return_value.__aenter__.side_effect = mock_responses

    game = await fetch_game(TITLE)
    assert isinstance(game, GameSchema)


@pytest.mark.asyncio
@patch("aiohttp.ClientSession.get")
async def test_fetch_game_no_result(mock_get):
    game_search_response = AsyncMock()
    game_search_response.status = 503
    game_search_response.json.return_value = []

    mock_get.return_value.__aenter__.side_effect = [game_search_response]
    game = await fetch_game(TITLE)
    assert isinstance(game, dict)
