from core.logger import setup_logger

logger = setup_logger("content_services", log_level="DEBUG", log_file="services.log")

from .anime_service import fetch_anime
from .game_service import fetch_game, get_steam_online
from .movie_series_service import fetch_movie, fetch_series
from .user_service import (
    register_user,
    update_user_profile,
    delete_user_profile,
    authenticate_user,
    get_current_user,
)

__all__ = (
    "fetch_anime",
    "fetch_game",
    "get_steam_online",
    "fetch_movie",
    "fetch_series",
    "register_user",
    "update_user_profile",
    "delete_user_profile",
    "authenticate_user",
    "get_current_user",
)
