from typing import Annotated, List

import sqlalchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database import Base

_id = Annotated[int, mapped_column(sqlalchemy.INTEGER, primary_key=True)]


class University(Base):
    __tablename__ = 'universities'

    id: Mapped[_id]
    name: Mapped[str]
    students: Mapped[List['Student']] = relationship(back_populates='university')


class Student(Base):
    __tablename__ = 'students'

    id: Mapped[_id]
    name: Mapped[str]
    gpa = sqlalchemy.Column(sqlalchemy.FLOAT, default=1.1)
    age: Mapped[int]
    university_id: Mapped[int] = mapped_column(ForeignKey('universities.id'))
    university: Mapped[University] = relationship(back_populates="students", uselist=False)
