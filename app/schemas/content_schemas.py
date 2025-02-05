from datetime import date
from pydantic import BaseModel, field_validator
from typing import Optional, List
from db.models import AgeRestriction, Platforms


class BaseModelSchema(BaseModel):
    """Represents the base schema for media entities, inheriting from `BaseModel`.

    Attributes:
        - title (str): Required. The title of the entity.
        - description (Optional[str]): Optional. A long-form text description.
        - rating (Optional[int]): Optional. Default is `None`. The rating of the entity.
        - popularity (Optional[int]): Optional. Default is `None`. The popularity of the entity.
        - image_url (Optional[str]): Optional. The URL for an associated image.
        - age_restriction (Optional[`AgeRestriction`]): Optional. Enum value for age restrictions.
        - studios (Optional[str]): Optional. The name of the associated studios.
        - release_date (Optional[str]): Optional. The release date of the entity.
    """

    title: str
    description: Optional[str] = None
    rating: Optional[float] = None
    popularity: Optional[int] = None
    image_url: Optional[str] = None
    age_restriction: Optional[AgeRestriction] = None
    studios: Optional[List[str]] = None
    release_date: Optional[date] = None

    @field_validator("popularity", mode="before")
    def process_popularity(cls, value):
        if value is not None:
            return round(value)
        return value

    @field_validator("rating", mode="before")
    def process_rating(cls, value):
        if value is not None and value > 10:
            return value / 10
        return value


class AnimeSchema(BaseModelSchema):
    """Represents an `Anime` entity, inheriting from `BaseModelSchema`.

    Attributes:
        - from `BaseModelSchema`:
            - title (str): Required. The title of the anime.
            - description (Optional[str]): Optional. A long-form text description.
            - rating (Optional[int]): Optional. Default is `None`. The rating of the anime.
            - image_url (Optional[str]): Optional. The URL for an associated image.
            - age_restriction (Optional[`AgeRestriction`]): Optional. Enum value for age restrictions.
            - studios (Optional[str]): Optional. The name of the associated studios.
            - release_date (Optional[str]): Optional. The release date of the anime.
        - from `Anime` model:
            - is_ongoing (bool): Indicates if the anime is ongoing. Default is `False`.
            - genres (List[str]): A list of associated genres.
            - tags (List[str]): A list of associated tags.
    """

    translated_title: Optional[str] = None
    is_ongoing: bool = False
    episodes: Optional[int] = None
    genres: List[str]
    tags: List[str]


class GameSchema(BaseModelSchema):
    """Represents a `Game` entity, inheriting from `BaseModel`.

    Attributes:
        - from `BaseModelSchema`:
            - title (str): Required. The title of the anime.
            - description (Optional[str]): Optional. A long-form text description.
            - rating (Optional[int]): Optional. Default is `None`. The rating of the anime.
            - image_url (Optional[str]): Optional. The URL for an associated image.
            - age_restriction (Optional[`AgeRestriction`]): Optional. Enum value for age restrictions.
            - studios (Optional[str]): Optional. The name of the associated studios.
            - release_date (Optional[str]): Optional. The release date of the anime.
        - from `Game` model:
            - id (int): Primary key, auto-incremented.
            - available_platforms (List[`Platforms`]): A list of associated platforms.
            - duration (Optional[int]): Optional duration in minutes.
            - playtime (Optional[int]): Optional. The total playtime in minutes.
            - stores (Optional[List[str]]): A list of associated stores.
            - genres (List[str]): List of associated genres.
            - tags (List[str]): List of associated tags.

    """

    available_platforms: List[Platforms]
    playtime: Optional[int]
    stores: Optional[List[str]] = None
    genres: List[str]
    tags: List[str]


class MovieSchema(BaseModelSchema):
    """Represents a `Movie` entity, inheriting from `BaseModelSchema`.

    Attributes:
        - from `BaseModelSchema`:
            - title (str): Required. The title of the anime.
            - description (Optional[str]): Optional. A long-form text description.
            - rating (Optional[int]): Optional. Default is `None`. The rating of the anime.
            - image_url (Optional[str]): Optional. The URL for an associated image.
            - age_restriction (Optional[`AgeRestriction`]): Optional. Enum value for age restrictions.
            - studios (Optional[str]): Optional. The name of the associated studios.
            - release_date (Optional[str]): Optional. The release date of the anime.
        - from `Movie` model:
            - duration (int): The duration of the movie in minutes.
            - genres (List[str]): A list of associated genres.
    """

    duration: Optional[int]
    genres: List[str]


class SeriesSchema(BaseModelSchema):
    """Represents a `Series` entity, inheriting from `BaseModelSchema`.

    Attributes:
        - from `BaseModelSchema`:
            - title (str): Required. The title of the anime.
            - description (Optional[str]): Optional. A long-form text description.
            - rating (Optional[int]): Optional. Default is `None`. The rating of the anime.
            - image_url (Optional[str]): Optional. The URL for an associated image.
            - age_restriction (Optional[`AgeRestriction`]): Optional. Enum value for age restrictions.
            - studios (Optional[str]): Optional. The name of the associated studios.
            - release_date (Optional[str]): Optional. The release date of the anime.
        - from `Series` model:
            - episode_duration (int): The duration of the episode in minutes.
            - episodes (Optional[int]): The number of episodes.
            - is_ongoing (bool): Indicates if the series is ongoing. Defaults to `False`.
            - genres (List[str]): A list of associated genres.
    """

    episode_duration: Optional[int]
    episodes: Optional[int]
    is_ongoing: bool = False
    genres: List[str]
