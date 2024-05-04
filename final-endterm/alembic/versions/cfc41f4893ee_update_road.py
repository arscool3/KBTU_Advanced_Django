"""update road

Revision ID: cfc41f4893ee
Revises: 6ba4e055fb91
Create Date: 2024-04-28 00:51:57.676155

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cfc41f4893ee'
down_revision: Union[str, None] = '6ba4e055fb91'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('roads', sa.Column('region_id', sa.Integer(), nullable=False))
    op.drop_constraint('roads_region_fkey', 'roads', type_='foreignkey')
    op.create_foreign_key(None, 'roads', 'regions', ['region_id'], ['id'])
    op.drop_column('roads', 'region')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('roads', sa.Column('region', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'roads', type_='foreignkey')
    op.create_foreign_key('roads_region_fkey', 'roads', 'regions', ['region'], ['id'])
    op.drop_column('roads', 'region_id')
    # ### end Alembic commands ###
