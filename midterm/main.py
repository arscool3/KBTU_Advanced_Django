import logging

import jwt
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status

from posts.repository import PostRepository
from users.repository import UserRepository
from utils import models as db
from utils.database import session, get_db
from utils.dependencies import get_container, RetrieveDependency
from utils.repository import AbcRepository
from utils.schemes import CreateUser, User, CreatePost, PrevCreatePost

app = FastAPI()
auth_scheme = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/all-users")
def get_all_users():
    db_users = session.execute(select(db.User)).scalars().all()
    users = [User.model_validate(db_user) for db_user in db_users]
    return users


@app.post("/register")
def registration(user: CreateUser, session: Session = Depends(get_db)):
    session.add(db.User(**user.model_dump()))
    return "User created"


@app.post("/login")
def login(payload: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_db)):
    try:
        user = session.query(db.User).filter(db.User.username == payload.username).first()
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user credentials"
        )
    logging.log(level=1, msg="login user found")
    if not user.validate_password(password=payload.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user credentials"
        )
    return user.generate_token()


def get_user_id_from_token(token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized: Missing token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = jwt.decode(token.credentials, db.secret_key, algorithms=["HS256"])
        user_id = payload.get("id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized: Invalid token payload",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized: Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized: Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.get("/home")
def get_home(user_id: int = Depends(get_user_id_from_token), session: Session = Depends(get_db)):
    db_user = session.query(db.User).get(user_id)
    user = User.model_validate(db_user)
    return f"Hello user: {user.username}!"


def get_post_repository(session: Session = Depends(get_db)) -> PostRepository:
    return PostRepository(session=session)


def get_user_repository(session: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(session=session)


@app.post("/posts")
def create_post(post: PrevCreatePost,
                user_id: int = Depends(get_user_id_from_token),
                repository: PostRepository = Depends(get_post_repository)):
    post_ = CreatePost(user_id=user_id, **post.dict())
    return repository.create(post_)


