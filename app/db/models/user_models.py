from datetime import date
from typing import List, Optional
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Date,
    ForeignKey,
    Integer,
    SmallInteger,
    String,
    Text,
    Enum as SqlEnum,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.connection import Base
from .enums import Status


class UserReview(Base):
    """Represents a user review entity.

    Attributes:
        id (int): Primary key, auto-incremented.
        user_id (int): Foreign key to the `User` entity.
        content_id (int): Foreign key to the `Content` entity.
        user_score (Optional[int]): User rating for the content, from 0-10.
        comment (Optional[str]): Optional comment for the content.
        favorite (bool): Whether the content is marked as a favorite or not.
        status (`Status`): Enum representing the status of content in a user's queue.
        priority (int): User priority for the content, from 0-3.
        creation_date (date): Date the entry was created.
        user (`User`): The user entity linked to this entry. One-to-many relationship with `User`.
        content (`Content`): The content entity linked to this entry. One-to-many relationship with `Content`.
    """

    __tablename__ = "users_reviews"
    __table_args__ = (
        CheckConstraint(
            "user_score >= 0 AND user_score <= 10", name="check_user_score_range"
        ),
        CheckConstraint("priority >= 0 AND priority <= 3", name="check_priority_range"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    content_id: Mapped[int] = mapped_column(ForeignKey("content.id"), nullable=False)
    user_score: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    favorite: Mapped[bool] = mapped_column(Boolean, default=False)
    status: Mapped[Status] = mapped_column(SqlEnum(Status), nullable=False)
    priority: Mapped[int] = mapped_column(SmallInteger, default=0, nullable=False)
    creation_date: Mapped[date] = mapped_column(Date, default=date.today())

    content_type = relationship("Content")
    user: Mapped["User"] = relationship("User", back_populates="reviews")
    contents: Mapped[List["Content"]] = relationship(
        "Content", secondary="review_content_link", back_populates="reviews"
    )

    def __repr__(self):
        return f"<UserReview {self.id} for user {self.user_id} linked to {self.content_id}>"


class User(Base):
    """Represents a user entity.

    Attributes:
        id (int): Primary key, auto-incremented.
        username (str): Unique username, indexed and non-nullable.
        email (str): Unique email, indexed and non-nullable.
        hashed_password (str): Hashed password for user authentication.
        avatar (Optional[str]): Optional URL for the user's avatar.
        review (List[`UserReview`]): List of associated queue entries. One-to-many relationship with `UserReview`.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(
        String(100), unique=True, index=True, nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(100), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(String(100), nullable=False)
    avatar: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    creation_date: Mapped[date] = mapped_column(Date, default=date.today())

    reviews: Mapped[List[UserReview]] = relationship(
        "UserReview", back_populates="user", cascade="all, delete"
    )

    def __repr__(self):
        return f"<User {self.id} {self.username}>"
