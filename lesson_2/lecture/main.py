from typing import Annotated

from fastapi import FastAPI, Path, Query
from pydantic import BaseModel, Field

app = FastAPI()

students = []


class Student(BaseModel):
    name: str = Field(max_length=10)
    age: int = Field(gt=0, lt=100)


@app.get("/students")
def get_students() -> list[Student]:
    return students


@app.get("/students/{id}")
def get_student_by_id(id: Annotated[int, Path(ge=0)]) -> Student:
    return students[id]


@app.get("/students_by_age/")
def get_students_by_age(age: Annotated[int, Query(gt=0, lt=100)]) -> list[Student]:
    return [student for student in students if student.age == age]


@app.post("/students")
def add_student(student: Student) -> str:
    students.append(student)
    return "Student was added"


# uvicorn main:app --reload
# ?age=12
# /students/0