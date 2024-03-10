from typing import List, Optional
from sqlalchemy import func
from fastapi import FastAPI, status, Response, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db, engine
from .. import auth
router = APIRouter(
    prefix='/comments',
    tags=['Comments']
)



@router.get("/", response_model=List[schemas.CommentBase])
def get_comments(db: Session = Depends(get_db), user_id: int = Depends(auth.get_current_user)):
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    posts = db.query(models.Comment).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.CreateComment)
def create_comment(comment: schemas.CreateComment, db: Session = Depends(get_db), current_user: int = Depends(auth.get_current_user)):


    new_commment = models.Comment(**comment.dict())
    db.add(new_commment)
    db.commit()
    db.refresh(new_commment)
    return new_commment


@router.get("/{id}", response_model=schemas.CommentBase)
def get_comment(id: int, db: Session = Depends(get_db), current_user: int = Depends(auth.get_current_user)):
    comment = db.query(models.Comment).filter(models.Comment.id == id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"comment with id: {id} was not found")
    return comment

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(id: int, db: Session = Depends(get_db), current_user: int = Depends(auth.get_current_user)):

    comment = db.query(models.Comment).filter(models.Comment.id == id)
    if comment.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Comment with id: {id} does not exist")
    comment.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

