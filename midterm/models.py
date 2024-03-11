from typing import Annotated
import sqlalchemy
from sqlalchemy import ForeignKey, Table, Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationships, relationship
from database import Base

_id = Annotated[int, mapped_column(Integer, primary_key=True)]

candidates_jobs_association = Table(
    'candidates_jobs',
    Base.metadata,
    Column('candidate_id', Integer, ForeignKey('candidates.id')),
    Column('job_id', Integer, ForeignKey('jobs.id')),
)

candidates_skills_association = Table(
    'candidates_skills',
    Base.metadata,
    Column('candidate_id', Integer, ForeignKey('candidates.id')),
    Column('skill_id', Integer, ForeignKey('skills.id')),
)


jobs_skills_association = Table(
    'jobs_skills',
    Base.metadata,
    Column('skills_id', Integer, ForeignKey('skills.id')),
    Column('job_id', Integer, ForeignKey('jobs.id')),
)


class Employer(Base):
    __tablename__ = 'employers'

    id: Mapped[_id]
    name: Mapped[str]
    location: Mapped[str]

    jobs: Mapped[list['Job']] = relationship(back_populates='employer')


class Candidate(Base):
    __tablename__ = 'candidates'

    id: Mapped[_id]
    name: Mapped[str]
    location: Mapped[str]
    education: Mapped[str]
    years_of_experience: Mapped[int]

    jobs: Mapped[list['Job']] = relationship(secondary=candidates_jobs_association, back_populates='candidates')
    skills: Mapped[list['Skill']] = relationship(secondary=candidates_skills_association, back_populates='candidates')


class Job(Base):
    __tablename__ = 'jobs'

    id: Mapped[_id]
    title: Mapped[str]
    location: Mapped[str]
    salary:  Mapped[float]
    time:  Mapped[str]
    year_of_experience: Mapped[int]
    employer_id: Mapped[int] = mapped_column(ForeignKey('employers.id'))

    employer: Mapped['Employer'] = relationship(back_populates='jobs')
    skills: Mapped[list['Skill']] = relationship(secondary=jobs_skills_association, back_populates='jobs')
    candidates: Mapped[list['Candidate']] = relationship(secondary=candidates_jobs_association, back_populates='jobs')


class Skill(Base):
    __tablename__ = 'skills'

    id: Mapped[_id]
    title: Mapped[str] = mapped_column(String, unique=True)

    jobs: Mapped[list['Job']] = relationship(secondary=jobs_skills_association, back_populates='skills')
    candidates: Mapped[list['Candidate']] = relationship(secondary=candidates_skills_association, back_populates='skills')

