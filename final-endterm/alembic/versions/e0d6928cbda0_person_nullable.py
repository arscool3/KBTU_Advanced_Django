"""person nullable

Revision ID: e0d6928cbda0
Revises: 21fb22756a7b
Create Date: 2024-04-29 15:44:09.359764

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e0d6928cbda0'
down_revision: Union[str, None] = '21fb22756a7b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('people', 'current_location_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('people', 'current_road_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('people', 'current_speed',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('people', 'current_speed',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('people', 'current_road_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('people', 'current_location_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###