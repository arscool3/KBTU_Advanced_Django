"""Initial

Revision ID: d91df05b4fb7
Revises: 
Create Date: 2024-03-12 13:33:21.038838

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd91df05b4fb7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('candidates',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('employers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('location', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('skills',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_table('jobs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('location', sa.String(), nullable=False),
    sa.Column('salary', sa.Float(), nullable=False),
    sa.Column('time', sa.String(), nullable=False),
    sa.Column('years_of_experience', sa.Integer(), nullable=False),
    sa.Column('employer_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['employer_id'], ['employers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('resumes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('candidate_id', sa.Integer(), nullable=False),
    sa.Column('location', sa.String(), nullable=False),
    sa.Column('education', sa.String(), nullable=False),
    sa.Column('years_of_experience', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['candidate_id'], ['candidates.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('applications',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('candidate_id', sa.Integer(), nullable=False),
    sa.Column('job_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('status', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['candidate_id'], ['candidates.id'], ),
    sa.ForeignKeyConstraint(['job_id'], ['jobs.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('jobs_skills',
    sa.Column('skills_id', sa.Integer(), nullable=True),
    sa.Column('job_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['job_id'], ['jobs.id'], ),
    sa.ForeignKeyConstraint(['skills_id'], ['skills.id'], )
    )
    op.create_table('resume_skills',
    sa.Column('resume_id', sa.Integer(), nullable=True),
    sa.Column('skill_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['resume_id'], ['resumes.id'], ),
    sa.ForeignKeyConstraint(['skill_id'], ['skills.id'], )
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('resume_skills')
    op.drop_table('jobs_skills')
    op.drop_table('applications')
    op.drop_table('resumes')
    op.drop_table('jobs')
    op.drop_table('skills')
    op.drop_table('employers')
    op.drop_table('candidates')
    # ### end Alembic commands ###
