import json
import punq as punq
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models as db
from database import session
from schemas import UserCreate, EventCreate, CameraCreate, NotificationCreate, ReturnType
from services import get_db, create_access_token, get_current_user, pwd_context
from starlette import status
from producer import KafkaProducer
from repository import Repository, UserRepository, EventRepository

app = FastAPI()
topic = "events_topic"
kafka_producer = KafkaProducer(servers="localhost:9092")


class Dependency:
    def __init__(self, repo: Repository):
        self.repo = repo

    def __call__(self, id: int) -> ReturnType:
        return self.repo.get_by_id(1)


class DependencyAll:
    def __init__(self, repo: Repository):
        self.repo = repo

    def __call__(self) -> list[ReturnType]:
        return self.repo.get_all()


def get_container(repository: type[Repository]) -> punq.Container:
    container = punq.Container()
    container.register(Repository, repository, instance=repository(session=session))
    container.register(Dependency)
    container.register(DependencyAll)
    return container


app.add_api_route("/users", get_container(UserRepository).resolve(Dependency), methods=["GET"])
app.add_api_route("/events", get_container(EventRepository).resolve(Dependency), methods=["GET"])

app.add_api_route("/all_users", get_container(UserRepository).resolve(DependencyAll), methods=["GET"])
app.add_api_route("/all_events", get_container(EventRepository).resolve(DependencyAll), methods=["GET"])


@app.post("/users")
def add_user(user: UserCreate, session: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(user.password)
    session.add(db.User(username=user.username, password=hashed_password))
    session.commit()
    session.close()
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer", "greeting": user.username}


@app.post("/login")
def login(user_credentials: UserCreate, session: Session = Depends(get_db)):
    db_user = session.query(db.User).filter(db.User.username == user_credentials.username).first()

    if db_user is None or not pwd_context.verify(user_credentials.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": db_user.username})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": db_user.username
    }


@app.get("/me")
def get_user(user: UserCreate = Depends(get_current_user)):
    return user


@app.delete("/users/{user_id}")
def delete_user(user_id: int, session: Session = Depends(get_db)):
    user = session.query(db.User).filter(db.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"message": "User deleted"}


@app.get("/users/{user_id}")
def read_user(user_id: int, session: Session = Depends(get_db)):
    user = session.query(db.User).filter(db.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/events")
def add_event(event: EventCreate, session: Session = Depends(get_db)):
    session.add(db.Event(description=event.description, is_prohibited=event.is_prohibited, user_id=event.user_id, camera_id=event.camera_id))
    session.commit()
    session.close()
    kafka_producer.send_to_kafka(topic=topic, entry={"description": event.description, "is_prohibited": event.is_prohibited, "user_id": event.user_id, "camera_id": event.camera_id})
    return {"message": "Event added"}


@app.post('/cameras')
def add_camera(camera: CameraCreate, session: Session = Depends(get_db)) -> str:
    session.add(db.Camera(**camera.model_dump()))
    return camera.location


@app.post("/notifications")
def add_notification(notification: NotificationCreate, session: Session = Depends(get_db)) -> str:
    new_notification = db.Notification(message=notification.message, event_id=notification.event_id)
    session.add(new_notification)
    session.commit()
    session.refresh(new_notification)

    return "Notification added"

