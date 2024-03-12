from datetime import date
from typing import Optional, List

from pydantic import BaseModel


class BaseUser(BaseModel):
    name: str

    class Config:
        from_attributes = True


class User(BaseUser):
    id: int

    @classmethod
    def model_validate(cls, db_instance):
        if db_instance:
            return cls(**db_instance.__dict__)


class CreateUser(BaseUser):
    pass

class UpdateUser(BaseUser):
    pass

class BaseProject(BaseModel):
    name: str
    created_at: date

    class Config:
        from_attributes = True

class CreateProject(BaseProject):
    pass

class UpdateProject(BaseProject):
    pass

class ProjectSchema(BaseProject):
    id: int
    user_id: int
    tasks: Optional[List['TaskSchema']]

    @classmethod
    def model_validate(cls, db_instance):
        if db_instance:
            return cls(**db_instance.__dict__)


class BaseTask(BaseModel):
    name: str

    class Config:
        from_attributes = True

class CreateTask(BaseTask):
    pass

class UpdateTask(BaseTask):
    pass

class TaskSchema(BaseTask):
    id: int
    project: ProjectSchema
    user: User

    @classmethod
    def model_validate(cls, db_instance):
        if db_instance:
            return cls(**db_instance.__dict__)

class BaseTaskStatus(BaseModel):
    name: str

    class Config:
        from_attributes = True

class CreateTaskStatus(BaseTaskStatus):
    pass

class TaskStatusSchema(BaseTaskStatus):
    id: int
    task_id: int


class BaseReport(BaseModel):
    name: str

    class Config:
        from_attributes = True

class CreateReport(BaseReport):
    pass

class UpdateReport(BaseReport):
    pass

class Report(BaseReport):
    id: int

    @classmethod
    def model_validate(cls, db_instance):
        if db_instance:
            return cls(**db_instance.__dict__)

class BaseTaskAssignment(BaseModel):
    name: str

    class Config:
        from_attributes = True

class CreateTaskAssignment(BaseTaskAssignment):
    pass

class TaskAssignment(BaseTaskAssignment):
    id: int

    @classmethod
    def model_validate(cls, db_instance):
        if db_instance:
            return cls(**db_instance.__dict__)

