from typing import Annotated
from datetime import date

import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Table, Column, Integer, ForeignKey
from database import Base

_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]

class User(Base):
    __tablename__ = 'users'

    id: Mapped[_id]
    name: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
    courses = relationship('Course', secondary='user_courses', back_populates='users')
    purchases: Mapped[list['Purchase']] = relationship('Purchase', back_populates='user')
    progress: Mapped[list['Progress']] = relationship('Progress', back_populates='user')

class Course(Base):
    __tablename__ = 'courses'

    id: Mapped[_id]
    title: Mapped[str]
    description: Mapped[str]
    price: Mapped[float]
    users = relationship('User', secondary='user_courses', back_populates='courses')
    videos: Mapped[list['Video']] = relationship('Video', back_populates='course')
    reviews: Mapped[list['Review']] = relationship('Review', back_populates='course')
    purchases: Mapped[list['Purchase']] = relationship('Purchase', back_populates='course')

class Video(Base):
    __tablename__ = 'videos'

    id: Mapped[_id]
    title: Mapped[str]
    url: Mapped[str]
    course_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('courses.id'))
    course: Mapped[Course] = relationship('Course', back_populates='videos')

class Review(Base):
    __tablename__ = 'reviews'

    id: Mapped[_id]
    content: Mapped[str]
    user_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('users.id'))
    course_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('courses.id'))
    course: Mapped[Course] = relationship('Course', back_populates='reviews')

class Progress(Base):
    __tablename__ = 'progress'

    id: Mapped[_id]
    completion_percentage: Mapped[float]
    user_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('users.id'))
    course_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('courses.id'))
    user: Mapped[User] = relationship('User', back_populates='progress')

class Purchase(Base):
    __tablename__ = 'purchases'

    id: Mapped[_id]
    user_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('users.id'))
    course_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('courses.id'))
    purchase_date: Mapped[date]

    user: Mapped[User] = relationship('User', back_populates='purchases')
    course: Mapped[Course] = relationship('Course', back_populates='purchases')


user_courses = Table('user_courses', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('course_id', Integer, ForeignKey('courses.id'), primary_key=True)
)


