from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models as db
from database import session
from schemas import CreateUser

app = FastAPI()


def get_db():
    try:
        yield session
        session.commit()
    except:
        raise
    finally:
        session.close()


@app.post("/users")
def add_user(user: CreateUser, session: Session = Depends(get_db)) -> dict:
    session.add(db.User(**user.model_dump()))
    return {"message": "User added successfully"}
