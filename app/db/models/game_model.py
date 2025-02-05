from sqlalchemy import Integer, SmallInteger, String, ARRAY, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional
from enum import Enum
from .base_models import BaseModel


class Platforms(str, Enum):
    """Enum representing various gaming platforms.

    This enumeration defines different platforms on which games can be played,
    including PC, consoles, mobile devices.

    Attributes:
        - PC (str): PC platform.
        - PS3 (str): PlayStation 3 platform.
        - PS4 (str): PlayStation 4 platform.
        - PS5 (str): PlayStation 5 platform.
        - XBOX_360 (str): Xbox 360 platform.
        - XBOX_ONE (str): Xbox One platform.
        - XBOX_SERIES_X (str): Xbox Series X platform.
        - NINTENDO_SWITCH (str): Nintendo Switch platform.
        - IOS (str): iOS platform.
        - ANDROID (str): Android platform.
    """

    PC = "PC"
    PS3 = "PS3"
    PS4 = "PS4"
    PS5 = "PS5"
    XBOX_360 = "XBOX 360"
    XBOX_ONE = "XBOX ONE"
    XBOX_SERIES_X = "XBOX SERIES X"
    NINTENDO_SWITCH = "NINTENDO SWITCH"
    IOS = "IOS"
    ANDROID = "ANDROID"
    WEB = "WEB"


class Game(BaseModel):
    """Represents a game entity, inheriting from `BaseModel`.

    Attributes:
        - from `BaseModel`:
            - title (str): Required, max length 255, indexed. Entity title.
            - description (Optional[str]): Optional long-form text description.
            - rating (int): Required, default 0. Entity rating (SmallInteger).
            - image_url (Optional[str]): Optional, max length 100. URL for an image.
            - age_restriction (`AgeRestriction`): Required enum for age restrictions.
            - studios (Optional[str]): Optional, max length 100. Associated studios name.
            - release_date (Optional[date]): Optional release date of the entity.
        - from `Game` model:
            - id (int): Primary key, auto-incremented.
            - available_platforms (List[`Platforms`]): List of platforms where the game is available, stored as an array of `Platforms` enum values.
            - stores (Optional[List[str]]): Optional list of store names (max length: 50 per store) where the game is available.
            - genres (List[`Genre`]): List of associated genres. Many-to-many relationship via `game_genre_link`.
            - tags (List[`Tag`]): List of associated tags. Many-to-many relationship via `game_tag_link`.
    """

    __tablename__ = "games"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    available_platforms: Mapped[List[Platforms]] = mapped_column(
        ARRAY(SqlEnum(Platforms)), nullable=False
    )
    playtime: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    stores: Mapped[Optional[List[str]]] = mapped_column(
        ARRAY(String(50)), nullable=True
    )

    genres: Mapped[List["Genre"]] = relationship(
        "Genre", secondary="game_genre_link", back_populates="games"
    )
    tags: Mapped[List["Tag"]] = relationship(
        "Tag", secondary="game_tag_link", back_populates="games"
    )

    def __repr__(self):
        return f"<Game {self.id} {self.title}"
