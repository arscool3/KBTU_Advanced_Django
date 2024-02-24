from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import select

import database as db

app = FastAPI()


class Teacher(BaseModel):
    name: str
    years: int

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


@app.get('/student')
def student() -> list[Student]:
    db_students = db.session.execute(select(db.Student)).scalars().all()
    students = []
    for db_student in db_students:
        students.append(Student.model_validate(db_student))
    return students


# 1 student (Pydantic model)
# 2 session = get_session()
# 3 session.add(db.Student(**student.model_dump()))
#   return f"Student {student.name} was added"
# 4 session.commit()
#   session.close()