from datetime import datetime
from typing import Annotated
import sqlalchemy
from sqlalchemy import ForeignKey, Table, Column, Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationships, relationship
from database import Base

_id = Annotated[int, mapped_column(Integer, primary_key=True)]


resume_skills_association = Table(
    'resume_skills',
    Base.metadata,
    Column('resume_id', Integer, ForeignKey('resumes.id')),
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
    age: Mapped[int]

    applications: Mapped[list['Application']] = relationship(back_populates='candidate')
    resumes: Mapped[list['Resume']] = relationship(back_populates='candidate')


class Job(Base):
    __tablename__ = 'jobs'

    id: Mapped[_id]
    title: Mapped[str]
    location: Mapped[str]
    salary:  Mapped[float]
    time:  Mapped[str]
    years_of_experience: Mapped[int]
    employer_id: Mapped[int] = mapped_column(ForeignKey('employers.id'))

    employer: Mapped['Employer'] = relationship(back_populates='jobs')
    skills: Mapped[list['Skill']] = relationship(secondary=jobs_skills_association, back_populates='jobs')
    applications: Mapped[list['Application']] = relationship(back_populates='job')


class Skill(Base):
    __tablename__ = 'skills'

    id: Mapped[_id]
    title: Mapped[str] = mapped_column(String, unique=True)

    jobs: Mapped[list['Job']] = relationship(secondary=jobs_skills_association, back_populates='skills')
    resumes: Mapped[list['Resume']] = relationship(secondary=resume_skills_association, back_populates='skills')


class Application(Base):
    __tablename__ = 'applications'

    id: Mapped[_id]
    candidate_id: Mapped[int] = mapped_column(ForeignKey('candidates.id'))
    job_id: Mapped[int] = mapped_column(ForeignKey('jobs.id'))
    resume_id: Mapped[int] = mapped_column(ForeignKey('resumes.id'))
    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    status: Mapped[str] = mapped_column(String, default='Submitted')

    candidate: Mapped['Candidate'] = relationship(back_populates='applications')
    job: Mapped['Job'] = relationship(back_populates='applications')
    resume: Mapped['Resume'] = relationship(back_populates='applications')


class Resume(Base):
    __tablename__ = 'resumes'

    id: Mapped[_id]
    title: Mapped[str]
    candidate_id: Mapped[int] = mapped_column(ForeignKey('candidates.id'))
    location: Mapped[str]
    education: Mapped[str]
    years_of_experience: Mapped[int]

    skills: Mapped[list['Skill']] = relationship(secondary=resume_skills_association, back_populates='resumes')
    applications: Mapped[list['Application']] = relationship(back_populates='resume')
    candidate: Mapped['Candidate'] = relationship(back_populates='resumes')

