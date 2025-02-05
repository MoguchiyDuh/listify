from datetime import date
from typing import Optional, Union
import aiohttp
from thefuzz import process, fuzz

from . import logger
from db.models import AgeRestriction
from schemas.content_schemas import AnimeSchema

age_restriction_map = {
    "G - All Ages": AgeRestriction.G,
    "PG - Children": AgeRestriction.PG,
    "PG-13 - Teens 13 or older": AgeRestriction.PG13,
    "R - 17+ (violence & profanity)": AgeRestriction.R,
    "R+ - Mild Nudity": AgeRestriction.R,
    "Rx - Hentai": AgeRestriction.NC17,
}


async def fetch_anime(
    title: str, year: Optional[int] = None
) -> Union[AnimeSchema, dict]:
    """
    Fetches anime details using the Jikan API and returns an `AnimeSchema` object.

    Args:
        title (str): The title of the anime.

    Returns:
        Union[AnimeSchema, dict]: An `AnimeSchema` object if the anime is found,
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

    # anime_list = {item["title"]: item for item in data["data"]}
    # anime_list.update({item["title_english"]: item for item in data["data"]})
    # match = process.extractOne(
    #     title, list(anime_list.keys()), scorer=fuzz., score_cutoff=90
    # )
    # match =
    # if match is None:
    #     return {"msg": "Anime not found"}
    # else:
    # item = anime_list[]
    item = data["data"][0]
    logger.debug(item)

    anime = AnimeSchema(
        title=item["title"],
        translated_title=item.get("title_english", title),
        description=item["synopsis"],
        rating=item["score"],
        popularity=item["popularity"],
        image_url=item["images"]["jpg"]["large_image_url"],
        age_restriction=age_restriction_map[item["rating"]],
        studios=[studio["name"] for studio in item.get("studios", [])],
        release_date=date.fromisoformat(item["aired"]["from"].split("T")[0]),
        is_ongoing=item["airing"],
        episodes=item["episodes"],
        genres=[genre["name"] for genre in item.get("genres", [])],
        tags=[tag["name"] for tag in item.get("tags", [])],
    )
    return anime
