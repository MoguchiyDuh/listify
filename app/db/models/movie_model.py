from sqlalchemy import Integer, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional
from .base_models import BaseModel


class Movie(BaseModel):
    """Represents a movie entity, inheriting from `BaseModel`.

    Attributes:
        - from `BaseModel`:
            - title (str): Required, max length 255, indexed. Entity title.
            - description (Optional[str]): Optional long-form text description.
            - rating (int): Required, default 0. Entity rating (SmallInteger).
            - image_url (Optional[str]): Optional, max length 100. URL for an image.
            - age_restriction (`AgeRestriction`): Required enum for age restrictions.
            - studios (Optional[str]): Optional, max length 100. Associated studios name.
            - release_date (Optional[date]): Optional release date of the entity.
        - from `Movie` model:
            - id (int): Primary key, auto-incremented.
            - duration (Optional[int]): Optional duration in minutes (`SmallInteger`).
            - genres (List[`Genre`]): List of associated genres. Many-to-many relationship via `movie_genre_link`.
    """

    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    duration: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)

    genres: Mapped[List["Genre"]] = relationship(
        "Genre", secondary="movie_genre_link", back_populates="movies"
    )

    def __repr__(self):
        return f"<Movie {self.id} {self.title}>"
