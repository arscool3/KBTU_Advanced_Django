"""journal add column method

Revision ID: e0124aa772ee
Revises: 7537da6f23a9
Create Date: 2024-04-25 13:51:51.547380

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e0124aa772ee'
down_revision: Union[str, None] = '7537da6f23a9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('access_logs', sa.Column('method', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('access_logs', 'method')
    # ### end Alembic commands ###
