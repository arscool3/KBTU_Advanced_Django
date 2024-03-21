from datetime import date

from app.config import ConfigSchema
from pydantic import BaseModel


class Department(ConfigSchema):
    id: int
    employees: list['Employee']


class CreateDepartment(ConfigSchema):
    pass


class Employee(ConfigSchema):
    id: int
    tasks: list['Task']
    schedules: list['Schedule']


class CreateEmployee(BaseModel):
    name: str
    department_id: int


class Task(ConfigSchema):
    id: int


class CreateTask(BaseModel):
    name: str
    todo: str
    added_time: date
    employee_id: int


class Schedule(ConfigSchema):
    id: int


class CreateSchedule(BaseModel):
    name: str
    description: str
    employee_id: int
