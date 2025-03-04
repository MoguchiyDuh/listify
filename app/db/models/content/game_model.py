from sqlalchemy import ForeignKey, SmallInteger, String, ARRAY, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column
from typing import List, Optional


from db.models.enums import Platforms, ContentType
from .content_model import Content


class Game(Content):
    """Represents a game content

    <h2>Inherited Attributes from Content model:</h2>
        **id** (int): The unique identifier of the content.
        **type** (ContentType): The type of the content.
        **title** (str): The title of the content.
        **description** (Optional[str]): The description of the content.
        **score** (Optional[float]): The score of the content, from 0 to 10.
        **popularity** (Optional[int]): The popularity of the content.
        **image_url** (Optional[str]): The URL of the image of the content.
        **age_rating** (Optional[AgeRating]): The age rating of the content.
        **studios** (Optional[List[str]]): A list of studios that produced this content, or None if unknown.
        **release_date** (Optional[date]): The date when the content was released.
        **genres** (List[Genre]): The genres associated with the content.
        **tags** (List[Tag]): The tags associated with the content.
        **reviews** (List[UserReview]): The user reviews associated with the content.

    <h2>Specific Attributes for Game model:</h2>
        **available_platforms**  (List[Platforms]): A list of platforms that the content is available on.
        **playtime**   (Optional[int]): The length of the game in minutes.
        **stores**   (Optional[List[str]]): A list of stores that sell the game.
    """

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
