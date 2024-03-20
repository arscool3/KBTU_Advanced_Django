from datetime import date

from app.config import ConfigSchema
from pydantic import BaseModel


class Department(ConfigSchema):
    employees: list['Employee']


class CreateDepartment(BaseModel):
    name: str


class Employee(ConfigSchema):
    tasks: list['Task']
    schedules: list['Schedule']


class CreateEmployee(BaseModel):
    name: str
    department_id: int


class Task(ConfigSchema):
    pass


class CreateTask(BaseModel):
    name: str
    todo: str
    added_time: date
    employee_id: int


class Schedule(ConfigSchema):
    pass


class CreateSchedule(BaseModel):
    name: str
    description: str
    employee_id: int
