from db.models import Content, Anime, Game, Movie, Series
from schemas.content_schemas import (
    AnimeSchema,
    BaseModelSchema,
    GameSchema,
    MovieSchema,
    SeriesSchema,
)


from typing import Literal, Type
from sqlalchemy import asc, desc, select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_content(
    db: AsyncSession, content_id: int
) -> Anime | Game | Movie | Series | None:
    """Get content by ID

    Args:
        db (AsyncSession): Database session
        content_id (int): ID of the content to retrieve

    Returns:
        `Anime`|`Game`|`Movie`|`Series`|None: The retrieved content or None if not found
    """
    result = await db.execute(select(Content).filter(Content.id == content_id))
    content = result.scalars().first()

    return content


async def get_content_by_type(
    db: AsyncSession,
    content_type: Literal["anime", "game", "movie", "series"],
    page: int = 1,
    page_size: int = 10,
    sort_by: Literal["popularity", "rating", "release_date", "title"] = "popularity",
    sort_order: Literal["desc", "asc"] = "desc",
) -> list[Anime | Game | Movie | Series]:
    """Get content by type and page

    Args:
        db  (AsyncSession): Database session
        content_type   (Literal["anime", "game", "movie", "series"]): Type of the content to retrieve
        page           (int): Page number. Defaults to 1.
        page_size      (int): Number of content per page. Defaults to 10.
        sort_by        (Literal["popularity", "rating", "release_date", "title"], optional): Column to sort by. Defaults to "popularity".
        sort_order     (Literal["desc", "asc"], optional): Order of sorting. Defaults to "desc".

    Returns:
        list[`Anime`|`Game`|`Movie`|`Series`]: List of retrieved content or empty list if not found
    """
    model_map = {
        "anime": Anime,
        "game": Game,
        "movie": Movie,
        "series": Series,
    }
    content_model = model_map.get(content_type)
    if not content_model:
        return []

    order_by_column = getattr(content_model, sort_by, None)
    if not order_by_column:
        return []

    order_by = desc(order_by_column) if sort_order == "desc" else asc(order_by_column)

    query = (
        select(content_model)
        .order_by(order_by)
        .offset((page - 1) * page_size)
        .limit(page_size)
    )

    result = await db.execute(query)
    return result.scalars().all()


model_mapping: dict[Type[BaseModelSchema], Type[Content]] = {
    AnimeSchema: Anime,
    GameSchema: Game,
    MovieSchema: Movie,
    SeriesSchema: Series,
}


async def add_content(
    db: AsyncSession,
    content_schema: AnimeSchema | GameSchema | MovieSchema | SeriesSchema,
):
    """Add content to the database

    Args:
        db  (AsyncSession): Database session
        content_schema   (`AnimeSchema`|`GameSchema`|`MovieSchema`|`SeriesSchema`): Schema of the content to add

    Returns:
        `AnimeSchema`: The added `AnimeSchema`
    """
    model_class = model_mapping.get(type(content_schema))
    if not model_class:
        raise ValueError("Unsupported content schema type.")

    content = model_class(**content_schema.model_dump())

    db.add(content)
    await db.commit()
    await db.refresh(content)
    return content


async def update_content(
    db: AsyncSession,
    content_id: int,
    content_schema: AnimeSchema | GameSchema | MovieSchema | SeriesSchema,
) -> AnimeSchema | None:
    """Update content in the database

    Args:
        db   (AsyncSession): Database session
        content_id  (int): ID of the content to update
        content_schema     (`AnimeSchema`|`GameSchema`|`MovieSchema`|`SeriesSchema`): Schema of the content to add

    Returns:
        `AnimeSchema`|None: The updated `AnimeSchema` or None if not found
    """
    model_class = model_mapping.get(type(content_schema))
    if not model_class:
        raise ValueError("Unsupported content schema type.")

    result = await db.execute(select(model_class).filter_by(id=content_id))
    content = result.scalars().first()

    if not content:
        return None

    update_data = content_schema.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(content, key, value)

    await db.commit()
    await db.refresh(content)
    return content


async def delete_content(db: AsyncSession, content_id: int) -> dict[str, str]:
    """Delete content from the database

    Args:
        db   (AsyncSession): Database session
        content_id       (int): ID of the content to delete

    Returns:
        dict: Dictionary containing the message of the deletion
    """
    result = await db.execute(select(Content).filter_by(id=content_id))
    content = result.scalars().first()

    await db.delete(content)
    await db.commit()
    return {"msg": "Deleted successfully"}
