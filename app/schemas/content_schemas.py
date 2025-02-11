from datetime import date
from pydantic import BaseModel, field_validator
from typing import Optional, List
from db.models import AgeRating, Platforms


class BaseModelSchema(BaseModel):
    """A base model schema for all models.

    Attributes:
        title (str): The title of the model.
        description (Optional[str]): The description of the model.
        score (Optional[float]): A float between 0 and 10 representing the score of the model.
        popularity (Optional[int]): An integer representing the popularity of the model.
        image_url (Optional[str]): A string representing the URL of the image for the model.
        age_rating(Optional[`AgeRating`]): The age rating of the model.
        studios(Optional[List[str]]): A list of strings representing the studios that the model is from.
        release_date(Optional[date]): A date object representing the release date of the model.
        genres(List[str]): A list of strings representing the genres of the model.
        tags(List[str]): A list of strings representing the tags of the model.
    """

    title: str
    description: Optional[str] = None
    score: Optional[float] = None
    popularity: Optional[int] = None
    image_url: Optional[str] = None
    age_rating: Optional[AgeRating] = None
    studios: Optional[List[str]] = None
    release_date: Optional[date] = None
    genres: List[str]
    tags: List[str]

    @field_validator("popularity", mode="before")
    def process_popularity(cls, value):
        if value is not None:
            return round(value)
        return value

    @field_validator("score", mode="before")
    def process_rating(cls, value):
        if value is not None and value > 10:
            return value / 10
        return value


class AnimeSchema(BaseModelSchema):
    """A schema for anime models.

    <h2>Inherited Attributes from `BaseModelSchema`:</h2>
        **title** (str): The title of the anime.
        **description** (Optional[str]): The description of the anime.
        **score** (Optional[float]): A float between 0 and 10 representing the score of the anime.
        **popularity** (Optional[int]): An integer representing the popularity of the anime.
        **image_url** (Optional[str]): A string representing the URL of the image for the anime.
        **age_rating** (Optional[AgeRating]): The age rating of the anime.
        **studios** (Optional[List[str]]): A list of strings representing the studios that produced the anime.
        **release_date** (Optional[date]): A date object representing the release date of the anime.
        **genres** (List[str]): A list of strings representing the genres of the anime.
        **tags** (List[str]): A list of strings representing the tags of the anime.

    <h2>Specific Attributes for `AnimeSchema`:</h2>
        **translated_title** (Optional[str]): The translated title of the anime.
        **episodes** (Optional[int]): The number of episodes in the anime.
        **is_ongoing** (bool): A boolean indicating whether the anime is ongoing.

    """

    translated_title: Optional[str] = None
    episodes: Optional[int] = None
    is_ongoing: bool = False


class GameSchema(BaseModelSchema):
    """A schema for game models.

    <h2>Inherited Attributes from `BaseModelSchema`:</h2>
        **title** (str): The title of the anime.
        **description** (Optional[str]): The description of the anime.
        **score** (Optional[float]): A float between 0 and 10 representing the score of the anime.
        **popularity** (Optional[int]): An integer representing the popularity of the anime.
        **image_url** (Optional[str]): A string representing the URL of the image for the anime.
        **age_rating** (Optional[AgeRating]): The age rating of the anime.
        **studios** (Optional[List[str]]): A list of strings representing the studios that produced the anime.
        **release_date** (Optional[date]): A date object representing the release date of the anime.
        **genres** (List[str]): A list of strings representing the genres of the anime.
        **tags** (List[str]): A list of strings representing the tags of the anime.

    <h2> Specific Attributes for `GameSchema`:</h2>
        **available_platforms** (List[Platforms]) : A list of `Platforms` objects representing the available platforms for the game.
        **playtime** (Optional[int]) : The playtime of the game in minutes.
        **stores** (List[str]): A list of strings representing the stores that have the game.
    """

    available_platforms: List[Platforms]
    playtime: Optional[int]
    stores: Optional[List[str]] = None


class MovieSchema(BaseModelSchema):
    """A schema for movie models.

    <h2>Inherited Attributes from `BaseModelSchema`:</h2>
        **title** (str): The title of the anime.
        **description** (Optional[str]): The description of the anime.
        **score** (Optional[float]): A float between 0 and 10 representing the score of the anime.
        **popularity** (Optional[int]): An integer representing the popularity of the anime.
        **image_url** (Optional[str]): A string representing the URL of the image for the anime.
        **age_rating** (Optional[AgeRating]): The age rating of the anime.
        **studios** (Optional[List[str]]): A list of strings representing the studios that produced the anime.
        **release_date** (Optional[date]): A date object representing the release date of the anime.
        **genres** (List[str]): A list of strings representing the genres of the anime.
        **tags** (List[str]): A list of strings representing the tags of the anime.

    <h2> Specific Attributes for `MovieSchema`:</h2>
        **duration**  (Optional[int]) : The duration of the movie in minutes.
    """

    duration: Optional[int]


class SeriesSchema(BaseModelSchema):
    """A schema for series models.

    <h2>Inherited Attributes from `BaseModelSchema`:</h2>
        **title** (str): The title of the anime.
        **description** (Optional[str]): The description of the anime.
        **score** (Optional[float]): A float between 0 and 10 representing the score of the anime.
        **popularity** (Optional[int]): An integer representing the popularity of the anime.
        **image_url** (Optional[str]): A string representing the URL of the image for the anime.
        **age_rating** (Optional[AgeRating]): The age rating of the anime.
        **studios** (Optional[List[str]]): A list of strings representing the studios that produced the anime.
        **release_date** (Optional[date]): A date object representing the release date of the anime.
        **genres** (List[str]): A list of strings representing the genres of the anime.
        **tags** (List[str]): A list of strings representing the tags of the anime.

    <h2> Specific Attributes for `SeriesSchema`:</h2>
        **episode_duration** (Optional[int]) : The duration of each episode in minutes.
        **episodes**   (Optional[int]) : The total number of episodes in the series.
        **is_ongoing**(bool) - Whether the series is currently ongoing or not
    """

    episode_duration: Optional[int]
    episodes: Optional[int]
    is_ongoing: bool = False
