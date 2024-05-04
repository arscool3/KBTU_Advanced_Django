"""second

Revision ID: e0903057d75e
Revises: 9e8cccb0e78b
Create Date: 2024-04-12 19:59:58.824987

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e0903057d75e'
down_revision: Union[str, None] = '9e8cccb0e78b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
