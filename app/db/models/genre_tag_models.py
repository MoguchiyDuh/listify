from sqlalchemy import (
    ForeignKey,
    String,
    Integer,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

from db.connection import Base


class ContentGenreLink(Base):
    __tablename__ = "content_genre_link"
    content_id: Mapped[int] = mapped_column(ForeignKey("content.id"), primary_key=True)
    genre_id: Mapped[int] = mapped_column(ForeignKey("genres.id"), primary_key=True)


class Genre(Base):
    """Represents a genre entity.

    Attributes:
        id (int): Primary key, auto-incremented.
        name (str): Name of the genre, indexed for efficient lookups.
        contents  (List[Content]): List of associated contents. Many-to-many relationship via `content_genre_link`.
    """

    __tablename__ = "genres"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, index=True)

    contents: Mapped[List["Content"]] = relationship(
        "Content", secondary="content_genre_link", back_populates="genres"
    )


class ContentTagLink(Base):
    __tablename__ = "content_tag_link"
    content_id: Mapped[int] = mapped_column(ForeignKey("content.id"), primary_key=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id"), primary_key=True)


class Tag(Base):
    """Represents a tag entity.

    Attributes:
        id (int): Primary key, auto-incremented.
        name (str): Name of the tag, indexed for efficient lookups.
        contents (List[Content]): List of associated contents. Many-to-many relationship via `content_tag_link`.
    """

    __tablename__ = "tags"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, index=True)

    contents: Mapped[List["Content"]] = relationship(
        "Content", secondary="content_tag_link", back_populates="tags"
    )
