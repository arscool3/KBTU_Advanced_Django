"""init

Revision ID: c04675f0e0be
Revises: 
Create Date: 2024-04-09 23:44:41.468208

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c04675f0e0be'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('crypto_trade',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('sold_currency', sa.String(), nullable=False),
    sa.Column('purchase_currency', sa.String(), nullable=False),
    sa.Column('k_to_usd', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('crypto_trade')
    # ### end Alembic commands ###
