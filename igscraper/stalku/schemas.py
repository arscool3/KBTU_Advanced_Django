from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class TargetBase(BaseModel):
    uid: str


class TargetCreate(TargetBase):
    pass


class TargetUpdate(TargetBase):
    uid: Optional[str] = None


class Target(TargetBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class FollowerBase(BaseModel):
    uid: str
    profile_picture_url: str
    target_uid: str


class FollowerCreate(FollowerBase):
    pass


class FollowerUpdate(FollowerBase):
    uid: Optional[str] = None
    profile_picture_url: Optional[str] = None


class Follower(FollowerBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    fetched_at: datetime


class FollowingBase(BaseModel):
    uid: str
    profile_picture_url: str
    target_uid: str


class FollowingCreate(FollowingBase):
    pass


class FollowingUpdate(FollowingBase):
    uid: Optional[str] = None
    profile_picture_url: Optional[str] = None


class Following(FollowingBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    fetched_at: datetime
