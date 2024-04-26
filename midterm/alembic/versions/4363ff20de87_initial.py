"""initial

Revision ID: 4363ff20de87
Revises: 
Create Date: 2024-03-09 16:20:16.382264

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4363ff20de87'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('insurances',
    sa.Column('insurance_amount', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('locations',
    sa.Column('latitude', sa.Float(), nullable=False),
    sa.Column('longitude', sa.Float(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('marks',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('people',
    sa.Column('iin', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('surname', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('iin')
    )
    op.create_table('insurance_person',
    sa.Column('insurance_id', sa.Integer(), nullable=True),
    sa.Column('person_id', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['insurance_id'], ['insurances.id'], ),
    sa.ForeignKeyConstraint(['person_id'], ['people.iin'], )
    )
    op.create_table('vehicles',
    sa.Column('mark', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('owner_id', sa.String(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['mark'], ['marks.id'], ),
    sa.ForeignKeyConstraint(['owner_id'], ['people.iin'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('fines',
    sa.Column('fined_person_id', sa.String(), nullable=False),
    sa.Column('fined_vehicle_id', sa.Integer(), nullable=False),
    sa.Column('fine_amount', sa.Integer(), nullable=False),
    sa.Column('location_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['fined_person_id'], ['people.iin'], ),
    sa.ForeignKeyConstraint(['fined_vehicle_id'], ['vehicles.id'], ),
    sa.ForeignKeyConstraint(['location_id'], ['locations.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('insurance_vehicle',
    sa.Column('insurance_id', sa.Integer(), nullable=True),
    sa.Column('vehicle_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['insurance_id'], ['insurances.id'], ),
    sa.ForeignKeyConstraint(['vehicle_id'], ['vehicles.id'], )
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('insurance_vehicle')
    op.drop_table('fines')
    op.drop_table('vehicles')
    op.drop_table('insurance_person')
    op.drop_table('people')
    op.drop_table('marks')
    op.drop_table('locations')
    op.drop_table('insurances')
    # ### end Alembic commands ###