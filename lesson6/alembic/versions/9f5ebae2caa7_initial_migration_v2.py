"""initial_migration v2

Revision ID: 9f5ebae2caa7
Revises: 226aec5a468f
Create Date: 2024-03-01 20:46:22.748926

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9f5ebae2caa7'
down_revision: Union[str, None] = '226aec5a468f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
