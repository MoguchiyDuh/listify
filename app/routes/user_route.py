from fastapi import APIRouter, HTTPException, Depends, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from db.crud.user_crud import get_user
from db.models.user_models import User
from db.connection import get_session
from schemas.user_schemas import UserCreate, UserProfile, UserUpdate
from services.user_service import (
    authenticate_user,
    delete_user_profile,
    get_current_user,
    register_user,
    update_user_profile,
)

router = APIRouter()


@router.post("/register")
async def register(
    db: AsyncSession = Depends(get_session), user_schema: UserCreate = Depends()
):
    """Register a new user.

    Args:
        user_schema (UserCreate): User schema to register.
        db (AsyncSession, optional): Database connection. Defaults to Depends(get_db).

    Returns:
        UserProfile: User profile schema
    """
    user = await register_user(db=db, user_schema=user_schema)
    return UserProfile.model_validate(user, from_attributes=True)


@router.post("/token")
async def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_session),
):
    access_token = await authenticate_user(
        db=db, credentials=form_data.username, password=form_data.password
    )
    # max age is 30 minutes
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=30 * 60,
        secure=True,
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
async def logout_user(response: Response):
    """Log out user by clearing the cookie."""
    response.delete_cookie(key="access_token")
    return {"msg": "Logged out successfully"}


@router.get("/profile/me")
async def get_my_profile(user: User = Depends(get_current_user)):
    """Get the current user profile.

    Args:
        user (UserModel): user model. Defaults to Depends(get_current_user).

    Returns:
        UserProfile: User profile schema
    """

    return UserProfile.model_validate(user, from_attributes=True)


@router.get("/profile/{username}")
async def get_user_profile(username: str, db: AsyncSession = Depends(get_session)):
    """Get a user profile by username.

    Args:
        username (str): The username of the user.
        db (AsyncSession, optional): Database connection. Defaults to Depends(get_db).

    Returns:
        UserProfile: User profile schema
    """
    user = await get_user(db=db, user_identifier=username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return UserProfile.model_validate(user, from_attributes=True)


@router.put("/profile/me")
async def update_my_profile(
    user_schema: UserUpdate = Depends(),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    """
    Update the current user's profile.

    Args:
        user_schema (UserCreate): The schema containing the new user profile data.
        user (UserModel): The current authenticated user, obtained from the dependency.
        db (AsyncSession): The database session, obtained from the dependency.

    Returns:
        UserModel: The updated user profile information.
    """
    updated_user = await update_user_profile(db=db, user=user, user_schema=user_schema)
    return UserProfile.model_validate(updated_user, from_attributes=True)


@router.delete("/profile/me")
async def delete_my_profile(
    password: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    """
    Delete the current user's profile.

    Args:
        password (str): The password of the current user.
        user (UserModel): The current user, obtained from the dependency injection. Defaults to Depends(get_current_user).
        db (AsyncSession): The database session, obtained from the dependency injection. Defaults to Depends(get_db).

    Returns:
        dict: A message indicating that the profile was deleted successfully.
    """
    await delete_user_profile(db=db, user=user, password=password)
    return {"msg": "Profile deleted successfully"}
