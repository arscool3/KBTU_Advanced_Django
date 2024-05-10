"""orderChange2

Revision ID: debc44a64685
Revises: 450d40d77420
Create Date: 2024-05-10 02:00:18.017690

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'debc44a64685'
down_revision: Union[str, None] = '450d40d77420'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('total_amount', sa.Float(), nullable=True))
    op.add_column('orders', sa.Column('status', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('orders', 'status')
    op.drop_column('orders', 'total_amount')
    # ### end Alembic commands ###