from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import logger
from db.models import UserLibrary, User
from schemas.lib_schema import LibAddSchema, QueueUpdateSchema


async def get_lib_items(db: AsyncSession, user_id: int) -> list[UserLibrary]:
    queue = await db.execute(select(UserLibrary).where(UserLibrary.user_id == user_id))
    return queue.scalars().all()


async def add_to_lib(db: AsyncSession, content_schema: LibAddSchema) -> UserLibrary:
    content = UserLibrary(**content_schema.model_dump())
    db.add(content)
    await db.commit()
    await db.refresh(content)
    logger.info(f"Content {content.content_id} added to lib of user {content.user_id}")
    return content


async def update_lib(
    db: AsyncSession, id: int, queue_schema: QueueUpdateSchema
) -> UserLibrary:
    result = await db.execute(select(UserLibrary).where(UserLibrary.id == id))
    queue = result.scalars().first()

    for key, value in queue_schema.model_dump(exclude_none=True, exclude_unset=True):
        setattr(queue, key, value)
    await db.commit()
    logger.info(
        f"Content {queue.content_type} {queue.content_id} updated in queue of user {queue.user_id}"
    )
    return queue


async def delete_item_from_lib(db: AsyncSession, id: int) -> dict:
    """
    Deletes an existing content item from the user's queue.

    Args:
        db (AsyncSession): The database session.
        queue_id (int): The ID of the queue item to be deleted.

    Returns:
        dict: A message indicating the success of the operation.
    """
    result = await db.execute(select(UserLibrary).where(UserLibrary.id == id))
    library = result.scalars().first()
    await db.delete(library)
    await db.commit()
    logger.info(f"Content {library.content_id} deleted from {library.user_id} library")
    return {"msg": f"Content {library.content_id} deleted successfully"}
