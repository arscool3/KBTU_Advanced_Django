from typing import Annotated
from datetime import date

import sqlalchemy
from sqlalchemy.orm import Session, Mapped, mapped_column, relationship
from database import Base

_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]


class BaseClass:
    id: Mapped[_id]
    name: Mapped[str]


class Human(BaseClass, Base):
    __tablename__ = "humans"

    surname: Mapped[str]
    clan_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("Clan.id"))
    clan: Mapped["Clan"] = relationship(back_populates='humans')


class Clan_leader(BaseClass, Base):
    __tablename__ = "clan_leaders"

    abilities: Mapped[str]
    surname: Mapped[str]
    clan_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("Clan.id"))
    clan: Mapped["Clan"] = relationship(back_populates='leader')


class Territory(BaseClass, Base):
    __tablename__ = "territory"

    address: Mapped[str]
    clan: Mapped["Clan"] = relationship(back_populates='leader')


class Bussiness(BaseClass, Base):
    __tablename__ = "bussiness"

    profit: Mapped[int]
    clan: Mapped["Clan"] = relationship(back_populates='leader')


class Clan(BaseClass, Base):
    __tablename__ = "clan"

    total_profit: Mapped[str]
    members: Mapped[list["Human"]] = relationship(back_populates='clan')
    clan_leader_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey(Clan_leader.id))
    clan_leader: Mapped[Clan_leader] = relationship(back_populates="clan")
    territory_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey(Territory.id))
    territory: Mapped[Territory] = relationship(back_populates="clan")


class Relations(BaseClass, Base):
    __tablename__ = "relations"

    clan_1_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("clan.id"))
    clan_2_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("clan.id"))
    relation_status: Mapped[str]

    clan_1: Mapped["Clan"] = relationship("Clan", foreign_keys=[clan_1_id], backref="clan_1_relations")
    clan_2: Mapped["Clan"] = relationship("Clan", foreign_keys=[clan_2_id], backref="clan_2_relations")
