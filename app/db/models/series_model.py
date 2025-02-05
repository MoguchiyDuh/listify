from sqlalchemy import Boolean, Integer, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional
from .base_models import BaseModel


class Series(BaseModel):
    """Represents a series entity, inheriting from `BaseModel`.

    Attributes:
        - from `BaseModel`:
            - title (str): Required, max length 255, indexed. Entity title.
            - description (Optional[str]): Optional long-form text description.
            - rating (int): Required, default 0. Entity rating (SmallInteger).
            - image_url (Optional[str]): Optional, max length 100. URL for an image.
            - age_restriction (`AgeRestriction`): Required enum for age restrictions.
            - studios (Optional[str]): Optional, max length 100. Associated studios name.
            - release_date (Optional[date]): Optional release date of the entity.
        - from `series` model:
            - id (int): Primary key, auto-incremented.
            - episode_duration (Optional[int]): Optional duration of each episode (`SmallInteger`).
            - episodes (Optional[int]): Optional number of episodes (`SmallInteger`)
            - is_ongoing (bool): Optional, default False. Is the series ongoing? (`Boolean`).
            - genres (List[`Genre`]): List of associated genres. Many-to-many relationship via `series_genre_link`.
    """

    __tablename__ = "series"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    episode_duration: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    episodes: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    is_ongoing: Mapped[bool] = mapped_column(Boolean, default=False)

    genres: Mapped[List["Genre"]] = relationship(
        "Genre", secondary="series_genre_link", back_populates="series"
    )

    def __repr__(self):
        return f"<Series {self.id} {self.title}>"
