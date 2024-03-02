"""initial_migration

Revision ID: acb5d6863dd9
Revises: 
Create Date: 2024-03-02 15:39:02.017709

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'acb5d6863dd9'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'directors',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('name', sa.String(), nullable=False)
    )

    op.create_table(
        'genres',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('name', sa.String(), nullable=False)
    )

    op.create_table(
        'studios',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('name', sa.String(), nullable=False)
    )

    op.create_table(
        'movies',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('release_date', sa.Date(), nullable=False),
        sa.Column('rating', sa.Integer(), nullable=True),
        sa.Column('director_id', sa.Integer(), sa.ForeignKey('directors.id')),
        sa.Column('genre_id', sa.Integer(), sa.ForeignKey('genres.id')),
        sa.Column('studio_id', sa.Integer(), sa.ForeignKey('studios.id'))
    )


def downgrade() -> None:
    op.drop_table('studios')
    op.drop_table('genres')
    op.drop_table('directors')
    op.drop_table('movies')
