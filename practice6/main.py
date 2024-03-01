from fastapi.params import Depends
from pydantic import BaseModel
from sqlalchemy import select, insert
from fastapi import FastAPI
from database import session

import models as db
from schemas import Student,CreateStudent,Teacher,CreateTeacher,Faculty,CreateFaculty,School,CreateSchool,University,CreateUniversity 
app=FastAPI()

@app.get('/students')
def get_students(name:str=None):
    if name is None:
        db_students=session.execute(
            select(db.Student)
        ).scalars().all()
    else:
        db_students=session.execute(
            select(db.Student).where(db.Student.name==name)
        ).scalars().all()

    students=[]
    for db_student in db_students:
        students.append(Student.model_validate(db_student))
    return students

@app.post('/students')
def add_students(student:CreateStudent)->str:
    session.add(db.Student(**student.model_dump()))
    session.commit()
    session.close()    
    return 'Student= was added'
@app.get('/teachers')
def get_teachers(name:str=None):
    if name is None:
        db_teachers=session.execute(
            select(db.Teacher)
        ).scalars().all()
    else:
        db_teachers=session.execute(
            select(db.Teacher).where(db.Teacher.name==name)
        ).scalars().all()

    teachers=[]
    for db_teacher in db_teachers:
        teachers.append(Teacher.model_validate(db_teacher))
    return teachers

@app.post('/teachers')
def add_students(teacher:CreateTeacher)->str:
    session.add(db.Teacher(**Teacher.model_dump()))
    session.commit()
    session.close()    
    return 'Teacher was added'

@app.post("/faculty")
def add_faculty(faculty: CreateFaculty):
    session.add(db.Faculty(**faculty.model_dump()))
    session.commit()
    session.close()
    return "Faculty was added"

@app.get("/faculty")
def get_faculty():
    db_faculties = session.execute(select(db.Faculty)).scalars().all()
    countries = []
    for db_faculty in db_faculties:
        countries.append(Faculty.model_validate(db_faculty))
    return countries

@app.post('/School')
def add_school(school:CreateSchool)->str:
    session.add(db.School(**school.model_dump()))
    session.commit()
    session.close()    
    return "School was added"

@app.get("/School")
def get_schools():
    db_schools = session.execute(select(db.School)).scalars().all()
    schools= []
    for db_school in db_schools:
        schools.append(School.model_validate(db_school))
    return schools

@app.post('/University')
def add_university(university:CreateUniversity)->str:
    session.add(db.University(**university.model_dump()))
    session.commit()
    session.close()    
    return "School was added"

@app.get("/University")
def get_universities():
    db_universities = session.execute(select(db.Univeristy)).scalars().all()
    universities= []
    for db_university in db_universities:
        universities.append(University.model_validate(db_university))
    return universities