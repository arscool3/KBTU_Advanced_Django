from pydantic import BaseModel


class BaseUniversity(BaseModel):
    name: str

    class Config:
        from_attributes = True


class University(BaseUniversity):
    id: int


class CreateUniversity(BaseUniversity):
    pass


class BasePerson(BaseModel):
    name: str
    age: int

    class Config:
        from_attributes = True


class Student(BasePerson):
    id: int
    university_id: int
    university: University
    gpa: float


class CreateStudent(BasePerson):
    university_id: int


ReturnType = Student | University
CreateType = CreateStudent | CreateUniversity