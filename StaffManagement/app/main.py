from fastapi import FastAPI, Depends
from sqlalchemy.orm.session import Session
import app.models as db
from app.database import get_db
from app.schemas import CreateDepartment, Department,\
    CreateTask, Task, CreateEmployee, Employee, CreateSchedule, Schedule
from sqlalchemy import select

app = FastAPI()


@app.get("/get_departments")
def get_departments(session: Session = Depends(get_db)) -> list[Department]:
    db_departments = session.execute(select(db.Department)).scalars().all()
    departments = [Department.model_validate(db_department) for db_department in db_departments]
    return departments


@app.post('/add_department')
def add_department(department: CreateDepartment, session: Session = Depends(get_db)) -> str:
    session.add(db.Department(**department.model_dump()))
    return department.name


@app.get("/get_employees")
def get_employees(session: Session = Depends(get_db)):
    db_employees = session.execute(select(db.Employee)).scalars().all()
    employees = [Employee.model_validate(db_employee) for db_employee in db_employees]
    return employees


@app.post("/add_employee")
def add_employee(employee: CreateEmployee, session: Session = Depends(get_db)):
    session.add(db.Employee(**employee.model_dump()))
    return employee.name
