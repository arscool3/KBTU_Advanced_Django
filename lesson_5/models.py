from typing import Annotated
from datetime import date

import sqlalchemy
from sqlalchemy.orm import Session, relationship, Mapped
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

_id = Annotated[int, sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)]

class Job(Base):
    __tablename__ = 'jobs'

    id: Mapped[_id]
    title: Mapped[str]
    description: Mapped[str]
    company_id: Mapped[int] = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('companies.id'))
    company: Mapped['Company'] = relationship('Company', back_populates='jobs')

class Worker(Base):
    __tablename__ = 'workers'

    id: Mapped[_id]
    name: Mapped[str]
    age: Mapped[int]
    job_id: Mapped[int] = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('jobs.id'))
    job: Mapped[Job] = relationship('Job', back_populates='workers')

class Company(Base):
    __tablename__ = 'companies'

    id: Mapped[_id]
    name: Mapped[str]
    industry: Mapped[str]
    jobs: Mapped[List[Job]] = relationship('Job', back_populates='company')


