from sqlalchemy import Boolean, Integer, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional
from .base_models import BaseModel


class Anime(BaseModel):
    """Represents an anime entity, inheriting from `BaseModel`.

    Attributes:
        - from `BaseModel`:
            - title (str): Required, max length 255, indexed. Entity title.
            - description (Optional[str]): Optional long-form text description.
            - rating (int): Required, default 0. Entity rating (SmallInteger).
            - image_url (Optional[str]): Optional, max length 100. URL for an image.
            - age_restriction (AgeRestriction): Required enum for age restrictions.
            - studios (Optional[str]): Optional, max length 100. Associated studios name.
            - release_date (Optional[date]): Optional release date of the entity.
        - from `Anime` model:
            - id (int): Primary key, auto-incremented.
            - translated_title (Optional[str]): Optional, max length 100. Translated title of the entity.
            - episodes (int): Optional number of episodes.
            - is_ongoing (bool): Indicates if the anime is ongoing. Defaults to `False`.
            - genres (List[Genre]): List of associated genres. Many-to-many relationship via `anime_genre_link`.
            - tags (List[Tag]): List of associated tags. Many-to-many relationship via `anime_tag_link`.
    """

    __tablename__ = "animes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    translated_title: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    episodes: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    is_ongoing: Mapped[bool] = mapped_column(Boolean, default=False)

    genres: Mapped[List["Genre"]] = relationship(
        "Genre", secondary="anime_genre_link", back_populates="animes"
    )
    tags: Mapped[List["Tag"]] = relationship(
        "Tag", secondary="anime_tag_link", back_populates="animes"
    )

    def __repr__(self):
        return f"<Anime {self.id} {self.title}>"
