import sqlalchemy
from sqlalchemy.orm import declarative_base, relationship

ModelBase = declarative_base()


class IdBase:
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)


class Hooper(IdBase, ModelBase):
    __tablename__ = "hoopers"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)

    commands = relationship("Command", back_populates="hooper")


class Command(IdBase, ModelBase):
    __tablename__ = "commands"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    description = sqlalchemy.Column(sqlalchemy.String)

    hooper_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("hoopers.id"))
    hooper = relationship("Hooper", back_populates="commands")

    conferences = relationship("Conference", secondary="command_conference")


class Conference(IdBase, ModelBase):
    __tablename__ = "conferences"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    location_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("locations.id"))

    location = relationship("Location")

    commands = relationship("Command", secondary="command_conference")


class Location(IdBase, ModelBase):
    __tablename__ = "locations"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    latitude = sqlalchemy.Column(sqlalchemy.Float)
    longitude = sqlalchemy.Column(sqlalchemy.Float)


# Example of additional tables if needed
# hooper_conference_table = sqlalchemy.Table(
#     'hooper_conference',
#     ModelBase.metadata,
#     sqlalchemy.Column("hooper_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("hoopers.id")),
#     sqlalchemy.Column("conference_id", sqlalchemy.Integer, sqlalchemy.ForeignKey('conferences.id'))
# )

# command_conference_table = sqlalchemy.Table(
#     'command_conference',
#     ModelBase.metadata,
#     sqlalchemy.Column("command_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("commands.id")),
#     sqlalchemy.Column("conference_id", sqlalchemy.Integer, sqlalchemy.ForeignKey('conferences.id'))
# )

