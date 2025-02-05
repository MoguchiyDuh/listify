from datetime import date
from typing import Optional, Union
import aiohttp
from thefuzz import process

from . import logger
from core.config import TMDB_API_KEY
from schemas.content_schemas import MovieSchema, SeriesSchema
from db.models import AgeRestriction

age_restriction_map = {
    "NR": None,
    # US
    "G": AgeRestriction.G,
    "PG": AgeRestriction.PG,
    "PG-13": AgeRestriction.PG13,
    "R": AgeRestriction.R,
    "NC-17": AgeRestriction.NC17,
    # RU
    "0+": AgeRestriction.G,
    "6+": AgeRestriction.PG,
    "12+": AgeRestriction.PG13,
    "16+": AgeRestriction.R,
    "18+": AgeRestriction.NC17,
    # US TV
    "TV-Y": AgeRestriction.G,
    "TV-Y7": AgeRestriction.G,
    "TV-Y7-FV": AgeRestriction.G,
    "TV-G": AgeRestriction.G,
    "TV-PG": AgeRestriction.PG,
    "TV-14": AgeRestriction.PG13,
    "TV-MA": AgeRestriction.R,
}

TMDB_BASE_URL = f"https://api.themoviedb.org/3"
HEADERS = {"accept": "application/json", "Authorization": f"Bearer {TMDB_API_KEY}"}
TMDB_POSTER_URL = "https://image.tmdb.org/t/p/original"


async def fetch_movie(
    title: str, year: Optional[int] = None
) -> Union[MovieSchema, dict[str, str]]:
    """
    Searches for a movie by title (and optionally by year) using the TMDB API.
    If a match is found with high confidence (>90%), it returns `MovieSchema` object.

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

        movie_list = {item["id"]: item.get("title") for item in data["results"]}
        match = process.extractOne(title, list(movie_list.values()), score_cutoff=90)
        if match is None:
            return {"msg": "Movie not found"}
        else:
            for id, value in movie_list.items():
                if match[0] == value:
                    movie_id = id

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
        rating=item["vote_average"],
        popularity=item["popularity"],
        image_url=(
            TMDB_POSTER_URL + item["poster_path"] if item["poster_path"] else None
        ),
        studios=[studio["name"] for studio in item["production_companies"]],
        release_date=date.fromisoformat(item["release_date"]),
        age_restriction=None,
        duration=item["runtime"],
        genres=[genre["name"] for genre in item["genres"]],
    )
    # Searching for age restriction
    for country in item["release_dates"]["results"]:
        if country["iso_3166_1"] in ("US", "RU"):
            for release in country["release_dates"]:
                if release["certification"]:
                    movie.age_restriction = age_restriction_map[
                        release["certification"]
                    ]
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

        # series_list = {item["id"]: item.get("name") for item in data["results"]}
        # match = process.extractOne(title, list(series_list.values()), score_cutoff=90)
        # if match is None:
        #     return {"msg": "Series not found"}
        # else:
        #     for id, value in series_list.items():
        #         if match[0] == value:
        #             series_id = id
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
        rating=item["vote_average"],
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
        age_restriction=None,
        episodes=item["number_of_episodes"],
        genres=[genre["name"] for genre in item["genres"]],
    )
    # Searching for age restriction
    for country in item["content_ratings"]["results"]:
        if country["iso_3166_1"] in ("US", "RU"):
            series.age_restriction = age_restriction_map[country["rating"]]
            break
    return series
