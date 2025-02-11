from datetime import date
from typing import Optional, Union
import aiohttp

from . import logger
from core.config import RAWG_API_KEY
from schemas.content_schemas import GameSchema
from db.models import AgeRating, Platforms

platforms_map = {
    "PC": Platforms.PC,
    "PlayStation 3": Platforms.PS3,
    "PlayStation 4": Platforms.PS4,
    "PlayStation 5": Platforms.PS5,
    "Xbox 360": Platforms.XBOX_360,
    "Xbox One": Platforms.XBOX_ONE,
    "Xbox Series S/X": Platforms.XBOX_SERIES_X,
    "Nintendo Switch": Platforms.NINTENDO_SWITCH,
    "iOS": Platforms.IOS,
    "Android": Platforms.ANDROID,
}
age_restriction_map = {
    "Everyone": AgeRating.G,
    "Everyone 10+": AgeRating.PG,
    "Teen": AgeRating.PG13,
    "Mature": AgeRating.R,
    "Adults Only": AgeRating.NC17,
}


async def fetch_game(
    title: str, year: Optional[int] = None
) -> Union[GameSchema, dict[str, str]]:
    """
    Searches for a game by title using the RAWG API.

    Args:
        title (str): The title of the game.

    Returns:
        Union[`GameSchema`,dict[str,str]]: A `GameSchema` object containing game details
        if a match is found, otherwise a dictionary with an error message: `{"msg": ...}`.
    """
    rawg_search_url = (
        f"https://api.rawg.io/api/games?key={RAWG_API_KEY}&page_size=5&search={title}"
    )
    if year is not None:
        rawg_search_url += f"&dates={year}-01-01,{year + 1}-01-01"

    async with aiohttp.ClientSession() as session:
        async with session.get(rawg_search_url) as response:
            if response.status == 200:
                data = await response.json()
            else:
                return {"msg": f"HTTP {response.status}"}

        game_id = data["results"][0]["id"]

        rawg_game_url = f"https://api.rawg.io/api/games/{game_id}?key={RAWG_API_KEY}"

        async with session.get(rawg_game_url) as response:
            if response.status == 200:
                item = await response.json()
                logger.debug(item)
            else:
                return {"msg": f"HTTP {response.status}"}

    game = GameSchema(
        title=item["name"],
        description=item["description_raw"],
        score=(
            item["metacritic"]
            / 10  # the metacritic field is 0-100, so we need to divide by 10 to get 0.0-10.0
            if item["metacritic"] is not None
            else (
                item["rating"] * 2 if item["rating"] is not None else None
            )  # the rating field is 0.0-5.0, so we need to multiply by 2 to get 0.0-10.0
        ),
        popularity=item["popularity"],
        image_url=item["background_image"],
        age_rating=(
            age_restriction_map[item["esrb_rating"]["name"]]
            if item["esrb_rating"]
            else None
        ),
        studios=[dev["name"] for dev in item["developers"]],
        release_date=(
            date.fromisoformat(item["released"]) if item["released"] else None
        ),
        available_platforms=[
            platforms_map.get(platform["platform"]["name"], None)
            for platform in item.get("platforms", [])
            if platforms_map.get(platform["platform"]["name"], None) is not None
        ],
        playtime=item["playtime"],
        stores=[store["store"]["name"] for store in item["stores"]],
        genres=[genre["name"] for genre in item["genres"]],
        tags=[tag["name"] for tag in item["tags"] if tag["language"] == "eng"],
    )

    return game
