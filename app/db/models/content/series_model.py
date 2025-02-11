from sqlalchemy import Boolean, ForeignKey, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional

from db.models.enums import ContentType
from .content_model import Content


class Series(Content):
    __tablename__ = "series"
    __mapper_args__ = {"polymorphic_identity": ContentType.SERIES}

    id: Mapped[int] = mapped_column(
        ForeignKey("content.id"), primary_key=True, autoincrement=True
    )
    episode_duration: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    episodes: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    is_ongoing: Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self):
        return f"<Series {self.id} {self.title}>"
