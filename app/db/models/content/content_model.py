from sqlalchemy import (
    ARRAY,
    CheckConstraint,
    ForeignKey,
    Numeric,
    SmallInteger,
    String,
    Integer,
    Date,
    Text,
    Enum as SqlEnum,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from typing import List, Optional

from db.connection import Base
from db.models.enums import AgeRating, ContentType


class Content(Base):
    """A base class for all content.

    Attributes:
        id (int): The unique identifier of the content.
        type (`ContentType`): The type of the content.
        title (str): The title of the content.
        description (Optional[str]): The description of the content.
        score (Optional[float]): The score of the content, from 0 to 10.
        popularity (Optional[int]): The popularity of the content.
        image_url (Optional[str]): The URL of the image of the content.
        age_rating (Optional[`AgeRating`]): The age rating of the content.
        studios(Optional[List[str]]): A list of studios that produced this content, or None if it is not known.
        release_date  (Optional[date]): The date when the content was released.
    """

    __tablename__ = "content"
    __table_args__ = (
        CheckConstraint("score >= 0 AND score <= 10", name="check_rating_range"),
        CheckConstraint("popularity >= 0", name="check_popularity"),
    )

    __mapper_args__ = {
        "polymorphic_on": "type",  # Polymorphic indicator
        "with_polymorphic": "*",
    }

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, index=True
    )
    type: Mapped[ContentType] = mapped_column(SqlEnum(ContentType), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    score: Mapped[Optional[float]] = mapped_column(
        Numeric(3, 1), nullable=True
    )  # from 0 to 10.0
    popularity: Mapped[Optional[int]] = mapped_column(
        SmallInteger, default=0, nullable=True
    )
    image_url: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    age_rating: Mapped[Optional[AgeRating]] = mapped_column(
        SqlEnum(AgeRating), nullable=True
    )
    studios: Mapped[Optional[List[str]]] = mapped_column(
        ARRAY(String(100)), nullable=True
    )
    release_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    genres: Mapped[List["Genre"]] = relationship(
        "Genre", secondary="content_genre_link", back_populates="contents"
    )
    tags: Mapped[List["Tag"]] = relationship(
        "Tag", secondary="content_tag_link", back_populates="contents"
    )
    reviews: Mapped[List["UserReview"]] = relationship(
        "UserReview",
        secondary="review_content_link",
        back_populates="contents",
    )


class ReviewContentLink(Base):
    """A link table for reviews and content, used to create a many-to-many relationship between them.

    Attributes:
        review_id (int): The unique identifier of the review.
        content_id  (int): The unique identifier of the content.
    """

    __tablename__ = "review_content_link"

    review_id: Mapped[int] = mapped_column(
        ForeignKey("users_reviews.id"), primary_key=True
    )
    content_id: Mapped[int] = mapped_column(ForeignKey("content.id"), primary_key=True)
