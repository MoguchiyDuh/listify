from datetime import date
from sqlalchemy import Boolean, Date, ForeignKey, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional

from db.models.enums import ContentType
from .content_model import Content


class Series(Content):
    """Represents a tv series content

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

    <h2>Specific Attributes from Series model:</h2>
        **end_date**  (Optional[date]): The date when the content ended, or None if unknown.
        **episodes**  (Optional[int]): The number of episodes in the series, or None if unknown.
        **is_ongoing**  (bool): True if the content is ongoing, False otherwise.
    """

    __tablename__ = "series"
    __mapper_args__ = {"polymorphic_identity": ContentType.SERIES}

    id: Mapped[int] = mapped_column(
        ForeignKey("content.id"), primary_key=True, autoincrement=True
    )
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    episodes: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    is_ongoing: Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self):
        return f"<Series {self.id} {self.title}>"
