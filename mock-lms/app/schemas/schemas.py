from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


# User
class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    is_admin: bool

    class Config:
        from_attributes = True


# Course
class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None


class CourseCreate(CourseBase):
    pass


class Course(CourseBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    creator_id: int

    class Config:
        from_attributes = True


# Module
class ModuleBase(BaseModel):
    title: str
    description: Optional[str] = None


class ModuleCreate(ModuleBase):
    course_id: int


class Module(ModuleBase):
    id: int
    course_id: int

    class Config:
        from_attributes = True


# Lesson
class LessonBase(BaseModel):
    title: str
    content: str
    video_url: Optional[str] = None
    order: int


class LessonCreate(LessonBase):
    module_id: int
    start_time: datetime


class LessonUpdate(LessonBase):
    module_id: Optional[int] = None
    start_time: Optional[datetime] = None


class LessonInDB(LessonBase):
    id: int
    module_id: int
    start_time: datetime

    class Config:
        from_attributes = True


# Enrollment
class EnrollmentBase(BaseModel):
    user_id: int
    course_id: int
    status: Optional[str] = "active"


class EnrollmentCreate(EnrollmentBase):
    pass


class Enrollment(EnrollmentBase):
    id: int
    enrolled_at: datetime

    class Config:
        from_attributes = True


# Comment
class CommentBase(BaseModel):
    content: str
    user_id: int
    course_id: Optional[int] = None
    lesson_id: Optional[int] = None


class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
