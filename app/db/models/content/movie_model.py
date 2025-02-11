from sqlalchemy import ForeignKey, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional

from db.models.enums import ContentType
from .content_model import Content


class Movie(Content):
    __tablename__ = "movies"
    __mapper_args__ = {"polymorphic_identity": ContentType.MOVIE}

    id: Mapped[int] = mapped_column(
        ForeignKey("content.id"), primary_key=True, autoincrement=True
    )
    duration: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)

    def __repr__(self):
        return f"<Movie {self.id} {self.title}>"
