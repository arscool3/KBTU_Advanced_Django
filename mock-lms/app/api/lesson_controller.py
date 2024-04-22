from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List
from ..schemas.schemas import LessonCreate, LessonInDB, LessonUpdate
from ..models.models import Lesson
from ..dependencies import get_db

router = APIRouter()


@router.post("/lessons/", response_model=LessonInDB, status_code=status.HTTP_201_CREATED)
async def create_lesson(lesson: LessonCreate, db: Session = Depends(get_db)):
    new_lesson = Lesson(**lesson.dict())
    db.add(new_lesson)
    db.commit()
    db.refresh(new_lesson)
    return new_lesson


@router.get("/lessons/", response_model=List[LessonInDB])
def read_lessons(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    lessons = db.query(Lesson).offset(skip).limit(limit).all()
    return lessons


@router.put("/lessons/{lesson_id}", response_model=LessonInDB)
def update_lesson(lesson_id: int, lesson: LessonUpdate, db: Session = Depends(get_db)):
    db_lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not db_lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    for key, value in lesson.dict(exclude_unset=True).items():
        setattr(db_lesson, key, value)
    db.commit()
    return db_lesson
