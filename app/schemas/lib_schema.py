from typing import Literal, Optional, Union
from pydantic import BaseModel, Field


from db.models import ContentType, Status, UserLibrary
from .content_schemas import MovieSchema, SeriesSchema, AnimeSchema, GameSchema


class QueueShowSchema(BaseModel):
    user_id: int
    content_id: int
    user_rating: Optional[int] = None
    comment: Optional[str] = None
    favorite: bool
    status: Status
    priority: int


class LibAddSchema(BaseModel):
    content_id: int
    user_rating: Optional[int] = Field(default=None, ge=0, le=10)
    comment: Optional[str] = None
    favorite: bool = False
    status: Literal["finished", "in_progress", "dropped", "planned"]
    priority: int = Field(
        default=0, ge=0, le=3
    )  # priority in [0,3], default is 0 (no priority)


class QueueUpdateSchema(BaseModel):
    user_rating: Optional[int] = Field(default=None, ge=0, le=10)
    comment: Optional[str] = None
    favorite: Optional[bool] = None
    status: Optional[Status] = None
    priority: Optional[int] = Field(default=None, ge=0, le=3)
