from typing import Annotated

import sqlalchemy
from sqlalchemy.orm import mapped_column, Mapped, relationship  

from database import Base

_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]

class League(Base):
    __tablename__ = 'League'
    id: Mapped[_id]
    name: Mapped[str]
    country: Mapped[str]

class Team(Base):
    __tablename__ = 'Team'
    id: Mapped[_id]
    name: Mapped[str]
    country: Mapped[str]
    league: Mapped['League'] = relationship()

class Player(Base):
    __tablename__ = 'Player'
    id: Mapped[_id]
    fullname: Mapped[str]
    nationality: Mapped[str]
    position: Mapped[str]
    team: Mapped['Team'] = relationship('players')