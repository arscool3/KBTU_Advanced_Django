from fastapi import FastAPI, Depends
from pydantic import BaseModel

app = FastAPI()


class Student(BaseModel):
    name: str
    gpa: float


def dependency_injection(s: Student) -> str:
    return f'Hello {s.name}. I am injected from DI. Your gpa {s.gpa}'


@app.post("/")
def index(dep_func: str = Depends(dependency_injection)):
    return dep_func
