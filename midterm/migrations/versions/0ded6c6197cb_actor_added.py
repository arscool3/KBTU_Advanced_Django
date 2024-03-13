"""actor added

Revision ID: 0ded6c6197cb
Revises: 9634efbe9b93
Create Date: 2024-03-13 12:47:15.280331

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0ded6c6197cb'
down_revision: Union[str, None] = '9634efbe9b93'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('actors',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('created_at', sa.DATE(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.alter_column('genres', 'created_at',
               existing_type=sa.DATE(),
               nullable=False,
               existing_server_default=sa.text('now()'))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('genres', 'created_at',
               existing_type=sa.DATE(),
               nullable=True,
               existing_server_default=sa.text('now()'))
    op.drop_table('actors')
    # ### end Alembic commands ###
