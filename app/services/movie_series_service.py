from datetime import date
from typing import Optional, Union
import aiohttp

from . import logger
from core.config import TMDB_API_KEY
from schemas.content_schemas import MovieSchema, SeriesSchema
from db.models import AgeRating

age_restriction_map = {
    "NR": None,
    # US
    "G": AgeRating.G,
    "PG": AgeRating.PG,
    "PG-13": AgeRating.PG13,
    "R": AgeRating.R,
    "NC-17": AgeRating.NC17,
    # RU
    "0+": AgeRating.G,
    "6+": AgeRating.PG,
    "12+": AgeRating.PG13,
    "16+": AgeRating.R,
    "18+": AgeRating.NC17,
    # US TV
    "TV-Y": AgeRating.G,
    "TV-Y7": AgeRating.G,
    "TV-Y7-FV": AgeRating.G,
    "TV-G": AgeRating.G,
    "TV-PG": AgeRating.PG,
    "TV-14": AgeRating.PG13,
    "TV-MA": AgeRating.R,
}

TMDB_BASE_URL = f"https://api.themoviedb.org/3"
HEADERS = {"accept": "application/json", "Authorization": f"Bearer {TMDB_API_KEY}"}
TMDB_POSTER_URL = "https://image.tmdb.org/t/p/original"


async def fetch_movie(
    title: str, year: Optional[int] = None
) -> Union[MovieSchema, dict[str, str]]:
    """
    Searches for a movie by title (and optionally by year) using the TMDB API.

    Args:
        title (str): The title of the movie.
        year (int, optional): The release year of the movie.

    Returns:
        Union[MovieSchema, dict[str, str]]: A `MovieSchema` object containing movie details
        if a match is found, otherwise a dictionary with an error message: `{"msg": ...}`.
    """
    tmdb_search_url = (
        f"/search/movie?include_adult=true&language=en-US&page=1&query={title}"
    )
    if year is not None:
        tmdb_search_url += f"&year={year}"

    async with aiohttp.ClientSession() as session:
        async with session.get(
            TMDB_BASE_URL + tmdb_search_url, headers=HEADERS
        ) as response:
            if response.status == 200:
                data = await response.json()
            else:
                return {"msg": f"HTTP {response.status}"}

        movie_id = data["results"][0]["id"]

        tmdb_info_url = (
            f"/movie/{movie_id}?language=en-US&append_to_response=release_dates"
        )
        async with session.get(
            TMDB_BASE_URL + tmdb_info_url, headers=HEADERS
        ) as response:
            if response.status == 200:
                item = await response.json()
                logger.debug(item)
            else:
                return {"msg": f"HTTP {response.status}"}

    movie = MovieSchema(
        title=item["title"],
        description=item["overview"],
        score=item["vote_average"],
        popularity=item["popularity"],
        image_url=(
            TMDB_POSTER_URL + item["poster_path"] if item["poster_path"] else None
        ),
        studios=[studio["name"] for studio in item["production_companies"]],
        release_date=date.fromisoformat(item["release_date"]),
        age_rating=None,
        duration=item["runtime"],
        genres=[genre["name"] for genre in item["genres"]],
    )
    # Searching for age restriction
    for country in item["release_dates"]["results"]:
        if country["iso_3166_1"] in ("US", "RU"):
            for release in country["release_dates"]:
                if release["certification"]:
                    movie.age_rating = age_restriction_map[release["certification"]]
                    break
            break

    return movie


async def fetch_series(
    title: str, year: Optional[int] = None
) -> Union[SeriesSchema, dict[str, str]]:
    """
    Searches for series by title (and optionally by year) using the TMDB API.
    If a match is found with high confidence (>90%), it returns `SeriesSchema` object.


    Args:
        title (str): The title of the TV series.
        year (int, optional): The release year of the series.

    Returns:
        Union[SeriesSchema, dict[str, str]]: A `SeriesSchema` object containing series details
        if a match is found, otherwise a dictionary with an error message: `{"msg": ...}`.
    """
    tmdb_search_url = (
        f"/search/tv?include_adult=true&language=en-US&page=1&query={title}"
    )
    if year is not None:
        tmdb_search_url += f"&year={year}"

    async with aiohttp.ClientSession() as session:
        async with session.get(
            TMDB_BASE_URL + tmdb_search_url, headers=HEADERS
        ) as response:
            if response.status == 200:
                data = await response.json()
            else:
                return {"msg": f"HTTP {response.status}"}

        series_id = data["results"][0]["id"]

        tmdb_info_url = (
            f"/tv/{series_id}?language=en-US&append_to_response=content_ratings"
        )

        async with session.get(
            TMDB_BASE_URL + tmdb_info_url, headers=HEADERS
        ) as response:
            if response.status == 200:
                item = await response.json()
                logger.debug(item)
            else:
                return {"msg": f"HTTP {response.status}"}

    series = SeriesSchema(
        title=item["name"],
        description=item["overview"],
        score=item["vote_average"],
        popularity=item["popularity"],
        image_url=(
            TMDB_POSTER_URL + item["poster_path"] if item["poster_path"] else None
        ),
        studios=[studio["name"] for studio in item["production_companies"]],
        release_date=date.fromisoformat(item["first_air_date"]),
        episode_duration=(
            item["episode_run_time"]
            if not isinstance(item["episode_run_time"], list)
            else (
                None
                if len(item["episode_run_time"]) == 0
                else item["episode_run_time"][0]
            )
        ),
        age_rating=None,
        episodes=item["number_of_episodes"],
        genres=[genre["name"] for genre in item["genres"]],
    )
    # Searching for age restriction
    for country in item["content_ratings"]["results"]:
        if country["iso_3166_1"] in ("US", "RU"):
            series.age_rating = age_restriction_map[country["rating"]]
            break
    return series
