import hashlib

import punq
from fastapi import FastAPI, Depends

import database
import database as db
from database import session
from hashing.hash import hash_and_save_password, add_user_to_redis
from repository.repository import *
from schemas import *

app = FastAPI()

REDIS_URL = "redis://localhost:6380"


def get_db():
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


class Dependency:
    def __init__(self, repo: AbcRepository):
        self.repo = repo

    def __call__(self, obj_id: int) -> User | Chat | Message | Group | Membership | Attachment:
        return self.repo.get_by_id(obj_id)


def get_container(repository: type[AbcRepository]) -> punq.Container:
    container = punq.Container()
    container.register(AbcRepository, repository, instance=repository(session=database.session))
    container.register(Dependency)
    return container


@app.get("/")
def root():
    return "OK"


app.add_api_route("/users", get_container(UserRepository).resolve(Dependency), methods=["GET"])

app.add_api_route("/chats", get_container(ChatRepository).resolve(Dependency), methods=["GET"])

app.add_api_route("/messages", get_container(MessageRepository).resolve(Dependency), methods=["GET"])

app.add_api_route("/groups", get_container(GroupRepository).resolve(Dependency), methods=["GET"])

app.add_api_route("/memberships", get_container(MembershipRepository).resolve(Dependency), methods=["GET"])

app.add_api_route("/attachments", get_container(AttachmentRepository).resolve(Dependency), methods=["GET"])

# app.add_api_route("/notifications", get_container(NotificationRepository).resolve(Dependency), methods=["GET"])


@app.post('/users_hashed')
async def add_user(user: CreateUser, session: Session = Depends(get_db)) -> str:
    db_user = db.User(username=user.username, email=user.email)
    db_user.password = hashlib.sha256(user.password.encode()).hexdigest()
    session.add(db_user)
    session.commit()
    user_id = db_user.id
    await hash_and_save_password(user.password, user_id)
    await add_user_to_redis(user, user_id)
    return f"User {user.username} was added."


@app.post('/users')
def add_user(user: CreateUser, session: Session = Depends(get_db)) -> str:
    session.add(db.User(**user.model_dump()))
    return user.username + " was added."


@app.post('/chats')
def add_chat(chat: CreateChat, session: Session = Depends(get_db)) -> str:
    session.add(db.Chat(**chat.model_dump()))
    return chat.name + " was added."


@app.post('/groups')
def add_groups(group: CreateGroup, session: Session = Depends(get_db)) -> str:
    session.add(db.Group(**group.model_dump()))
    return "Group was created."


@app.post('/memberships')
def add_memberships(group: CreateMembership, session: Session = Depends(get_db)) -> str:
    session.add(db.Membership(**group.model_dump()))
    return "Membership was created."


@app.get("/messages/{user_id}", response_model=list[Message])
def get_messages(user_id: int, db: Session = Depends(get_db)):
    message_repo = MessageRepository(db)
    return message_repo.get_messages_for_user(user_id)


@app.post('/send_message')
def add_message(group: CreateMessage, session: Session = Depends(get_db)) -> str:
    session.add(db.Message(**group.model_dump()))
    return "Message sent."

