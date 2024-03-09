from typing import Annotated
import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column, relationships, relationship
from database import Base

_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]


class Employer(Base):
    __tablename__ = 'employers'

    id: Mapped[_id]
    name: Mapped[str]
    location: Mapped[str]

    jobs: Mapped['Job'] = relationship(back_populates="employer")


class Candidate(Base):
    __tablename__ = 'candidates'

    id: Mapped[_id]
    name: Mapped[str]
    location: Mapped[str]
    education: Mapped[str]
    year_of_experience: Mapped[int]

    jobs: Mapped[list['Job']] = relationship(back_populates="candidates")
    skills: Mapped[list['Skill']] = relationship(back_populates="candidates")


class Job(Base):
    __tablename__ = 'jobs'

    id: Mapped[_id]
    title: Mapped[str]
    salary:  Mapped[float]
    time:  Mapped[str]
    year_of_experience: Mapped[int]

    employer: Mapped['Employer'] = relationship(back_populates="jobs")
    skills: Mapped[list['Skill']] = relationship(back_populates="jobs")


class Skill(Base):
    __tablename__ = 'skills'

    id: Mapped[_id]
    title: Mapped[str]

    jobs: Mapped[list['Job']] = relationship(back_populates="skills")
