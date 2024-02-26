"""create table

Revision ID: 981db188c5b2
Revises: 
Create Date: 2024-02-24 00:39:43.891386

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '981db188c5b2'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('students',
                    sa.Column('id', sa.INTEGER(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('age', sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('teachers',
                    sa.Column('id', sa.INTEGER(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('yoe', sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade() -> None:
    pass
