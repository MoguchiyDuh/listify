"""user library link table added

Revision ID: 27122f3d7119
Revises: 42cfc8652fef
Create Date: 2025-02-11 06:47:55.290978

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '27122f3d7119'
down_revision: Union[str, None] = '42cfc8652fef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('library_content_link',
    sa.Column('library_id', sa.Integer(), nullable=False),
    sa.Column('content_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['content_id'], ['content.id'], ),
    sa.ForeignKeyConstraint(['library_id'], ['users_libraries.id'], ),
    sa.PrimaryKeyConstraint('library_id', 'content_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('library_content_link')
    # ### end Alembic commands ###
