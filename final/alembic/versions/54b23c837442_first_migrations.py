"""first migrations

Revision ID: 54b23c837442
Revises: 1f9ffb2054c0
Create Date: 2024-05-04 10:51:57.444928

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '54b23c837442'
down_revision: Union[str, None] = '1f9ffb2054c0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
