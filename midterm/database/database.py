from sqlalchemy import create_engine, Boolean, Column, ForeignKey, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from dotenv import dotenv_values
from datetime import datetime
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
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    tasks = relationship("Task", back_populates="owner")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    tasks = relationship("Task", back_populates="category")

class Priority(Base):
    __tablename__ = "priorities"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(Integer)
    name = Column(String)

    tasks = relationship("Task", back_populates="priority")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    is_completed = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    priority_id = Column(Integer, ForeignKey("priorities.id"), nullable=True)

    owner = relationship("User", back_populates="tasks")
    category = relationship("Category", back_populates="tasks")
    priority = relationship("Priority", back_populates="tasks")
    audits = relationship("TaskAudit", back_populates="task")
    history = relationship("TaskHistory", back_populates="task")

class TaskAudit(Base):
    __tablename__ = "task_audit"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    action = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    performed_by = Column(Integer, ForeignKey("users.id"))

    task = relationship("Task", back_populates="audits")
    user = relationship("User")

class TaskHistory(Base):
    __tablename__ = "task_history"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    title = Column(String, index=True)
    description = Column(Text)
    is_completed = Column(Boolean)
    timestamp = Column(DateTime, default=datetime.utcnow)

    task = relationship("Task", back_populates="history")