from fastapi import FastAPI
from sqlalchemy import select

import database as db
import schemas
import models

app = FastAPI()


@app.get('/users')
def get_users():
    db_users = db.session.execute(select(models.User)).scalars().all()
    users = []
    for user in db_users:
        users.append(user)
    return users


@app.post('/users')
def add_users(user: schemas.CreateUser):
    db.session.add(models.User(**user.model_dump()))
    db.session.commit()
    db.session.close()
    return f"{user.name} was added"


@app.get('/posts')
def get_posts():
    db_posts = db.session.execute(select(models.Post)).scalars().all()
    posts = []
    for post in db_posts:
        posts.append(post)
    return posts


@app.post('/posts')
def add_post(post: schemas.CreatePost):
    db.session.add(models.Post(**post.model_dump()))
    db.session.commit()
    db.session.close()
    return f"{post.title} was published"
