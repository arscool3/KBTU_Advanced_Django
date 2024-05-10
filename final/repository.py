from sqlalchemy.orm import Session
from database.database import User, Project, Task, Comment, Notification, Event
from schemas import UserCreate, ProjectCreate, TaskCreate, CommentCreate, NotificationCreate, EventCreate
from tasks import send_notification
from kafkaconfig.producer import send_data_to_kafka

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def create_user(self, user: UserCreate):
        db_user = User(**user.dict())
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_users(self):
        return self.db.query(User).all()

class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_project(self, project_id: int):
        return self.db.query(Project).filter(Project.id == project_id).first()

    def create_project(self, project: ProjectCreate):
        db_project = Project(**project.dict())
        self.db.add(db_project)
        self.db.commit()
        self.db.refresh(db_project)
        return db_project

    def get_projects(self):
        return self.db.query(Project).all()

class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_task(self, task_id: int):
        return self.db.query(Task).filter(Task.id == task_id).first()

    def create_task(self, task: TaskCreate):
        send_data_to_kafka('Tasks', str(task.dict()))
        db_task = Task(**task.dict())
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def get_tasks(self):
        return self.db.query(Task).all()

class CommentRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_comment(self, comment_id: int):
        return self.db.query(Comment).filter(Comment.id == comment_id).first()

    def create_comment(self, comment: CommentCreate):
        db_comment = Comment(**comment.dict())
        self.db.add(db_comment)
        self.db.commit()
        self.db.refresh(db_comment)
        return db_comment

    def get_comments(self):
        return self.db.query(Comment).all()

class NotificationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_notification(self, notification_id: int):
        return self.db.query(Notification).filter(Notification.id == notification_id).first()

    def create_notification(self, notification: NotificationCreate):
        recipient = self.db.query(User).filter(User.id == notification.user_id).first()
        send_notification.send(recipient.email, **notification.dict())
        db_notification = Notification(**notification.dict())
        self.db.add(db_notification)
        self.db.commit()
        self.db.refresh(db_notification)
        return db_notification

    def get_notifications(self):
        return self.db.query(Notification).all()

class EventRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_event(self, event_id: int):
        return self.db.query(Event).filter(Event.id == event_id).first()

    def create_event(self, event: EventCreate):
        db_event = Event(**event.dict())
        self.db.add(db_event)
        self.db.commit()
        self.db.refresh(db_event)
        return db_event

    def get_events(self):
        return self.db.query(Event).all()
