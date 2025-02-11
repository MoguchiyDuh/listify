import os
import shutil
from fastapi import Depends, HTTPException, UploadFile, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4

from db.connection import get_session
from core.security import PasswordManager, TokenManager
from core.logger import setup_logger
from db.models.user_models import User
from db.crud.user_crud import (
    get_user,
    create_user,
    update_user,
    delete_user,
)
from schemas.user_schemas import UserCreate, UserUpdate

logger = setup_logger("user_service")


async def authenticate_user(credentials: str, password: str, db: AsyncSession) -> str:
    """
    Authenticate a user with given credentials and password.

    Args:
        db: The database session or connection object.
        credentials (str): The user's identifier (e.g., username or email).
        password (str): The user's password.

    Returns:
        str: The generated access token for the authenticated user.

    Raises:
        HTTPException: If the user is not found, raises a 404 HTTP exception.
    """
    user = await get_user(db=db, user_identifier=credentials)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if not PasswordManager.validate_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    access_token = TokenManager.create_token(payload={"sub": user.username})

    return access_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token")


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_session)
) -> User:
    """
    Retrieve the current user based on the provided token.

    Args:
        token (str): The authentication token for the user.
        db (AsyncSession, optional): The database session dependency. Defaults to Depends(get_session).

    Returns:
        UserModel: The user model corresponding to the authenticated user.

    Raises:
        HTTPException: If the user is not found, raises a 404 HTTP exception.
    """
    username = TokenManager.validate_token(token)

    user = await get_user(db=db, user_identifier=username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return user


async def register_user(db: AsyncSession, user_schema: UserCreate) -> User:
    """Register a new user.

    This function creates a new user after validating that the username and email
    do not already exist. It also hashes the password before storing the user data

    Args:
        user_schema (UserCreate): Schema containing user registration details.

    Raises:
        HTTPException: 400 Bad Request if the username or email already exists.

    Returns:
        User: The created user object.
    """
    if await get_user(db=db, user_identifier=user_schema.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists"
        )
    if await get_user(db=db, user_identifier=user_schema.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists"
        )

    user_schema.password = PasswordManager.hash_password(user_schema.password)

    user = await create_user(db=db, user_schema=user_schema)

    return user


def save_image(avatar: UploadFile, dir: str) -> str:
    """
    Saves an uploaded image file to the specified directory.

    Args:
        avatar (UploadFile): The uploaded image file.
        dir (str): The directory where the image will be saved.

    Returns:
        str: The file path of the saved image.

    Raises:
        HTTPException: If the image format is not jpg, jpeg, or png.
    """
    file_extension = avatar.filename.split(".")[-1]
    if file_extension not in ["jpg", "jpeg", "png"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid image format"
        )
    file_name = f"{uuid4()}.{file_extension}"
    file_path = os.path.join(dir, file_name)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(avatar.file, buffer)

    logger.info(f"Saved image to {file_path}")

    return file_path


async def update_user_profile(
    db: AsyncSession, user: User, user_schema: UserUpdate
) -> User:
    if (
        user.username is not None
        and user.username != user_schema.username
        and await get_user(db=db, user_identifier=user_schema.username)
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists"
        )

    if (
        user.email is not None
        and user.email != user_schema.email
        and await get_user(db=db, user_identifier=user_schema.email)
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists"
        )

    if user_schema.password:
        user_schema.password = PasswordManager.hash_password(user_schema.password)

    if user_schema.avatar:
        if user_schema.avatar.size > 1024 * 1024 * 5:
            logger.warning("Avatar is too big")
        else:
            try:
                avatar_path = save_image(user_schema.avatar, dir="./static/avatars")
                if os.path.exists(user.profile_photo):
                    os.remove(user.avatar)
                user_schema.avatar = avatar_path
            except Exception as e:
                logger.error(f"Error saving avatar: {e}")

    updated_user = await update_user(db=db, user=user, user_schema=user_schema)

    return updated_user


async def delete_user_profile(db: AsyncSession, user: User, password: str) -> dict:
    if not PasswordManager.validate_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password"
        )

    response = await delete_user(db=db, user=user)

    return response
