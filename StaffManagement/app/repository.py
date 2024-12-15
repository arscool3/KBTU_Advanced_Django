from abc import ABC, abstractmethod
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm.session import Session

import app.schemas
from app.models import Department, Task, Employee, Schedule

from app.database import Base


class AbcRepository(ABC):
    model: Base = None
    schema: BaseModel = None

    @abstractmethod
    def __init__(self, session: Session):
        raise NotImplementedError()

    @abstractmethod
    def get_list(self):
        raise NotImplementedError()

    @abstractmethod
    def create(self, model: BaseModel):
        raise NotImplementedError()


class BaseRepository(AbcRepository):

    def __init__(self, session: Session):
        self.session = session

    def get_list(self):
        instances = self.session.execute(select(self.model)).scalars().all()
        return [self.schema.model_validate(instance) for instance in instances]

    def create(self, model: BaseModel):
        self.session.add(self.model(**model.model_dump()))
        return "Instance created"


class DepartmentRepository(BaseRepository):
    model = Department
    schema = app.schemas.Department


class EmployeeRepository(BaseRepository):
    model = Employee
    schema = app.schemas.Employee


class TaskRepository(BaseRepository):
    model = Task
    schema = app.schemas.Task


class ScheduleRepository(BaseRepository):
    model = Schedule
    schema = app.schemas.Schedule
