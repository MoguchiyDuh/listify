from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import logger
from db.models import UserReview, User
from schemas.review_schemas import ReviewCreateSchema, ReviewUpdateSchema


async def get_reviews(db: AsyncSession, user_id: int) -> list[UserReview]:
    queue = await db.execute(select(UserReview).where(UserReview.user_id == user_id))
    return queue.scalars().all()


async def add_review(
    db: AsyncSession, content_schema: ReviewCreateSchema
) -> UserReview:
    """
    Adds a new review item for the specified user.

    Args:
        db (AsyncSession): The database session.
        content_schema(ReviewCreateSchema): A schema containing the values for the content item.

    Returns:
        UserReview: The created review item.
    """
    review = UserReview(**content_schema.model_dump())
    db.add(review)
    await db.commit()
    await db.refresh(review)
    logger.info(
        f"Content {review.content_id} added to review {review.id} of user {review.user_id}"
    )
    return review


async def update_review(
    db: AsyncSession, user_id: int, queue_schema: ReviewUpdateSchema
) -> UserReview:
    """
    Updates an existing review item for the specified user.

    Args:
        db (AsyncSession): The database session.
        user_id (int): The ID of the user whose queue is being updated.
        queue_schema  (ReviewUpdateSchema): A schema containing the new values for the content item.

    Returns:
        UserReview: The updated review item.
    """
    result = await db.execute(select(UserReview).where(UserReview.user_id == user_id))
    review = result.scalars().first()

    for key, value in queue_schema.model_dump(exclude_none=True, exclude_unset=True):
        setattr(review, key, value)
    await db.commit()
    await db.refresh(review)
    logger.info(
        f"Content {review.content_id} updated in review {review.id} of user {review.user_id}"
    )
    return review


async def delete_item_from_lib(db: AsyncSession, user_id: int) -> dict:
    """
    Deletes an existing review item for the specified user.

    Args:
        db (AsyncSession): The database session.
        user_id (int): The ID of the user whose queue is being updated.

    Returns:
        dict: A message indicating the success of the operation.
    """
    result = await db.execute(select(UserReview).where(UserReview.user_id == user_id))
    review = result.scalars().first()
    await db.delete(review)
    await db.commit()
    logger.info(f"Review {review.id} of user {review.user_id} delete")
    return {"msg": f"Review {review.id} of user {review.user_id} deleted successfully"}
