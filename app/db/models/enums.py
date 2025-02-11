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
    # generate google style docstring
    """Represents a game's platform.

    <h2>Values:</h2>
        **PC**: Play on a PC or laptop.
        **PS3**: Play on the PlayStation 3.
        **PS4**: Play on the PlayStation 4.
        **PS** 5: Play on the PlayStation 5.
        **XBOX** 360: Play on the Xbox 360.
        **XBOX** ONE: Play on the Xbox One.
        **XBOX** SERIES X: Play on the Xbox Series X.
        **NINTENDO** SWITCH: Play on the Nintendo Switch.
        **IOS**: Play on the iOS.
        **ANDROID**: Play on the Android.
        **WEB**: Play on a web browser.
    """

    PC = "PC"
    PS3 = "PS3"
    PS4 = "PS4"
    PS5 = "PS5"
    XBOX_360 = "XBOX 360"
    XBOX_ONE = "XBOX ONE"
    XBOX_SERIES_X = "XBOX SERIES X"
    NINTENDO_SWITCH = "NINTENDO SWITCH"
    IOS = "IOS"
    ANDROID = "ANDROID"
    WEB = "WEB"
