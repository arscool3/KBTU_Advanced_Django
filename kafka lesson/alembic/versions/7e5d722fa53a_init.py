"""init

Revision ID: 7e5d722fa53a
Revises: 733ebba01791
Create Date: 2024-03-30 17:56:19.722321

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7e5d722fa53a'
down_revision: Union[str, None] = '733ebba01791'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
