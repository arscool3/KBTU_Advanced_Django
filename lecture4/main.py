from fastapi import FastAPI, Depends
from pydantic import BaseModel

app = FastAPI()


class Teacher(BaseModel):
    name: str
    years: int


class TeacherWithLesson(BaseModel):
    teacher: Teacher
    lesson: str


class Student(BaseModel):
    name: str
    age: int


# 1 handler and 1 Function that is injected as DI
def nested_dependency(teacher_with_lesson: TeacherWithLesson):
    lesson = teacher_with_lesson.lesson
    teacher = teacher_with_lesson.teacher
    return f"You have joined {lesson}, Your teacher is {teacher.name} with {teacher.years} years of experience"


def dependency(nested_dep_func: str = Depends(nested_dependency)) -> str:
    print("Started Handling Nested Dependency Function")
    return nested_dep_func


# create 1 handler with nested dependency
def nested_dependency_python_basics(teacher_with_lesson: TeacherWithLesson):
    lesson = teacher_with_lesson.lesson
    teacher = teacher_with_lesson.teacher
    return (f"You have joined basic course {lesson}, Your teacher is {teacher.name} with {teacher.years} "
            f"years of experience")

def dependency_python_basics(nested_dep_func: str = Depends(nested_dependency_python_basics)):
    return nested_dep_func


@app.post('/student')
def student(dep_func: str = Depends(dependency)):
    return dep_func


@app.post("/python-basics")
def python_basics(dep_func: str = Depends(nested_dependency_python_basics)):
    return dep_func


# Class Work:

# class DependencyClass:
#     def __init__(self, lesson: str):
#         self.lesson = lesson
#     def __call__(self, teacher: Teacher):
#         if self.lesson == 'Django Advanced':
#             return f"You have joined Django Advanced Lesson, this is advanced lesson. Your teacher is {teacher.name}"
#         else:
#             return f"You have joined Basic Django Lesson, this is inter lesson. Your teacher is {teacher.name}"


# dep_class_adv = DependencyClass(lesson="Django Advanced")
# dep_class_basic = DependencyClass(lesson="Django Basic")

# class DependencyClassPythonBasics:
#     def __init__(self, lesson: str):
#         self.lesson = lesson
#
#     def __call__(self, teacher: Teacher) -> str:
#         if self.lesson == 'Python Basics':
#             return f"You have joined Python Basics Lesson. Your teacher is {teacher.name}"
#         else:
#             return f"You have joined a different lesson. Your teacher is {teacher.name}"
#
#
# dep_class_python_basics = DependencyClassPythonBasics(lesson="Python Basics")


# def dependency(teacher: Teacher) -> str:
#     return f"Hello, {teacher.name}! How was your {teacher.lesson} lesson?"
#
#
# @app.post("/basic")
# def basic_django(dep_func: str = Depends(dep_class_basic)):
#     return dep_func
#
#
# @app.post("/advanced")
# def advanced_django(dep_func: str = Depends(dep_class_adv)):
#     return dep_func

# @app.post("/python-basics")
# def python_basics(dep_func: str = Depends(dep_class_python_basics)):
#     return dep_func
