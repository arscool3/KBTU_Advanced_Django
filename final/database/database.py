from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Text, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from dotenv import dotenv_values
config = dotenv_values(".env")

url = 'postgresql://{user}:{password}@localhost:5428/{database}'.format(
    user=config.get("POSTGRES_USER"),
    password=config.get("POSTGRES_PASSWORD"),
    database=config.get("POSTGRES_DB")
)

engine = create_engine(url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    active = Column(Boolean, default=True)
    # Relationships
    projects = relationship("Project", back_populates="owner")
    tasks = relationship("Task", back_populates="assignee")
    comments = relationship("Comment", back_populates="author")
    notifications = relationship("Notification", back_populates="user")
    # events = relationship("Event", back_populates="related", 
    #                       primaryjoin="and_(Event.related_id==User.id, "
    #                                   "Event.related_type=='users')")

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # Relationships
    owner = relationship("User", back_populates="projects")
    tasks = relationship("Task", back_populates="project")
    # events = relationship("Event", back_populates="related", 
    #                       primaryjoin="and_(Event.related_id==Project.id, "
    #                                   "Event.related_type=='projects')")

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    title = Column(String, index=True)
    description = Column(Text)
    status = Column(String, index=True)
    priority = Column(String, index=True)
    assignee_id = Column(Integer, ForeignKey('users.id'))
    deadline = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # Relationships
    project = relationship("Project", back_populates="tasks")
    assignee = relationship("User", back_populates="tasks")
    comments = relationship("Comment", back_populates="task")
    # events = relationship("Event", back_populates="related", 
    #                       primaryjoin="and_(Event.related_id==Task.id, "
    #                                   "Event.related_type=='tasks')")

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey('tasks.id'))
    author_id = Column(Integer, ForeignKey('users.id'))
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    # Relationships
    task = relationship("Task", back_populates="comments")
    author = relationship("User", back_populates="comments")

class Notification(Base):
    __tablename__ = 'notifications'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String)
    message = Column(Text)
    read = Column(Boolean, default=False)
    event_type = Column(String)
    event_id = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    # Relationships
    user = relationship("User", back_populates="notifications")

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, index=True)
    related_id = Column(Integer, nullable=True)
    related_type = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)