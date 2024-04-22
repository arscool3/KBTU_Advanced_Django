from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..dependencies import get_db
from ..schemas.schemas import CommentCreate, Comment as CommentSchema
from ..models.models import Comment as CommentModel

router = APIRouter()


@router.post("/comments/", response_model=CommentSchema, status_code=201)
def create_comment(comment: CommentCreate, db: Session = Depends(get_db)):
    new_comment = CommentModel(**comment.dict())
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


@router.get("/comments/", response_model=List[CommentSchema])
def read_comments(db: Session = Depends(get_db)):
    comments = db.query(CommentModel).all()
    return comments


@router.get("/comments/{comment_id}", response_model=CommentSchema)
def read_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = db.query(CommentModel).filter(CommentModel.id == comment_id).first()
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment


@router.put("/comments/{comment_id}", response_model=CommentSchema)
def update_comment(comment_id: int, updated_comment: CommentCreate, db: Session = Depends(get_db)):
    comment = db.query(CommentModel).filter(CommentModel.id == comment_id).first()
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    for var, value in vars(updated_comment).items():
        setattr(comment, var, value) if value else None
    db.commit()
    return comment


@router.delete("/comments/{comment_id}", status_code=204)
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = db.query(CommentModel).filter(CommentModel.id == comment_id).first()
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    db.delete(comment)
    db.commit()
    return {"ok": True}
