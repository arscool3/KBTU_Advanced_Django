from fastapi import FastAPI, Depends
from sqlalchemy import select, delete
from sqlalchemy.orm import Session
import models as db
from database import session
from schemas import CreateUser, User

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


@app.get("/users")
def get_users(session: Session = Depends(get_db)):
    users = session.execute(select(db.User)).scalars().all()
    user_response = [User.validate(user) for user in users]
    return user_response


@app.get("/users/{user_id}", response_model=User)
def get_user_by_id(user_id: str, session: Session = Depends(get_db)):
    user = session.query(db.User).filter(db.User.id == user_id).first()
    return User.validate(user)


@app.delete("/users/{user_id}")
def delete_user(user_id: str, session: Session = Depends(get_db)):
    item = session.execute(delete(db.User).where(db.User.id == user_id))
    print(item.scalars().all())
    return "User deleted successfully"
