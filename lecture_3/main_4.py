from fastapi import  FastAPI, Depends
from pydantic import BaseModel


app = FastAPI()


class Lecturer(BaseModel):
    name: str
    lesson: str


def nested_dependency(l: Lecturer) -> str:
    name = l.name
    lesson = l.lesson
    return f"You are {name}. Your lesson {lesson}"


def dependency(dep_func: str = Depends(nested_dependency)) -> str:
    print("Started Handling Nested Dependency Function")
    return dep_func


@app.post('/')
def index(dep_func: str = Depends(dependency)) -> str:
    return dep_func
