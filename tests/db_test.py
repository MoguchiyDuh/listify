from datetime import date
import os, sys

import pytest
from sqlalchemy.orm import Session

sys.path.append(os.path.join(os.path.dirname(__file__), "../app"))
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.models import *
else:
    from db.models import *


def test_user_model(session: Session):
    """Test creating a new User."""
    user = User(
        username="test_user",
        email="test_user@example.com",
        hashed_password="hashed_password",
    )
    session.add(user)
    session.commit()

    assert user.username == "test_user"
    assert user.email == "test_user@example.com"
    assert user.hashed_password == "hashed_password"

    # Test that the User can be updated correctly.
    user.email = "new_email@example.com"
    session.commit()

    assert user.email == "new_email@example.com"

    # Test that the User can be deleted correctly.
    session.delete(user)
    session.commit()

    user = session.query(User).filter(User.username == "test_user").one_or_none()
    assert user is None


@pytest.fixture(scope="module")
def test_genre(session: Session):
    """Test creating a new Genre."""
    genre = Genre(name="Action")
    session.add(genre)
    session.commit()
    yield genre


@pytest.fixture(scope="module")
def test_tag(session: Session):
    """Test creating a new Tag."""
    tag = Tag(name="School")
    session.add(tag)
    session.commit()
    yield tag


def test_anime_model(session: Session, test_genre: Genre, test_tag: Tag):
    """Test creating a new Anime."""
    anime = Anime(
        title="test_anime",
        description="description",
        rating=1,
        image_url="image_url",
        age_restriction=AgeRestriction.G,
        studios=["studios"],
        release_date=date.today(),
        is_ongoing=False,
        genres=[test_genre],
        tags=[test_tag],
    )

    session.add(anime)
    session.commit()

    # Test that the Anime was created correctly.
    assert anime.title == "test_anime"
    assert anime.description == "description"
    assert anime.image_url == "image_url"
    assert anime.rating == 1
    assert anime.age_restriction == AgeRestriction.G
    assert anime.studios == ["studios"]
    assert anime.release_date == date.today()
    assert anime.is_ongoing is False
    assert anime.genres[0].name == "Action"
    assert anime.tags[0].name == "School"


def test_game_model(session: Session, test_genre: Genre, test_tag: Tag):
    """Test creating a new Game."""
    game = Game(
        title="test_game",
        description="description",
        rating=1,
        image_url="image_url",
        age_restriction=AgeRestriction.G,
        studios=["studios"],
        release_date=date.today(),
        available_platforms=[Platforms.PC],
        stores=["Steam"],
        genres=[test_genre],
        tags=[test_tag],
    )

    session.add(game)
    session.commit()

    assert isinstance(game, Game)


def test_series_model(session: Session, test_genre: Genre):
    """Test creating a new Series."""
    series = Series(
        title="test_series",
        description="description",
        rating=1,
        image_url="image_url",
        age_restriction=AgeRestriction.G,
        studios=["studios"],
        release_date=date.today(),
        episode_duration=25,
        episodes=10,
        is_ongoing=False,
        genres=[test_genre],
    )

    session.add(series)
    session.commit()

    assert isinstance(series, Series)


def test_movie_model(session: Session, test_genre: Genre, test_tag: Tag):
    """Test creating a new Media."""
    media = Movie(
        title="test_media",
        description="description",
        rating=1,
        image_url="image_url",
        age_restriction=AgeRestriction.G,
        studios=["studios"],
        release_date=date.today(),
        duration=100,
        genres=[test_genre],
    )

    session.add(media)
    session.commit()

    assert isinstance(media, Movie)


def test_user_queue(session: Session):
    """Test creating a new UserQueue."""
    user = User(
        username="test_user", email="test@gmail.com", hashed_password="password"
    )
    session.add(user)
    session.commit()
    anime = session.query(Anime).filter(Anime.title == "test_anime").one()

    queue = UserQueue(
        user_id=user.id,
        content_type=ContentType.ANIME,
        content_id=anime.id,
        user_rating=1,
        comment="comment",
        favorite=True,
        status=Status.PLANNED,
        priority=3,
    )

    session.add(queue)
    session.commit()

    # Test that the UserQueue was created correctly.
    assert queue.user_id == user.id
    assert queue.content_type == ContentType.ANIME
    assert queue.content_id == anime.id
    assert queue.user_rating == 1
    assert queue.comment == "comment"
    assert queue.favorite is True
    assert queue.status == Status.PLANNED
    assert queue.priority == 3


def test_link_tables(session: Session):
    """Anime-Genre, Anime-Tag, Game-Genre, Media-Genre, Media-Tag link tables test"""
    anime_genre_link = session.query(AnimeGenreLink).first()
    assert anime_genre_link.anime_id == 1
    assert anime_genre_link.genre_id == 1

    anime_tag_link = session.query(AnimeTagLink).first()
    assert anime_tag_link.anime_id == 1
    assert anime_tag_link.tag_id == 1

    game_genre_link = session.query(GameGenreLink).first()
    assert game_genre_link.game_id == 1
    assert game_genre_link.genre_id == 1

    game_tag_link = session.query(GameTagLink).first()
    assert game_tag_link.game_id == 1
    assert game_tag_link.tag_id == 1

    movie_genre_link = session.query(MovieGenreLink).first()
    assert movie_genre_link.movie_id == 1
    assert movie_genre_link.genre_id == 1

    series_genre_link = session.query(SeriesGenreLink).first()
    assert series_genre_link.series_id == 1
    assert series_genre_link.genre_id == 1
