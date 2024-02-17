from fastapi import FastAPI, Depends
from pydantic import BaseModel

app = FastAPI()

students = []
teachers = []

class User(BaseModel):
    name: str
    age: int

class Student(User):
    pass

class Teacher(User):
    pass

class UserDependency:
    def __init__(self, user_type: type[User]):
        self.user_type = user_type

    def __call__(self, user: User) -> str:
        if self.user_type == Student:
            students.append(user)
        elif self.user_type == Teacher:
            teachers.append(user)

        return "User was added"

# Dependency as a function
def student_dependency(user: User) -> str:
    students.append(user)
    return "Student was added"

def teacher_dependency(user: User) -> str:
    teachers.append(user)
    return "Teacher was added"

student_dep = student_dependency
teacher_dep = teacher_dependency

# Dependency as an instance of a class
class UserDependencyClass:
    def __init__(self, user_type: type[User]):
        self.user_type = user_type

    def __call__(self, user: User) -> str:
        if self.user_type == Student:
            students.append(user)
        elif self.user_type == Teacher:
            teachers.append(user)

        return "User was added"

user_dep_class = UserDependencyClass(User)

@app.post('/student')
def add_student(user_dep: str = Depends(student_dep)) -> dict:
    return {"message": user_dep}


@app.post('/teacher')
def add_teacher(user_dep: str = Depends(teacher_dep)) -> dict:
    return {"message": user_dep}


@app.get('/students')
def get_students() -> list[Student]:
    return students


@app.get('/teachers')
def get_teachers() -> list[Teacher]:
    return teachers
