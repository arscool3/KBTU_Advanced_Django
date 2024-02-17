import uvicorn
from fastapi import FastAPI, Depends
from pydantic import BaseModel

app = FastAPI()


class Student(BaseModel):
    name: str
    age: int


class Course(BaseModel):
    name: str
    credits: int




students = []
courses = []


def add_student_dep(student: Student):
    students.append(student)
    return student


def add_course_dep(course: Course):
    courses.append(course)
    return course


class StudentDep:
    def __call__(self, student: Student):
        students.append(student)
        return student


@app.post("/student")
async def create_student(student_dep: Student = Depends(add_student_dep)):
    return student_dep


@app.post("/course")
async def create_course(course_dep: Course = Depends(add_course_dep)):
    return course_dep


@app.post("/student/v2")
async def create_student_with_class(student_dep: Student = Depends(StudentDep())):
    return student_dep


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
# class Book(BaseModel):
#     name: str
#     author: str
#
#
# class Magazine(BaseModel):
#     name: str
#     name2: str
#
#
# literatures = []
#
#
# def get_book_dep(literature: Book | Magazine):
#     literatures.append(literature)
#     return literature
#
#
# @app.post("/book")
# async def create_book(lit_dep=Depends(get_book_dep)):
#     return lit_dep
#
#
# @app.post("/magazine")
# async def create_book(lit_dep=Depends(get_book_dep)):
#     return lit_dep
