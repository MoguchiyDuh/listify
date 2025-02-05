from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import logger
from db.models import UserQueue, User
from schemas.queue_schema import QueueAddSchema, QueueUpdateSchema


async def get_queue_items(db: AsyncSession, user_id: int) -> list[UserQueue]:
    """
    Retrieves the queue of a specific user.

    Args:
        db (AsyncSession): The database session.
        user_id (int): The ID of the user whose queue is being retrieved.

    Returns:
        list[UserQueue]: A list of queue items associated with the user.
    """
    queue = await db.execute(select(UserQueue).where(UserQueue.user_id == user_id))
    return queue.scalars().all()


async def add_to_queue(
    db: AsyncSession, user: User, queue_schema: QueueAddSchema
) -> UserQueue:
    """
    Adds a new content item to the user's queue.

    Args:
        db (AsyncSession): The database session.
        user (User): The user object representing the owner of the queue.
        queue_schema (QueueAddSchema): The schema containing queue item details.

    Returns:
        UserQueue: The newly added queue item.
    """
    queue = UserQueue(user_id=user.id, user=user, **queue_schema.model_dump())
    db.add(queue)
    await db.commit()
    await db.refresh(user)
    logger.info(
        f"Content {queue.content_type} {queue.content_id} added to queue of user {user.id} {user.username}"
    )
    return queue


async def update_queue(
    db: AsyncSession, queue_id: int, queue_schema: QueueUpdateSchema
) -> UserQueue:
    """
    Updates an existing content item in the user's queue.

    Args:
        db (AsyncSession): The database session.
        queue_id (int): The ID of the queue item to be updated.
        queue_schema (QueueUpdateSchema): The schema containing queue item details.

    Returns:
        UserQueue: The updated queue item.
    """
    result = await db.execute(select(UserQueue).where(UserQueue.id == queue_id))
    queue = result.scalars().first()

    for key, value in queue_schema.model_dump(exclude_none=True, exclude_unset=True):
        setattr(queue, key, value)
    await db.commit()
    logger.info(
        f"Content {queue.content_type} {queue.content_id} updated in queue of user {queue.user_id}"
    )
    return queue


async def delete_queue(db: AsyncSession, queue_id: int) -> dict:
    """
    Deletes an existing content item from the user's queue.

    Args:
        db (AsyncSession): The database session.
        queue_id (int): The ID of the queue item to be deleted.

    Returns:
        dict: A message indicating the success of the operation.
    """
    result = await db.execute(select(UserQueue).where(UserQueue.id == queue_id))
    queue = result.scalars().first()
    await db.delete(queue)
    await db.commit()
    logger.info(
        f"Content {queue.content_type} {queue.content_id} deleted from queue of user {queue.user_id}"
    )
    return {"msg": "Queue item deleted successfully"}
