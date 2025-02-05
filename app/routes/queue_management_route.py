from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.connection import get_session
from db.models import User
from db.crud.queue_crud import get_queue_items, add_to_queue
from schemas.queue_schema import QueueAddSchema
from services.user_service import get_current_user
from services.queue_management_service import queue_db_model_to_pydantic

router = APIRouter()


@router.get("/my_queue")
async def my_queue_endpoint(
    user: User = Depends(get_current_user), db: AsyncSession = Depends(get_session)
):
    queue_items = await get_queue_items(db=db, user_id=user.id)
    return [
        await queue_db_model_to_pydantic(db=db, db_model=queue_item)
        for queue_item in queue_items
    ]


@router.post("/my_queue")
async def add_to_queue_endpoint(
    queue_schema: QueueAddSchema = Depends(),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    queue_item = await add_to_queue(db=db, queue_schema=queue_schema, user=user)
    return await queue_db_model_to_pydantic(db=db, db_model=queue_item)
