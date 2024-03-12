from datetime import date
from typing import Annotated
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, mapped_column, Mapped, relationship

url = 'postgresql://postgres:postgres@localhost:5437/postgres'
engine = create_engine(url)
session = Session(engine)

Base = declarative_base()

_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]


# TODO: Models: User, Project, Task, TaskStatus, Report, TaskAssignment


# TODO: Relations: User -> Project: one-to-many
#            Project -> Task: one-to-many
#            Task -> Project: one-to-one
#            Task -> TaskStatus: one-to-one
#            Task -> User: one-to-one


class User(Base):
    __tablename__ = 'users'

    id: Mapped[_id]
    name: Mapped[str]
    created_at: Mapped[date] = sqlalchemy.Column(sqlalchemy.DATE, default=date.today())
    projects: Mapped['Project'] = relationship('Project', back_populates='user')
    tasks: Mapped['Task'] = relationship('Task', back_populates='user')


class Project(Base):
    __tablename__ = 'projects'

    id: Mapped[_id]
    name: Mapped[str]
    created_at: Mapped[date] = sqlalchemy.Column(sqlalchemy.DATE, default=date.today())
    user_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('users.id'))
    user: Mapped['User'] = relationship('User', back_populates='projects')
    tasks: Mapped['Task'] = relationship('Task', back_populates='project')


class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[_id]
    name: Mapped[str]
    project_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('projects.id'))
    project: Mapped['Project'] = relationship('Project', back_populates='tasks')
    task_status: Mapped['TaskStatus'] = relationship("TaskStatus", uselist=False, back_populates="task")
    user_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('users.id'))
    user: Mapped['User'] = relationship("User", back_populates="tasks")


class TaskStatus(Base):
    __tablename__ = 'task_statuses'

    id: Mapped[_id]
    name: Mapped[str]
    task_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('tasks.id'))
    task: Mapped['Task'] = relationship("Task", back_populates="task_status")


class Report(Base):
    __tablename__ = 'reports'

    id: Mapped[_id]
    name: Mapped[str]


class TaskAssignment(Base):
    __tablename__ = 'task_assignments'

    id: Mapped[_id]
    name: Mapped[str]


# Docker: # a09cfef71b3ef0f60b1944e1b07dab9467707ccf32cf74491096a6cadd18d2f1
