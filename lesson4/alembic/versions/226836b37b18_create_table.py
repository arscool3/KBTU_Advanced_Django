"""create table

Revision ID: 226836b37b18
Revises: 
Create Date: 2024-02-23 21:31:49.403793

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '226836b37b18'
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
