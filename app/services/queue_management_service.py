from sqlalchemy.ext.asyncio import AsyncSession
from db.models import UserQueue
from schemas.queue_schema import QueueShowSchema
from db.crud.find_content import find_content


async def queue_db_model_to_pydantic(db: AsyncSession, db_model: UserQueue):
    content = await find_content(
        db=db, content_type=db_model.content_type, content_id=db_model.content_id
    )
    queue = QueueShowSchema.model_validate(db_model, from_attributes=True)
    return queue.model_copy(update={"content": content})
