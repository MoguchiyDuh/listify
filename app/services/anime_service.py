from datetime import date
from typing import Optional
import aiohttp

from . import logger
from db.models import AgeRating
from schemas.content_schemas import AnimeSchema

age_restriction_map = {
    "G - All Ages": AgeRating.G,
    "PG - Children": AgeRating.PG,
    "PG-13 - Teens 13 or older": AgeRating.PG13,
    "R - 17+ (violence & profanity)": AgeRating.R,
    "R+ - Mild Nudity": AgeRating.R,
    "Rx - Hentai": AgeRating.NC17,
}


async def fetch_anime(title: str, year: Optional[int] = None) -> AnimeSchema | dict:
    """
    Fetches anime details using the Jikan API and returns an `AnimeSchema` object.

    Args:
        title (str): The title of the anime.

    Returns:
        AnimeSchema|dict: An `AnimeSchema` object if the anime is found,
        otherwise a dictionary with an error message.
    """
    jikan_url = f"https://api.jikan.moe/v4/anime?q={title}&limit=5&unapproved=true"
    if year is not None:
        jikan_url += f"&start_date={year}-01-01&end_date={year+1}-01-01"
    async with aiohttp.ClientSession() as session:
        async with session.get(jikan_url) as response:
            if response.status == 200:
                data = await response.json()
            else:
                return {"msg": f"HTTP {response.status}"}

    item = data["data"][0]
    logger.debug(item)

    anime = AnimeSchema(
        title=item["title"],
        translated_title=item.get("title_english", title),
        description=item["synopsis"],
        score=item["score"],
        popularity=item["popularity"],
        image_url=item["images"]["jpg"]["large_image_url"],
        age_rating=age_restriction_map[item["rating"]],
        studios=[studio["name"] for studio in item.get("studios", [])],
        release_date=date.fromisoformat(item["aired"]["from"].split("T")[0]),
        end_date=date.fromisoformat(item["aired"]["to"].split("T")[0]),
        is_ongoing=item["airing"],
        episodes=item["episodes"],
        genres=[genre["name"] for genre in item["genres"]],
        tags=[theme["name"] for theme in item["themes"]],
    )
    return anime
