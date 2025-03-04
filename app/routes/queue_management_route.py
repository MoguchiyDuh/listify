from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.connection import get_session
from db.models import User
from db.crud.review_crud import get_reviews, add_review
from db.crud.content_crud import get_content
from schemas.review_schemas import ReviewCreateSchema
from services.user_service import get_current_user

router = APIRouter()


@router.get("/my_queue")
async def my_queue_endpoint(
    user: User = Depends(get_current_user), db: AsyncSession = Depends(get_session)
):
    queue_items = await get_reviews(db=db, user_id=user.id)
    return queue_items


@router.post("/my_queue")
async def add_to_queue_endpoint(
    queue_schema: ReviewCreateSchema = Depends(),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    queue_item = await add_review(db=db, content_schema=queue_schema, user=user)
    return queue_item
