from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..schemas.schemas import EnrollmentCreate, Enrollment
from ..models.models import Enrollment as EnrollmentModel
from ..dependencies import get_db
from ..tasks import process_enrollment

router = APIRouter()


@router.post("/enrollments/", response_model=Enrollment, status_code=201)
async def create_enrollment(enrollment: EnrollmentCreate, db: Session = Depends(get_db)):
    db_enrollment = EnrollmentModel(**enrollment.dict())
    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)
    process_enrollment.send(db_enrollment.id)
    return db_enrollment


@router.get("/enrollments/", response_model=List[Enrollment])
def read_enrollments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    enrollments = db.query(EnrollmentModel).offset(skip).limit(limit).all()
    return enrollments


@router.get("/enrollments/{enrollment_id}", response_model=Enrollment)
def read_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    enrollment = db.query(EnrollmentModel).filter(EnrollmentModel.id == enrollment_id).first()
    if enrollment is None:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return enrollment


@router.put("/enrollments/{enrollment_id}", response_model=Enrollment)
def update_enrollment(enrollment_id: int, enrollment: EnrollmentCreate, db: Session = Depends(get_db)):
    db_enrollment = db.query(EnrollmentModel).filter(EnrollmentModel.id == enrollment_id).first()
    if not db_enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    db_enrollment.course_id = enrollment.course_id
    db_enrollment.user_id = enrollment.user_id
    db.commit()
    return db_enrollment


@router.delete("/enrollments/{enrollment_id}", status_code=204)
def delete_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    enrollment = db.query(EnrollmentModel).filter(EnrollmentModel.id == enrollment_id).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    db.delete(enrollment)
    db.commit()
    return {"ok": True}


