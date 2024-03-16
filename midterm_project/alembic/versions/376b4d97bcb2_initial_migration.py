"""initial_migration

Revision ID: 376b4d97bcb2
Revises: 
Create Date: 2024-03-16 00:48:18.318471

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '376b4d97bcb2'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('email', sa.String, nullable=False, unique=True),
        sa.Column('phone_number', sa.String, nullable=False, unique=True)
    )

    op.create_table(
        'accounts',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('account_number', sa.String, nullable=False, unique=True),
        sa.Column('account_type', sa.String, nullable=False),
        sa.Column('balance', sa.Float, nullable=False)
    )

    op.create_table(
        'transactions',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('account_id', sa.Integer, sa.ForeignKey('accounts.id'), nullable=False),
        sa.Column('transaction_type', sa.String, nullable=False),
        sa.Column('amount', sa.Float, nullable=False),
        sa.Column('timestamp', sa.DateTime, nullable=False),
        sa.Column('source', sa.String, nullable=False),
        sa.Column('destination', sa.String, nullable=False)
    )

    op.create_table(
        'loans',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('loan_amount', sa.Float, nullable=False),
        sa.Column('interest_rate', sa.Float, nullable=False),
        sa.Column('start_date', sa.DateTime, nullable=False),
        sa.Column('term', sa.Integer, nullable=False),
        sa.Column('purpose', sa.String, nullable=False),
        sa.Column('late_fee', sa.Float, nullable=False)
    )

    op.create_table(
        'payments',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('loan_id', sa.Integer, sa.ForeignKey('loans.id'), nullable=False),
        sa.Column('payment_amount', sa.Float, nullable=False),
        sa.Column('payment_date', sa.DateTime, nullable=False)
    )

    op.create_table(
        'securities',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('username', sa.String, nullable=False, unique=True),
        sa.Column('password', sa.String, nullable=False)
    )


def downgrade() -> None:
    op.drop_table('securities')
    op.drop_table('payments')
    op.drop_table('loans')
    op.drop_table('transactions')
    op.drop_table('accounts')
    op.drop_table('users')
