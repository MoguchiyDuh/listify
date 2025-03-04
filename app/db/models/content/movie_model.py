from sqlalchemy import ForeignKey, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional

from db.models.enums import ContentType
from .content_model import Content


class Movie(Content):
    """Represents a movie content

    <h2>Inherited Attributes from Content model:</h2>
        **id** (int): The unique identifier of the content.
        **type** (ContentType): The type of the content.
        **title** (str): The title of the content.
        **description** (Optional[str]): The description of the content.
        **score** (Optional[float]): The score of the content, from 0 to 10.
        **popularity** (Optional[int]): The popularity of the content.
        **image_url** (Optional[str]): The URL of the image of the content.
        **age_rating** (Optional[AgeRating]): The age rating of the content.
        **studios** (Optional[List[str]]): A list of studios that produced this content, or None if unknown.
        **release_date** (Optional[date]): The date when the content was released.
        **genres** (List[Genre]): The genres associated with the content.
        **tags** (List[Tag]): The tags associated with the content.
        **reviews** (List[UserReview]): The user reviews associated with the content.

    <h2>Inherited Attributes from Movie model:</h2>
        **duration** (Optional[int]): The duration of the movie, in minutes.

    """

    __tablename__ = "movies"
    __mapper_args__ = {"polymorphic_identity": ContentType.MOVIE}

    id: Mapped[int] = mapped_column(
        ForeignKey("content.id"), primary_key=True, autoincrement=True
    )
    duration: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)

    def __repr__(self):
        return f"<Movie {self.id} {self.title}>"
