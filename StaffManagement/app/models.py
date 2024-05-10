from datetime import date

from sqlalchemy.orm import Mapped

from app.config import ConfigModel
import sqlalchemy
from sqlalchemy.orm import mapped_column, relationship
from app.database import Base


class Department(ConfigModel, Base):
    __tablename__ = 'departments'

    employees: Mapped[list['Employee']] = relationship(back_populates='department')


class Employee(ConfigModel, Base):
    __tablename__ = 'employees'

    department_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('departments.id'))

    department: Mapped[Department] = relationship(back_populates='employees')

    tasks: Mapped[list['Task']] = relationship(back_populates='employee')
    schedules: Mapped[list['Schedule']] = relationship(back_populates='employee')


class Task(ConfigModel, Base):
    __tablename__ = 'tasks'

    todo: Mapped[str]
    added_time: Mapped[date] = mapped_column(sqlalchemy.Date, default=date.today())

    employee_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('employees.id'))

    employee: Mapped[Employee] = relationship(back_populates='tasks')


class Schedule(ConfigModel, Base):
    __tablename__ = 'schedules'

    description: Mapped[str]

    employee_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('employees.id'))

    employee: Mapped[Employee] = relationship(back_populates='schedules')
