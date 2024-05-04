from typing import Annotated

from fastapi import FastAPI, Path, Query
from pydantic import BaseModel, Field

app = FastAPI()

students = []


def validate_age(age: int) -> int:
    if age < 16:
        raise Exception()
    if age > 30:
        raise Exception
    return age


class Student(BaseModel):
    name: str = Field(max_length=10)
    age: int = Field(ge=16, le=99)


@app.get("/")
def test(age: int):
    return f"{age}"


@app.get("/students/")
def get_all_students(page: Annotated[int, Query(gt=0)], limit: Annotated[int, Query(gt=0)]) -> list[Student]:
    return students[(page - 1) * limit : min(page * limit, len(students))]


@app.post("/student/")
def add_student(student: Student) -> str:
    students.append(student)
    return "added"


@app.get("/students_by_age/")
def get_students_by_age(age: int = Query(gt=0, lt=100)) -> list[Student]:
    return [student for student in students if student.age == age]


@app.get("/student/{id}")
def get_student_by_id(id: Annotated[int, Path(ge=0)]) -> Student:
    return students[id]


# uvicorn main:app --reload


# def decorator(func):
#     import time
#     def wrapper():
#         time_start = time.time()
#         func()
#         time_end = time.time()
#         print(time_end - time_start)
#
#     return wrapper
#
#
# @decorator
# def x():
#     for _ in range(1_000_000_000):
#         continue
#
# x()
