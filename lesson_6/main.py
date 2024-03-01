from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import select

import models
from database import session
from schemas import CreateUniversity, University, CreatePrincipal, Principal, CreateStudent, Student, CreateTeacher, Teacher, CreateDiscipline, Discipline


app = FastAPI()

# Dependency
def get_db():
    db = session
    try:
        yield db
    finally:
        db.close()


@app.post("/universities/")
def create_university(university: CreateUniversity, db: Session = Depends(get_db)):
    db_university = models.University(name=university.name, city=university.city)
    db.add(db_university)
    db.commit()
    db.refresh(db_university)
    return db_university


@app.get("/universities/")
def get_universities(db: Session = Depends(get_db)) -> list[University]:
    db_universities = db.execute(select(db.University)).scalars().all()
    universities = []
    for db_university in db_universities:
        University.append(University.model_validate(db_university))
    return universities
