"""second

Revision ID: 546e09e6bb1b
Revises: e0903057d75e
Create Date: 2024-04-13 12:47:57.026305

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '546e09e6bb1b'
down_revision: Union[str, None] = 'e0903057d75e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
