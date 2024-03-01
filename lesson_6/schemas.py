from datetime import date
from pydantic import BaseModel
from typing import List

from models import Teacher, Principal, Student, University, Discipline

class BaseUniversity(BaseModel):
    name: str
    city: str

    class Config:
        from_attributes = True

class CreateUniversity(BaseUniversity):
    pass

class University(BaseUniversity):
    id: int
    principal: Principal
    students: List[Student] = []
    teachers: List[Teacher] = []

class BasePrincipal(BaseModel):
    name: str

    class Config:
        from_attributes = True

class CreatePrincipal(BasePrincipal):
    university_id: int

class Principal(BasePrincipal):
    id: int
    university: University

class BaseStudent(BaseModel):
    name: str

    class Config:
        from_attributes = True

class CreateStudent(BaseStudent):
    university_id: int

class Student(BaseStudent):
    id: int
    university: University

class BaseTeacher(BaseModel):
    name: str

    class Config:
        from_attributes = True

class CreateTeacher(BaseTeacher):
    university_id: int

class Teacher(BaseTeacher):
    id: int
    university: University
    disciplines: List[Discipline] = []

class BaseDiscipline(BaseModel):
    name: str

    class Config:
        from_attributes = True

class CreateDiscipline(BaseDiscipline):
    teacher_id: int

class Discipline(BaseDiscipline):
    id: int
    teacher: Teacher

