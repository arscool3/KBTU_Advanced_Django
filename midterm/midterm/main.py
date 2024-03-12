import http
import models as db
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select, delete
from sqlalchemy.orm import Session
from database import session
from schemas import CreateUser, User, GetFavorite, CreateCategory, CreatePost

app = FastAPI()


def get_db():
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()


@app.post("/users", response_model=dict, tags=["User"])
def add_user(user: CreateUser, session: Session = Depends(get_db)) -> dict:
    try:
        if user.password == "":
            return {"message": "Password is empty"}
        new_user = db.User(**user.model_dump())
        session.add(new_user)
        cur_id = session.query(db.User).where(db.User.username == user.username).first().id
        session.add(db.Favorite(owner_id=cur_id))
        return {"message": "User added successfully"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/users", response_model=list[User], tags=["User"])
def get_users(session: Session = Depends(get_db)):
    try:
        users = session.execute(select(db.User)).scalars().all()
        user_response = [User.validate(user) for user in users]
        return user_response
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/users/{user_id}", response_model=User, tags=["User"])
def get_user_by_id(user_id: str, session: Session = Depends(get_db)):
    try:
        user = session.query(db.User).filter(db.User.id == user_id).first()
        if user.id:
            return User.model_validate(user)
        else:
            raise HTTPException(status_code=http.HTTPStatus.NOT_FOUND, detail={"message": "User not found"})
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/users/{user_id}", response_model=dict, tags=["User"])
def delete_user(user_id: str, session: Session = Depends(get_db)):
    try:
        favorite_count = session.execute(delete(db.Favorite).where(db.Favorite.owner_id == user_id)).rowcount
        deleted_count = session.execute(delete(db.User).where(db.User.id == user_id)).rowcount
        if deleted_count == 0 or favorite_count == 0:
            raise HTTPException(status_code=http.HTTPStatus.NOT_FOUND, detail="User not found")
        return {"message": "User deleted successfully"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/favorite/{user_id}", tags=["Favorite"])
def get_user_favorite(user_id: str, session: Session = Depends(get_db)):
    try:
        favorite = session.query(db.Favorite).filter(db.Favorite.owner_id == user_id).first()
        if not favorite.id:
            return {"message": "favorite not found!"}
        return GetFavorite.model_validate(favorite)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/category", tags=["Category"])
def add_category(category: CreateCategory, session: Session = Depends(get_db)):
    if not category.name:
        return {"message": "name is empty!"}

    session.add(db.Category(**category.model_dump()))

    return {"message": "category is created!"}


@app.get("/post", tags=["Post"])
def get_posts():
    post = session.query(db.Post).all()
    return post


@app.post("/post", tags=["Post"])
def add_post(post: CreatePost, session: Session = Depends(get_db)):
    if post.title == "" or post.content == "":
        return {"message": "post title or content is empty!"}
    session.add(db.Post(**post.model_dump()))
    return {"message": "post is created!"}
