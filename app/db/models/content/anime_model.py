from sqlalchemy import Boolean, ForeignKey, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional

from db.models.enums import ContentType
from .content_model import Content


class Anime(Content):
    __tablename__ = "animes"
    __mapper_args__ = {"polymorphic_identity": ContentType.ANIME}

    id: Mapped[int] = mapped_column(
        ForeignKey("content.id"), primary_key=True, autoincrement=True
    )
    translated_title: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    episodes: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    is_ongoing: Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self):
        return f"<Anime {self.id} {self.title}>"
