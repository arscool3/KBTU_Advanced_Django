from fastapi import FastAPI, HTTPException, Depends, Body
from sqlalchemy.orm import Session

from database import get_db
from user.repository import UserRepo


app = FastAPI()

@app.post("/users/")
def create_category(user_request: UserRepo, db: Session = Depends(get_db)):
    new_user = user_request.create()
    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return new_user


