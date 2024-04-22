from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Text, LargeBinary
from sqlalchemy.orm import relationship, configure_mappers
from sqlalchemy.sql import func
from ..database.database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(150), unique=True, index=True)
    email = Column(String(150), unique=True, index=True)
    hashed_password = Column(LargeBinary)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    enrollments = relationship("Enrollment", backref="user", cascade="all, delete-orphan", lazy='select')
    comments = relationship("Comment", backref="user", cascade="all, delete-orphan", lazy='select')


class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    creator_id = Column(Integer, ForeignKey('users.id'), index=True)
    modules = relationship("Module", backref="course", cascade="all, delete-orphan", lazy='select')
    comments = relationship("Comment", backref="course", cascade="all, delete-orphan", lazy='select')
    enrollments = relationship("Enrollment", backref="course", cascade="all, delete-orphan", lazy='select')


class Module(Base):
    __tablename__ = 'modules'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    description = Column(Text)
    course_id = Column(Integer, ForeignKey('courses.id'), index=True)
    lessons = relationship("Lesson", backref="module", cascade="all, delete-orphan", lazy='select')


class Lesson(Base):
    __tablename__ = 'lessons'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    content = Column(Text)
    video_url = Column(String(500), nullable=True)
    module_id = Column(Integer, ForeignKey('modules.id'))
    order = Column(Integer)
    start_time = Column(DateTime)


class Enrollment(Base):
    __tablename__ = 'enrollments'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    course_id = Column(Integer, ForeignKey('courses.id'), index=True)
    enrolled_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String(50), default='active')


class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    course_id = Column(Integer, ForeignKey('courses.id'), index=True, nullable=True)
    lesson_id = Column(Integer, ForeignKey('lessons.id'), index=True, nullable=True)

