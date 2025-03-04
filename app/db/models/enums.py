from enum import Enum


class ContentType(str, Enum):
    """Enum representing different types of content.

    <h2>Values:</h2>
        **ANIME**: Represents an anime.
        **GAME**: Represents a game.
        **MOVIE**: Represents a movie.
        **SERIES**: Represents a series.
    """

    ANIME = "ANIME"
    GAME = "GAME"
    MOVIE = "MOVIE"
    SERIES = "SERIES"


class Status(str, Enum):
    """Enum representing the status of content in a user's queue.

    <h2>Values:</h2>
        **FINISHED**: The content has been completed.
        **IN_PROGRESS**: The content is currently being watched/played.
        **DROPPED**: The content has been abandoned.
        **PLANNED**: The content is planned to be watched/played in the future.
    """

    FINISHED = "FINISHED"
    IN_PROGRESS = "IN_PROGRESS"
    DROPPED = "DROPPED"
    PLANNED = "PLANNED"


class AgeRating(str, Enum):
    """Enum representing age ratings for content.

    <h2>Values:</h2>
        **G**: General audiences.
        **PG**: Parental guidance suggested.
        **PG13**: Parents strongly cautioned, some content may be inappropriate for children under 13.
        **R**: Restricted, viewers under 17 require accompanying parent or guardian.
        **NC17**: No one 17 and under admitted.
    """

    G = "G"
    PG = "PG"
    PG13 = "PG-13"
    R = "R"
    NC17 = "NC-17"


class Platforms(str, Enum):
    """Represents a game's platform.

    <h2>Values:</h2>
        **PC**: Represents a PC game.
        **LINUX**: Represents a Linux game.
        **MACOS**: Represents a Mac OS X game.
        **PSP**: Represents a Sony PlayStation Portable game.
        **PS3**: Represents a PlayStation 3 game.
        **PS4**: Represents a PlayStation 4 game.
        **PS5**: Represents a PlayStation 5 game.
        **XBOX_360**: Represents a Xbox 360 game.
        **XBOX_ONE**: Represents a Xbox One game.
        **XBOX_SERIES_SX**: Represents a Xbox Series S/X game.
        **NINTENDO_SWITCH**: Represents a Nintendo Switch game.
        **IOS**: Represents an iOS game.
        **ANDROID**: Represents an Android game.
        **WEB**: Represents a web-based game.
    """

    PC = "PC"
    LINUX = "LINUX"
    MACOS = "MACOS"
    PSP = "PSP"
    PS3 = "PS3"
    PS4 = "PS4"
    PS5 = "PS5"
    XBOX_360 = "XBOX 360"
    XBOX_ONE = "XBOX ONE"
    XBOX_SERIES_SX = "XBOX SERIES S/X"
    NINTENDO_SWITCH = "NINTENDO SWITCH"
    IOS = "IOS"
    ANDROID = "ANDROID"
    WEB = "WEB"
