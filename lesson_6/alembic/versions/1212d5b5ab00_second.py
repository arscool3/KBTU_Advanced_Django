"""second

Revision ID: 1212d5b5ab00
Revises: cdd8d05dd014
Create Date: 2024-03-01 21:40:41.999288

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1212d5b5ab00'
down_revision: Union[str, None] = 'cdd8d05dd014'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('items_user_id_fkey', 'items', type_='foreignkey')
    op.drop_column('items', 'user_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('items', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('items_user_id_fkey', 'items', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###