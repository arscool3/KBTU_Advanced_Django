import datetime
from typing import List
from contextlib import contextmanager

import punq
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import select

import database
import models as db
from repository import AbcRepository, UniversityRepository, StudentRepository

from schemas import Student, CreateStudent, University, CreateUniversity, ReturnType, CreateType

app = FastAPI()


class Dependency:
    def __init__(self, repository: AbcRepository):
        self.repository = repository

    def __call__(self, id: int, name: str) -> str:
        return self.repository.update_name(id=id, name=name)


def get_container(repository: type[AbcRepository]) -> punq.Container:
    container = punq.Container()
    container.register(AbcRepository, repository, instance=repository(session=database.session))
    container.register(Dependency)
    return container


@contextmanager
def get_db():
    try:
        session = database.session
        yield session
        session.commit()
    except Exception as e:
        raise
    finally:
        session.close()


@app.get("/")
def welcome() -> str:
    return "Welcome to"


@app.get("/universities")
def get_universities() -> List[University]:
    with get_db() as session:
        db_universities = session.execute(select(db.University)).scalars().all()
        universities = []
        for db_university in db_universities:
            universities.append(University.model_validate(db_university))
        return universities


@app.post("/students")
def create_student(student: CreateStudent) -> str:
    with get_db() as session:
        session.add(db.Student(**student.model_dump()))
    return "Student created"


@app.get("/students")
def get_students() -> List[Student]:
    with get_db() as session:
        db_students = session.execute(select(db.Student)).scalars().all()
        students = []
        for db_student in db_students:
            students.append(Student.model_validate(db_student))

        return students


@app.post("/universities")
def create_university(university: CreateUniversity) -> str:
    with get_db() as session:
        session.add(db.University(**university.model_dump()))
    return "University created"


# @app.post("/universities")
# def update_university(id: int, name: str) -> str:
#     return 'it is good'
# return get_container(UniversityRepository).resolve(Dependency)(id=id, name=name)
app.add_api_route("/universities/update-name", get_container(UniversityRepository).resolve(Dependency),
                  methods=['POST'])
app.add_api_route("/students/update-name", get_container(StudentRepository).resolve(Dependency), methods=['POST'])


def authenticate_user(token: str, id: int):
    if token == "valid_token":
        return True
    else:
        return False


def get_current_user(token: str = Depends(authenticate_user)):
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return True  # Or return user object if needed


def count_age(birth_year: int):
    return datetime.datetime.now().year - birth_year


@app.post("/birth-year")
def write_birth_year(age: int = Depends(count_age)):
    return f'your age is {age}'


@app.get("/protected")
async def protected_route(current_user: bool = Depends(get_current_user)):
    return {"message": "You have access to the protected route"}
