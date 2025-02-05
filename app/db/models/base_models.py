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
    Enum as SqlaEnum,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from typing import List, Optional
from enum import Enum
from db.connection import Base


class AgeRestriction(str, Enum):
    """Enum representing age ratings for content.

    Values:
        G (str): General audiences.
        PG (str): Parental guidance suggested.
        PG13 (str): Parents strongly cautioned, some content may be inappropriate for children under 13.
        R (str): Restricted, viewers under 17 require accompanying parent or guardian.
        NC17 (str): No one 17 and under admitted.
    """

    G = "G"
    PG = "PG"
    PG13 = "PG-13"
    R = "R"
    NC17 = "NC-17"


# BaseModel is the base model for all media types
class BaseModel(Base):
    """An abstract SQLAlchemy ORM model for all media types (`Anime`, `Game`, `Movie`, `Series`).

    Attributes:
        - id (int): Primary key, auto-incremented.
        - title (str): Title of the media, indexed for efficient lookups.
        - description (Optional[str]): Description of the media.
        - rating (Optional[float]): Rating from 0 to 10.0.
        - popularity (Optional[int]): Popularity score.
        - image_url (Optional[str]): URL for a thumbnail image.
        - age_restriction (Optional[AgeRestriction]): Age restriction of the media.
        - studios (Optional[List[str]]): List of associated studios.
        - release_date (Optional[date]): Release date of the media.
    """

    __abstract__ = True
    __table_args__ = (
        CheckConstraint("rating >= 0 AND rating <= 10", name="check_rating_range"),
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    rating: Mapped[Optional[float]] = mapped_column(
        Numeric(3, 1), nullable=True
    )  # from 0 to 10.0
    popularity: Mapped[Optional[int]] = mapped_column(
        SmallInteger, default=0, nullable=True
    )
    image_url: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    age_restriction: Mapped[Optional[AgeRestriction]] = mapped_column(
        SqlaEnum(AgeRestriction), nullable=True
    )
    studios: Mapped[Optional[List[str]]] = mapped_column(
        ARRAY(String(100)), nullable=True
    )
    release_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)


# Genre and Tag many-to-many relationships
class AnimeGenreLink(Base):
    __tablename__ = "anime_genre_link"
    anime_id: Mapped[int] = mapped_column(ForeignKey("animes.id"), primary_key=True)
    genre_id: Mapped[int] = mapped_column(ForeignKey("genres.id"), primary_key=True)


class AnimeTagLink(Base):
    __tablename__ = "anime_tag_link"
    anime_id: Mapped[int] = mapped_column(ForeignKey("animes.id"), primary_key=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id"), primary_key=True)


class GameGenreLink(Base):
    __tablename__ = "game_genre_link"
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"), primary_key=True)
    genre_id: Mapped[int] = mapped_column(ForeignKey("genres.id"), primary_key=True)


class GameTagLink(Base):
    __tablename__ = "game_tag_link"
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"), primary_key=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id"), primary_key=True)


class MovieGenreLink(Base):
    __tablename__ = "movie_genre_link"
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"), primary_key=True)
    genre_id: Mapped[int] = mapped_column(ForeignKey("genres.id"), primary_key=True)


class SeriesGenreLink(Base):
    __tablename__ = "series_genre_link"
    series_id: Mapped[int] = mapped_column(ForeignKey("series.id"), primary_key=True)
    genre_id: Mapped[int] = mapped_column(ForeignKey("genres.id"), primary_key=True)


# Genre and Tag Models
class Genre(Base):
    """Represents a genre entity.

    Attributes:
        - id (int): Primary key, auto-incremented.
        - name (str): Name of the genre, indexed for efficient lookups.
        - animes (List[Anime]): List of associated animes. Many-to-many relationship via `anime_genre_link`.
        - games (List[Game]): List of associated games. Many-to-many relationship via `game_genre_link`.
        - movies (List[Movie]): List of associated movies. Many-to-many relationship via `movie_genre_link`.
        - series (List[Series]): List of associated series. Many-to-many relationship via `series_genre_link`.
    """

    __tablename__ = "genres"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, index=True)

    animes: Mapped[List["Anime"]] = relationship(
        "Anime", secondary="anime_genre_link", back_populates="genres"
    )
    games: Mapped[List["Game"]] = relationship(
        "Game", secondary="game_genre_link", back_populates="genres"
    )
    movies: Mapped[List["Movie"]] = relationship(
        "Movie", secondary="movie_genre_link", back_populates="genres"
    )
    series: Mapped[List["Series"]] = relationship(
        "Series", secondary="series_genre_link", back_populates="genres"
    )


class Tag(Base):
    """Represents a tag entity.

    Attributes:
        - id (int): Primary key, auto-incremented.
        - name (str): Name of the tag, indexed for efficient lookups.
        - animes (List[Anime]): List of associated animes. Many-to-many relationship via `anime_tag_link`.
    """

    __tablename__ = "tags"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, index=True)

    animes: Mapped[List["Anime"]] = relationship(
        "Anime", secondary="anime_tag_link", back_populates="tags"
    )
    games: Mapped[List["Game"]] = relationship(
        "Game", secondary="game_tag_link", back_populates="tags"
    )
