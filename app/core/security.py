import bcrypt
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from .config import SECRET_KEY


class PasswordManager:
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a plaintext password.

        Args:
            password (str): Plaintext password to hash.

        Returns:
            str: Hashed password
        """
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed_password.decode("utf-8")

    @staticmethod
    def validate_password(password: str, hashed_password: str) -> bool:
        """Validate a plaintext password against a hashed password.

        Args:
            password (str): Plaintext password to validate.
            hashed_password (str): Hashed password to compare against.

        Returns:
            bool: True if the plaintext password matches the hashed password, False otherwise.

        """
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


class TokenManager:
    secret_key = SECRET_KEY
    algorithm = "HS256"

    @classmethod
    def create_token(cls, payload: dict, expires_in: int = 3600) -> str:
        """Create a JWT token from a payload and an expiration time in seconds.

        Args:
            payload (dict): Payload to encode in the JWT.
            expires_in (int, optional): Expiration time in seconds. Defaults to 3600.

        Returns:
            str: JWT token
        """
        payload["exp"] = datetime.now(tz=timezone.utc) + timedelta(seconds=expires_in)
        token = jwt.encode(payload.copy(), cls.secret_key, algorithm=cls.algorithm)
        return token

    @classmethod
    def validate_token(cls, token: str) -> str:
        """Validate a JWT token and return its payload.

        Args:
            token (str): JWT token to validate.

        Raises:
            HTTPException: if the JWT token is expired.
            HTTPException: if the JWT token is not valid.

        Returns:
            str: Username of the user associated with the JWT token.
        """
        try:
            decoded = jwt.decode(token, cls.secret_key, algorithms=[cls.algorithm])
            return decoded["sub"]
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="The token has expired.",
            )
        except InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="The token is invalid."
            )
