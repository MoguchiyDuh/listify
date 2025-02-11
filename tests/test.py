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


def test_anime(session: Session, test_genre: Genre, test_tag: Tag):
    anime = Anime(
        title="One Piece",
        description="A great anime",
        score=10,
        popularity=5,
        image_url="https://example.com/image.jpg",
        age_rating=AgeRating.PG13,
        studios=["Eiichiro Oda"],
        release_date=date.today(),
        genres=[test_genre],
        tags=[test_tag],
        translated_title="One Piece",
        episodes=240,
        is_ongoing=True,
    )
    session.add(anime)
    session.commit()
    assert isinstance(anime, (Anime, Content))
