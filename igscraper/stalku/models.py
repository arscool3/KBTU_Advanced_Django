from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, BigInteger
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class Target(Base):
    __tablename__ = 'targets'
    id = Column(Integer, primary_key=True, index=True)
    uid = Column(String, unique=True, index=True)


class Follower(Base):
    __tablename__ = 'followers'
    id = Column(Integer, primary_key=True, index=True)
    uid = Column(String, index=True)
    profile_picture_url = Column(String)
    target_uid = Column(String, ForeignKey('targets.uid'))
    fetched_at = Column(DateTime, default=datetime.now())

    target = relationship("Target")


class Following(Base):
    __tablename__ = 'followings'
    id = Column(Integer, primary_key=True, index=True)
    uid = Column(String, index=True)
    profile_picture_url = Column(String)
    target_uid = Column(String, ForeignKey('targets.uid'))
    fetched_at = Column(DateTime, default=datetime.now())

    target = relationship("Target")






