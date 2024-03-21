from abc import ABC

from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.repository import AbcRepository
from app.schemas import CreateEmployee, CreateTask, CreateSchedule, CreateDepartment


class BaseDependency(ABC):
    def __init__(self, repo: AbcRepository):
        self.repo = repo

    def __call__(self, *args, **kwargs):
        raise NotImplementedError()


class GetListDependency(BaseDependency):
    def __call__(self, session: Session = Depends(get_db)):
        self.repo.session = session
        return self.repo.get_list()


class DepartmentCreateDependency(BaseDependency):
    def __call__(self, body: CreateDepartment, session: Session = Depends(get_db)):
        self.repo.session = session
        return self.repo.create(body)


class EmployeeCreateDependency(BaseDependency):
    def __call__(self, body: CreateEmployee, session: Session = Depends(get_db)):
        self.repo.session = session
        return self.repo.create(body)


class TaskCreateDependency(BaseDependency):
    def __call__(self, body: CreateTask, session: Session = Depends(get_db)):
        self.repo.session = session
        return self.repo.create(body)


class ScheduleCreateDependency(BaseDependency):
    def __call__(self, body: CreateSchedule, session: Session = Depends(get_db)):
        self.repo.session = session
        return self.repo.create(body)
