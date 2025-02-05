"""first commit

Revision ID: f37da9332969
Revises: 
Create Date: 2025-02-05 21:50:07.958199

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f37da9332969"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "animes",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("translated_title", sa.String(length=100), nullable=True),
        sa.Column("episodes", sa.SmallInteger(), nullable=True),
        sa.Column("is_ongoing", sa.Boolean(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("rating", sa.Numeric(precision=3, scale=1), nullable=True),
        sa.Column("popularity", sa.SmallInteger(), nullable=True),
        sa.Column("image_url", sa.String(length=100), nullable=True),
        sa.Column(
            "age_restriction",
            sa.Enum("G", "PG", "PG13", "R", "NC17", name="agerestriction"),
            nullable=True,
        ),
        sa.Column("studios", sa.ARRAY(sa.String(length=100)), nullable=True),
        sa.Column("release_date", sa.Date(), nullable=True),
        sa.CheckConstraint("rating >= 0 AND rating <= 10", name="check_rating_range"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_animes_title"), "animes", ["title"], unique=False)
    op.create_table(
        "games",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "available_platforms",
            sa.ARRAY(
                sa.Enum(
                    "PC",
                    "PS3",
                    "PS4",
                    "PS5",
                    "XBOX_360",
                    "XBOX_ONE",
                    "XBOX_SERIES_X",
                    "NINTENDO_SWITCH",
                    "IOS",
                    "ANDROID",
                    "WEB",
                    name="platforms",
                )
            ),
            nullable=False,
        ),
        sa.Column("playtime", sa.SmallInteger(), nullable=True),
        sa.Column("stores", sa.ARRAY(sa.String(length=50)), nullable=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("rating", sa.Numeric(precision=3, scale=1), nullable=True),
        sa.Column("popularity", sa.SmallInteger(), nullable=True),
        sa.Column("image_url", sa.String(length=100), nullable=True),
        sa.Column(
            "age_restriction",
            sa.Enum("G", "PG", "PG13", "R", "NC17", name="agerestriction"),
            nullable=True,
        ),
        sa.Column("studios", sa.ARRAY(sa.String(length=100)), nullable=True),
        sa.Column("release_date", sa.Date(), nullable=True),
        sa.CheckConstraint("rating >= 0 AND rating <= 10", name="check_rating_range"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_games_title"), "games", ["title"], unique=False)
    op.create_table(
        "genres",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_genres_name"), "genres", ["name"], unique=False)
    op.create_table(
        "movies",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("duration", sa.SmallInteger(), nullable=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("rating", sa.Numeric(precision=3, scale=1), nullable=True),
        sa.Column("popularity", sa.SmallInteger(), nullable=True),
        sa.Column("image_url", sa.String(length=100), nullable=True),
        sa.Column(
            "age_restriction",
            sa.Enum("G", "PG", "PG13", "R", "NC17", name="agerestriction"),
            nullable=True,
        ),
        sa.Column("studios", sa.ARRAY(sa.String(length=100)), nullable=True),
        sa.Column("release_date", sa.Date(), nullable=True),
        sa.CheckConstraint("rating >= 0 AND rating <= 10", name="check_rating_range"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_movies_title"), "movies", ["title"], unique=False)
    op.create_table(
        "series",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("episode_duration", sa.SmallInteger(), nullable=True),
        sa.Column("episodes", sa.SmallInteger(), nullable=True),
        sa.Column("is_ongoing", sa.Boolean(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("rating", sa.Numeric(precision=3, scale=1), nullable=True),
        sa.Column("popularity", sa.SmallInteger(), nullable=True),
        sa.Column("image_url", sa.String(length=100), nullable=True),
        sa.Column(
            "age_restriction",
            sa.Enum("G", "PG", "PG13", "R", "NC17", name="agerestriction"),
            nullable=True,
        ),
        sa.Column("studios", sa.ARRAY(sa.String(length=100)), nullable=True),
        sa.Column("release_date", sa.Date(), nullable=True),
        sa.CheckConstraint("rating >= 0 AND rating <= 10", name="check_rating_range"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_series_title"), "series", ["title"], unique=False)
    op.create_table(
        "tags",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_tags_name"), "tags", ["name"], unique=False)
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("username", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=False),
        sa.Column("hashed_password", sa.String(length=100), nullable=False),
        sa.Column("avatar", sa.String(length=100), nullable=True),
        sa.Column("creation_date", sa.Date(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_username"), "users", ["username"], unique=True)
    op.create_table(
        "anime_genre_link",
        sa.Column("anime_id", sa.Integer(), nullable=False),
        sa.Column("genre_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["anime_id"],
            ["animes.id"],
        ),
        sa.ForeignKeyConstraint(
            ["genre_id"],
            ["genres.id"],
        ),
        sa.PrimaryKeyConstraint("anime_id", "genre_id"),
    )
    op.create_table(
        "anime_tag_link",
        sa.Column("anime_id", sa.Integer(), nullable=False),
        sa.Column("tag_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["anime_id"],
            ["animes.id"],
        ),
        sa.ForeignKeyConstraint(
            ["tag_id"],
            ["tags.id"],
        ),
        sa.PrimaryKeyConstraint("anime_id", "tag_id"),
    )
    op.create_table(
        "game_genre_link",
        sa.Column("game_id", sa.Integer(), nullable=False),
        sa.Column("genre_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["game_id"],
            ["games.id"],
        ),
        sa.ForeignKeyConstraint(
            ["genre_id"],
            ["genres.id"],
        ),
        sa.PrimaryKeyConstraint("game_id", "genre_id"),
    )
    op.create_table(
        "game_tag_link",
        sa.Column("game_id", sa.Integer(), nullable=False),
        sa.Column("tag_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["game_id"],
            ["games.id"],
        ),
        sa.ForeignKeyConstraint(
            ["tag_id"],
            ["tags.id"],
        ),
        sa.PrimaryKeyConstraint("game_id", "tag_id"),
    )
    op.create_table(
        "movie_genre_link",
        sa.Column("movie_id", sa.Integer(), nullable=False),
        sa.Column("genre_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["genre_id"],
            ["genres.id"],
        ),
        sa.ForeignKeyConstraint(
            ["movie_id"],
            ["movies.id"],
        ),
        sa.PrimaryKeyConstraint("movie_id", "genre_id"),
    )
    op.create_table(
        "series_genre_link",
        sa.Column("series_id", sa.Integer(), nullable=False),
        sa.Column("genre_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["genre_id"],
            ["genres.id"],
        ),
        sa.ForeignKeyConstraint(
            ["series_id"],
            ["series.id"],
        ),
        sa.PrimaryKeyConstraint("series_id", "genre_id"),
    )
    op.create_table(
        "users_queues",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column(
            "content_type",
            sa.Enum("ANIME", "GAME", "MOVIE", "SERIES", name="contenttype"),
            nullable=False,
        ),
        sa.Column("content_id", sa.Integer(), nullable=False),
        sa.Column("user_rating", sa.SmallInteger(), nullable=True),
        sa.Column("comment", sa.Text(), nullable=True),
        sa.Column("favorite", sa.Boolean(), nullable=False),
        sa.Column(
            "status",
            sa.Enum("FINISHED", "IN_PROGRESS", "DROPPED", "PLANNED", name="status"),
            nullable=False,
        ),
        sa.Column("priority", sa.SmallInteger(), nullable=False),
        sa.Column("creation_date", sa.Date(), nullable=False),
        sa.CheckConstraint(
            "priority >= 0 AND priority <= 3", name="check_priority_range"
        ),
        sa.CheckConstraint(
            "user_rating >= 0 AND user_rating <= 10", name="check_user_rating_range"
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("users_queues")
    op.drop_table("series_genre_link")
    op.drop_table("movie_genre_link")
    op.drop_table("game_tag_link")
    op.drop_table("game_genre_link")
    op.drop_table("anime_tag_link")
    op.drop_table("anime_genre_link")
    op.drop_index(op.f("ix_users_username"), table_name="users")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
    op.drop_index(op.f("ix_tags_name"), table_name="tags")
    op.drop_table("tags")
    op.drop_index(op.f("ix_series_title"), table_name="series")
    op.drop_table("series")
    op.drop_index(op.f("ix_movies_title"), table_name="movies")
    op.drop_table("movies")
    op.drop_index(op.f("ix_genres_name"), table_name="genres")
    op.drop_table("genres")
    op.drop_index(op.f("ix_games_title"), table_name="games")
    op.drop_table("games")
    op.drop_index(op.f("ix_animes_title"), table_name="animes")
    op.drop_table("animes")
    op.execute("drop type platforms, contenttype, status, agerestriction;")
    # ### end Alembic commands ###
