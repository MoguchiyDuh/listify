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
from enum import Enum
from db.connection import Base


class ContentType(str, Enum):
    """Enum representing different types of content.

    Values:
        ANIME (str): Represents an anime.
        GAME (str): Represents a game.
        MOVIE (str): Represents a movie.
        SERIES (str): Represents a series.
    """

    ANIME = "ANIME"
    GAME = "GAME"
    MOVIE = "MOVIE"
    SERIES = "SERIES"


class Status(str, Enum):
    """Enum representing the status of content in a user's queue.

    Values:
        FINISHED (str): The content has been completed.
        IN_PROGRESS (str): The content is currently being watched/played.
        DROPPED (str): The content has been abandoned.
        PLANNED (str): The content is planned to be watched/played in the future.
    """

    FINISHED = "FINISHED"
    IN_PROGRESS = "IN_PROGRESS"
    DROPPED = "DROPPED"
    PLANNED = "PLANNED"


class UserQueue(Base):
    """Represents a user's queue entry for a specific content type.

    Attributes:
        id (int): Primary key, auto-incremented.
        user_id (int): Foreign key linking to the `users` table.
        user (`User`): Associated `User` object, linked by `user_id`.
        content_type (ContentType): Enum representing the type of content (e.g., anime, game).
        content_id (int): ID of the specific content (anime, game, etc.).
        user_rating (Optional[int]): Optional rating given by the user.
        comment (Optional[str]): Optional user comment about the content.
        favorite (bool): Indicates if the content is marked as a favorite. Defaults to `False`.
        status (`Status`): Enum indicating the current status ("FINISHED", "IN PROGRESS", "DROPPED", "PLANNED").
        priority (int): Integer representing the priority of the content in the queue, 0 <= priority <= 3. Defaults to `0`.
    """

    __tablename__ = "users_queues"
    __table_args__ = (
        CheckConstraint(
            "user_rating >= 0 AND user_rating <= 10", name="check_user_rating_range"
        ),
        CheckConstraint("priority >= 0 AND priority <= 3", name="check_priority_range"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="queues")
    content_type: Mapped[ContentType] = mapped_column(
        SqlEnum(ContentType), nullable=False
    )
    content_id: Mapped[int] = mapped_column(Integer, nullable=False)
    user_rating: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    favorite: Mapped[bool] = mapped_column(Boolean, default=False)
    status: Mapped[Status] = mapped_column(SqlEnum(Status), nullable=False)
    priority: Mapped[int] = mapped_column(SmallInteger, default=0, nullable=False)
    creation_date: Mapped[date] = mapped_column(Date, default=date.today())

    def __repr__(self):
        return f"<UserQueue {self.id} for user {self.user_id} linked to {self.content_type.value}:{self.content_id}>"


class User(Base):
    """Represents a user entity.

    Attributes:
        id (int): Primary key, auto-incremented.
        username (str): Unique username, indexed and non-nullable.
        email (str): Unique email, indexed and non-nullable.
        hashed_password (str): Hashed password for user authentication.
        avatar (Optional[str]): Optional URL for the user's avatar.
        queues (List[`UserQueue`]): List of associated queue entries. One-to-many relationship with `UserQueue`.
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
    queues: Mapped[List[UserQueue]] = relationship("UserQueue", back_populates="user")

    def __repr__(self):
        return f"<User {self.id} {self.username}>"
