from typing import Annotated

from fastapi import FastAPI, Query, Path
from pydantic import BaseModel, Field

app = FastAPI()

students = []


class Student(BaseModel):
    name: str = Field(max_length=10)
    age: int = Field(gt=0, lt=100)


@app.post("/students")
def add_student(student: Student) -> str:
    students.append(student)
    return "Student was added"


@app.get("/students/{id}")
def get_student_by_id(id: Annotated[int, Path(ge=0)]) -> str:
    return f"Student with {id} = {students[id]}"


@app.get("/students/age")
def get_student_by_age(age: Annotated[int, Query(gt=0, lt=100)]) -> list[Student]:
    return [student for student in students if student.age == age]


@app.get("/students")
def get_students() -> list[Student]:
    return students


# @app.get("/students")
# def get_students(page: int, limit: int) -> list[Student]:
#     return students[limit * (page-1): min(len(students), limit*page)]


# uvicorn main:app --reload
# ?age=17 - param