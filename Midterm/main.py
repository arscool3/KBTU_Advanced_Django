from fastapi import FastAPI, HTTPException, Depends, Body
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from user.models import User
from user.repository import UserRepo
from user.schemas import BaseUser, CreateUser

app = FastAPI()

@app.post("/users/")
def create_category(user: CreateUser, session: Session = Depends(get_db)):
    user_repo = UserRepo()
    user_repo.session = session
    new_user = user_repo.create(user)
    return new_user


