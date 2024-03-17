import logging

import jwt
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from starlette import status

from posts.repository import PostRepository
from users.repository import UserRepository
from utils import models as db
from utils.database import session, get_db
from utils.dependencies import get_container, RetrieveDependency, ListDependency
from utils.repository import AbcRepository
from utils.schemes import CreateUser, User, CreatePost, PrevCreatePost, CreateComment, PrevCreateComment, CreateLike, \
    CreateComplaint, PrevCreateComplaint

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


@app.get("/posts")
def get_posts(repository: PostRepository = Depends(get_post_repository),
              user_id: int = Depends(get_user_id_from_token)):
    posts = repository.list()
    return posts


@app.get("/posts/{post_id}")
def get_posts(post_id: int, repository: PostRepository = Depends(get_post_repository),
              user_id: int = Depends(get_user_id_from_token)):
    post = repository.retrieve(post_id)
    return post

@app.get("/posts/{post_id}/comments")
def get_comments(post_id: int, repository: PostRepository = Depends(get_post_repository),
                 user_id: int = Depends(get_user_id_from_token)):
    return repository.get_comments(post_id=post_id)

@app.post("/posts/{post_id}/comments")
def leave_comment(post_id: int, comment_: PrevCreateComment, repository: UserRepository = Depends(get_user_repository),
                 user_id: int = Depends(get_user_id_from_token)):
    comment = CreateComment(post_id=post_id, user_id=user_id, **comment_.dict())
    return repository.leave_comment(comment=comment)

@app.get("/posts/{post_id}/likes")
def get_likes(post_id: int, repository: PostRepository = Depends(get_post_repository),
                 user_id: int = Depends(get_user_id_from_token)):
    return repository.get_likes(post_id=post_id)

@app.post("/posts/{post_id}/likes")
def put_like(post_id: int, repository: UserRepository = Depends(get_user_repository),
                 user_id: int = Depends(get_user_id_from_token)):
    like = CreateLike(post_id=post_id, user_id=user_id)
    return repository.put_like(like=like)

@app.get("/posts/{post_id}/complaints")
def get_complaints(post_id: int, repository: PostRepository = Depends(get_post_repository),
                 user_id: int = Depends(get_user_id_from_token)):
    return repository.get_complaints(post_id=post_id)

@app.post("/posts/{post_id}/complaints")
def leave_complaint(post_id: int, complaint_: PrevCreateComplaint, repository: UserRepository = Depends(get_user_repository),
                 user_id: int = Depends(get_user_id_from_token)):
    complaint = CreateComplaint(post_id=post_id, user_id=user_id, **complaint_.dict())
    return repository.leave_complaint(complaint=complaint)


