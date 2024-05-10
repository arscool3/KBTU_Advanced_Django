from typing import List, Optional
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    email: str

    class Config:
        orm_mode = True

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int

    class Config:
        orm_mode = True

class PriorityBase(BaseModel):
    level: int
    name: str

class PriorityCreate(PriorityBase):
    pass

class Priority(PriorityBase):
    id: int

    class Config:
        orm_mode = True

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    category_id: Optional[int] = None
    priority_id: Optional[int] = None

class TaskCreate(TaskBase):
    pass

# Схема задачи для ответа (выходные данные)
class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    is_completed: bool

    class Config:
        orm_mode = True

class Task(TaskBase):
    id: int

    class Config:
        orm_mode = True

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class TaskAuditBase(BaseModel):
    action: str
    timestamp: datetime
    performed_by: int

class TaskAuditCreate(TaskAuditBase):
    task_id: int

class TaskAudit(TaskAuditBase):
    id: int
    task_id: int

    class Config:
        orm_mode = True

class TaskHistoryBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None
    timestamp: datetime

class TaskHistoryCreate(TaskHistoryBase):
    task_id: int

class TaskHistory(TaskHistoryBase):
    id: int
    task_id: int

    class Config:
        orm_mode = True
