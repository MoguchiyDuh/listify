from sqlalchemy import ForeignKey, SmallInteger, String, ARRAY, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column
from typing import List, Optional


from db.models.enums import Platforms, ContentType
from .content_model import Content


class Game(Content):
    __tablename__ = "games"
    __mapper_args__ = {"polymorphic_identity": ContentType.GAME}

    id: Mapped[int] = mapped_column(
        ForeignKey("content.id"), primary_key=True, autoincrement=True
    )
    available_platforms: Mapped[List[Platforms]] = mapped_column(
        ARRAY(SqlEnum(Platforms)), nullable=False
    )
    playtime: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    stores: Mapped[Optional[List[str]]] = mapped_column(
        ARRAY(String(50)), nullable=True
    )

    def __repr__(self):
        return f"<Game {self.id} {self.title}"
