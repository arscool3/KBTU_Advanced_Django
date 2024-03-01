from typing import List

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import get_db, session
import schemas
import models
import repositories
from dependencies import PostCreateDep, CommentCreateDep, ListDep, LikeCreateDep

app = FastAPI()


def get_user_dep(id: int, session: Session = Depends(get_db)) -> schemas.User:
    user = session.get(models.User, id)
    return schemas.User.model_validate(user)


@app.post("/users")
async def create_user(
        user: schemas.CreateUser,
        db_session: Session = Depends(get_db),
):
    db_session.add(models.User(**user.model_dump()))
    db_session.commit()
    return "User added"


@app.get("/users")
async def get_user(dep_func: schemas.User = Depends(get_user_dep)):
    return dep_func


@app.post("/posts")
async def create_post(
        dep: schemas.CreatePost = Depends(PostCreateDep(repositories.PostRepository(session()))),
):
    return dep


@app.get("/posts")
async def get_posts(
        dep_func: List[schemas.Post] = Depends(ListDep(repositories.PostRepository(session()))),
):
    return dep_func


@app.post("/comments")
async def create_comment(
        dep_func: schemas.CreateComment = Depends(CommentCreateDep(repositories.CommentRepository(session()))),
):
    return dep_func


@app.get("/comments")
async def get_comments(
        dep_func: List[schemas.Comment] = Depends(ListDep(repositories.CommentRepository(session()))),
):
    return dep_func


@app.post("/likes")
async def create_like(
        dep_func: schemas.CreateLike = Depends(LikeCreateDep(repositories.LikeRepository(session()))),
):
    return dep_func


@app.get("/likes")
async def get_like(
        dep_func: List[schemas.Like] = Depends(ListDep(repositories.LikeRepository(session()))),
):
    return dep_func
