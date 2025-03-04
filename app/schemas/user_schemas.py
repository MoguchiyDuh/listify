from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date
from fastapi import UploadFile


class UserProfile(BaseModel):
    """
    Schema for representing a user's public profile.

    Attributes:
        username (str): The unique username of the user.
        avatar (str): URL or path to the user's avatar.
        creation_date (date): The date when the user was created.
    """

    username: str
    avatar: str
    creation_date: date


class UserCreate(BaseModel):
    """
    Schema for creating a new user.

    Attributes:
        username (str): The unique username of the user.
        email (EmailStr): The user's email address.
        password (str): The hashed password of the user.
        avatar (Optional[UploadFile | str]): The avatar file or URL (optional).
    """

    username: str
    email: EmailStr
    password: str
    avatar: Optional[UploadFile | str] = None


class UserUpdate(BaseModel):
    """
    Schema for updating user information.

    Attributes:
        username (Optional[str]): Updated username (if provided).
        email (Optional[EmailStr]): Updated email address (if provided).
        avatar (Optional[UploadFile | str]): New avatar file or URL (optional).
        password (Optional[str]): Updated password (if provided).
    """

    username: Optional[str] = None
    email: Optional[EmailStr] = None
    avatar: Optional[UploadFile | str] = None
    password: Optional[str] = None
