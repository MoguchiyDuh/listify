import os
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import logger
from db.models.user_models import User
from schemas.user_schemas import UserCreate, UserUpdate


async def get_user(db: AsyncSession, user_identifier: int | str | None) -> User | None:
    """Retrieves a user from the database based on their identifier.

    Args:
        db (AsyncSession, optional): The database session used for querying. This is injected by the `Depends(get_session)` dependency. Defaults to a new session if not provided.
        user_identifier (int | str | None): The identifier of the user to retrieve. If an integer is provided, it will be used as the user ID. If a string is provided, it will be used as the user username or email. Defaults to None.

    Returns:
        User|None: The user object if found, None otherwise.
    """

    if not user_identifier:
        return None
    query = select(User)

    if isinstance(user_identifier, int) or user_identifier.isdecimal():  # Search by ID
        user_identifier = int(user_identifier)
        query = query.filter(User.id == user_identifier)
    else:
        query = query.filter(
            (User.username == user_identifier) | (User.email == user_identifier)
        )

    result = await db.execute(query)
    user = result.scalars().first()
    return user


async def create_user(db: AsyncSession, user_schema: UserCreate) -> User:
    """Creates a new user in the database.

    Args:
        db (AsyncSession, optional): The database session used for querying. This is injected by the `Depends(get_session)` dependency. Defaults to a new session if not provided.
        user_schema (UserCreate): The Pydantic model that contains the user data for creation.

    Returns:
        User: The newly created `User` object.
    """

    user_schema = user_schema.model_dump()
    user_schema["hashed_password"] = user_schema.pop("password")
    user = User(**user_schema)

    db.add(user)
    await db.commit()
    await db.refresh(user)
    logger.info(f"{user} created")
    return user


async def update_user(db: AsyncSession, user: User, user_schema: UserUpdate) -> User:
    """Updates an existing user with the data from the `UserUpdate` schema.

    Args:
        db (AsyncSession, optional): Database session.
        user (User): User to be updated.
        user_schema (UserUpdate): Updated user data.

    Returns:
        User: The updated `User` object.
    """
    user_schema = user_schema.model_dump(exclude_none=True, exclude_unset=True)
    if user_schema["password"] is not None:
        user_schema["hashed_password"] = user_schema.pop("password")

    for key, value in user_schema.items():
        if hasattr(user, key):
            setattr(user, key, value)

    await db.commit()
    await db.refresh(user)
    logger.info(f"{user} updated")
    return user


async def delete_user(db: AsyncSession, user: User) -> dict:
    """Deletes a user from the database and removes their avatar if it exists.

    Args:
        db (AsyncSession, optional): Database session.
        user (User): User to be deleted.

    Returns:
        dict: A dictionary containing a message indicating the deletion status. `{'msg': ...}`
    """

    if user.avatar is not None and os.path.exists(user.avatar):
        os.remove(user.avatar)

    await db.delete(user)
    await db.commit()
    logger.info(f"{user} deleted")

    return {"msg": f"{user} has been deleted successfully"}
