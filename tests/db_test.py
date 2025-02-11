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
