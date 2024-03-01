from datetime import date
from typing import Annotated, List

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship

Base = declarative_base()
_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]


class Principal(Base):
    __tablename__ = 'principals'

    id: Mapped[_id]
    name: Mapped[str]
    university_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('universities.id'))
    university: Mapped['University'] = relationship('University', back_populates='principal')


class University(Base):
    __tablename__ = 'universities'

    id: Mapped[_id]
    name: Mapped[str]
    city: Mapped[str]
    created_at: Mapped[date] = mapped_column(sqlalchemy.Date, default=date.today())
    principal: Mapped[Principal] = relationship('Principal', back_populates='university', uselist=False)
    students: Mapped[List['Student']] = relationship('Student', back_populates='university')
    teachers: Mapped[List['Teacher']] = relationship('Teacher', back_populates='university')


class Student(Base):
    __tablename__ = 'students'

    id: Mapped[_id]
    name: Mapped[str]
    university_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('universities.id'))
    university: Mapped[University] = relationship('University', back_populates='students')


class Teacher(Base):
    __tablename__ = 'teachers'

    id: Mapped[_id]
    name: Mapped[str]
    university_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('universities.id'))
    university: Mapped[University] = relationship('University', back_populates='teachers')
    disciplines: Mapped[List['Discipline']] = relationship('Discipline', back_populates='teacher')


class Discipline(Base):
    __tablename__ = 'disciplines'

    id: Mapped[_id]
    name: Mapped[str]
    teacher_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('teachers.id'))
    teacher: Mapped[Teacher] = relationship('Teacher', back_populates='disciplines')
