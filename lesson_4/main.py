from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import select

import database as db

app = FastAPI()


class Teacher(BaseModel):
    name: str
    yoe: int

    class Config:
        from_attributes = True


class Student(BaseModel):
    name: str
    age: int

    class Config:
        from_attributes = True


def get_db():
    session = db.session
    yield session
    session.commit()
    session.close()


@app.post('/student')
def student(student: Student, session: db.Session = Depends(get_db)):
    session.add(db.Student(**student.model_dump()))
    return f"Student {student.name} was added"


# 1 student (Pydantic model)
# 2 session = get_session()
# 3 session.add(db.Student(**student.model_dump()))
#   return f"Student {student.name} was added"
# 4 session.commit()
#   session.close()

@app.get('/student')
def student() -> list[Student]:
    db_students = db.session.execute(select(db.Student)).scalars().all()
    students = []
    for db_student in db_students:
        students.append(Student.model_validate(db_student))
    return students

# A -> B

# x, y, z

# A x-> B
# A y-> B
# A z-> B
# Commit (if everything is ok (x,y,z were sent to destination))

# Atomicity (Атомарность)

#
# def nested_dependency(teacher_with_lesson: TeacherWithLesson):
#     lesson = teacher_with_lesson.lesson
#     teacher = teacher_with_lesson.teacher
#     return f"You have joined {lesson}, Your teacher is {teacher.name} with {teacher.yoe} years of experience"
#
#
# def dependency(nested_dep_func: str = Depends(nested_dependency)) -> str:
#     print("Started Handling Nested Dependency Function")
#     return nested_dep_func
#
#
# @app.post('/student')
# def student(dep_func: str = Depends(dependency)):
#     return dep_func

# @contextmanager
# def gen():
#     x = 0
#     while x <= 5:
#         yield x
#         x += 1
#
#
# g = gen()
#
# for i in g:
#     print(i)