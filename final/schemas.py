from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Базовые схемы для всех моделей
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    active: bool
    projects: List['Project'] = []
    tasks: List['Task'] = []
    comments: List['Comment'] = []
    notifications: List['Notification'] = []

    class Config:
        orm_mode = True

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    owner_id: Optional[int] = None

class Project(ProjectBase):
    id: int
    owner_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    tasks: List['Task'] = []

    class Config:
        orm_mode = True

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: str
    priority: str
    deadline: datetime

class TaskCreate(TaskBase):
    project_id: Optional[int] = None
    assignee_id: Optional[int] = None

class Task(TaskBase):
    id: int
    project_id: Optional[int] = None
    assignee_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    comments: List['Comment'] = []

    class Config:
        orm_mode = True

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    task_id: int
    author_id: int

class Comment(CommentBase):
    id: int
    task_id: int
    author_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class NotificationBase(BaseModel):
    title: str
    message: str
    read: bool = False
    event_type: str
    event_id: int

class NotificationCreate(NotificationBase):
    user_id: int

class Notification(NotificationBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class EventBase(BaseModel):
    type: str
    related_id: Optional[int] = None
    related_type: Optional[str] = None
    description: Optional[str] = None

class EventCreate(EventBase):
    pass

class Event(EventBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

# Используем эту строчку для создания forward references
User.update_forward_refs()
Project.update_forward_refs()
Task.update_forward_refs()
Comment.update_forward_refs()
Notification.update_forward_refs()
