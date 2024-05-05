from fastapi import FastAPI, Depends
from pydantic import BaseModel

app = FastAPI()


class Teacher(BaseModel):
    name: str
    exp_year: int


class DependencyClass:
    def __init__(self, lesson: str):
        self.lesson = lesson

    def __call__(self, teacher: Teacher):
        return f'Lesson - {self.lesson}, teacher - {teacher.name}'


dep_class_django = DependencyClass('django')
dep_class_spring = DependencyClass('spring')


@app.post('/django')
def django(dep_func: str = Depends(dep_class_django)) -> str:
    return dep_func


@app.post('/spring')
def spring(dep_func: str = Depends(dep_class_spring)) -> str:
    return dep_func
