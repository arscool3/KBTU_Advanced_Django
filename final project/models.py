from datetime import datetime
from typing import List, Annotated, Optional

import sqlalchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
_id = Annotated[int, mapped_column(sqlalchemy.INTEGER, primary_key=True)]


class User(Base):
    __tablename__ = 'users'
    id: Mapped[_id]
    username: Mapped[str]
    complaints = relationship('UserComplaint', back_populates='user')


class UserComplaint(Base):
    __tablename__ = 'user_complaints'
    id: Mapped[_id]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    project_id: Mapped[int] = mapped_column(ForeignKey('projects.id'))
    user = relationship(User, back_populates='complaints')
    description: Mapped[str]


class Project(Base):
    __tablename__ = 'projects'
    id: Mapped[_id]
    organization_id: Mapped[int] = mapped_column(ForeignKey('organizations.id'))
    organization = relationship('Organization', back_populates='projects')
    investor_id: Mapped[int] = mapped_column(ForeignKey('investors.id'))
    investor = relationship('Investor', back_populates='projects')
    initial_budget: Mapped[float]
    current_budget: Mapped[float]
    start_date: Mapped[datetime]
    promised_end_date: Mapped[datetime]
    real_end_date: Mapped[Optional[datetime]]
    is_finished: Mapped[bool]
    states = relationship('State', back_populates='project')

class ITProject(Base):
    __tablename__ = 'it_projects'
    id: Mapped[_id]
    investor_id: Mapped[int] = mapped_column(ForeignKey('investors.id'))
    initial_budget: Mapped[float]


class Organization(Base):
    __tablename__ = 'organizations'
    id: Mapped[_id]
    name: Mapped[str]
    projects = relationship('Project', back_populates='organization')
    num_of_finished_projects: Mapped[int]


class Investor(Base):
    __tablename__ = 'investors'
    id: Mapped[_id]
    name: Mapped[str]
    projects = relationship('Project', back_populates='investor')


class State(Base):
    __tablename__ = 'states'
    id: Mapped[_id]
    project_id: Mapped[int] = mapped_column(ForeignKey('projects.id'))
    project = relationship('Project', back_populates='states')
    created_at: Mapped[datetime] = datetime.now()
    last_total_spent_money: Mapped[float]
    report: Mapped[str]
    future_plan: Mapped[str]


class Log(Base):
    __tablename__ = "logs"
    id: Mapped[_id]
    created_at: Mapped[datetime]
    data = Mapped[str]
    method: Mapped[str]
    request: Mapped[str]

