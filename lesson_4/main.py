from abc import abstractstaticmethod, abstractmethod
from contextlib import contextmanager

import punq
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import select, update

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


@contextmanager
def get_db():
    try:
        session = db.session
        yield session
        session.commit()
    except Exception:
        raise
    finally:
        session.close()


class RepoAbc:
    @staticmethod
    @abstractmethod
    def get_by_id(id: int):
        raise NotImplementedError()


class PresidentRepo(RepoAbc):
    @staticmethod
    def get_by_id(id: int):
        with get_db() as session:
            print(session.get(db.President, id))
            return session.get(db.President, id)


class Dep:
    def __init__(self, repo: RepoAbc):
        self.repo = repo

    def __call__(self, id: int):
        return self.repo.get_by_id(id)


def container() -> punq.Container:
    container = punq.Container()
    container.register(RepoAbc, PresidentRepo)
    container.register(Dep)
    return container


app.add_api_route('/president', container().resolve(Dep))


# session.add(db.Lesson())
# session.execute(update(db.Student).where(db.Student.id == 1).values(lesson_Id=1))
# session.add(db.Student(**student.model_dump()))
# return f"Student {student.name} was added"


# 1 student (Pydantic model)
# 2 session = get_session()
# 3 session.add(db.Student(**student.model_dump()))
#   return f"Student {student.name} was added"
# 4 session.commit()
#   session.close()

# @app.get('/student')
# def student() -> list[Student]:
#     db_students = db.session.execute(select(db.Student)).scalars().all()
#     print(db_students[0].lesson.students)
#     students = []
#     for db_student in db_students:
#         students.append(Student.model_validate(db_student))
#     return students

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
