# pip install fastapi uvicorn sqlalchemy alembic psycopg2-binary
from datetime import date
from typing import Annotated

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, Mapped, mapped_column, relationship


url = 'postgresql://postgres:aru@localhost/fastapi2'
engine = create_engine(url)
session = Session(engine)

Base = declarative_base()
_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]


#student,faculty,school,university,teacher
"""
class Parent(Base):
    __tablename__ = "parents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)

    children = relationship("Child", back_populates="parent")


class Child(Base):
    __tablename__ = "children"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    parent_id = Column('parent_id', Integer(), ForeignKey('parents.id'), nullable=False)

    parent = relationship("Parent", back_populates="children")
"""
class University(Base):
    __tablename__ = 'universities'
    id: Mapped[_id]
    name: Mapped[str]
    description:Mapped[str]
    school: Mapped['School'] = relationship(back_populates='university')

class School(Base):
    __tablename__ = 'schools'
    id: Mapped[_id]
    name: Mapped[str]
    description:Mapped[str]
    university_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('universities.id'))
    university: Mapped[University] = relationship(back_populates='school' )
    faculty: Mapped['Faculty'] = relationship(back_populates='school')
    
class Faculty(Base):
    __tablename__ = 'faculties'
    id: Mapped[_id]
    name: Mapped[str]
    description:Mapped[str]
    school_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('schools.id'))
    school: Mapped[School] = relationship(back_populates='faculty' )
    student: Mapped['Student'] = relationship(back_populates='faculty')
    teacher:Mapped['Teacher']=relationship(back_populates='faculty')


        
class Student(Base):
    __tablename__='students'
    id:Mapped[_id]
    name:Mapped[str]
    gpa:Mapped[int]
    faculty_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('faculties.id'))
    faculty: Mapped[Faculty] = relationship(back_populates='Student')
class Teacher(Base):
    __tablename__='teachers'
    id:Mapped[_id]
    name:Mapped[str]
    degree:Mapped[str]
    school_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('schools.id'))
    school: Mapped[School] = relationship(back_populates='Teacher' )


