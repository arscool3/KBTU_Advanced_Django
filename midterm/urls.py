import models
from fastapi import APIRouter, Depends
from database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import select
from schemas import Mark, CreateMark

router = APIRouter(prefix="")


@router.get("/marks/")
def get_marks_list(db: Session = Depends(get_db)) -> list[Mark]:
    db_marks = db.execute(select(models.Mark)).scalars()
    return [Mark.model_validate(db_mark) for db_mark in db_marks]
