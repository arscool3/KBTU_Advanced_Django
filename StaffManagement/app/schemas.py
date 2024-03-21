from datetime import date

from app.config import ConfigSchema


class Department(ConfigSchema):
    id: int
    employees: list['Employee']


class CreateDepartment(ConfigSchema):
    pass


class Employee(ConfigSchema):
    id: int
    tasks: list['Task']
    schedules: list['Schedule']


class CreateEmployee(ConfigSchema):
    department_id: int


class Task(ConfigSchema):
    id: int
    todo: str
    added_time: date


class CreateTask(ConfigSchema):
    todo: str
    added_time: date
    employee_id: int


class Schedule(ConfigSchema):
    id: int
    description: str


class CreateSchedule(ConfigSchema):
    description: str
    employee_id: int
