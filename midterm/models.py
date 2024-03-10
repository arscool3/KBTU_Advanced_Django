import sqlalchemy
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship

__all__ = ("Mark", "Vehicle", "Location", "Fine", "Insurance", "Person", "ModelBase")

ModelBase = declarative_base()

insurance_person_table = sqlalchemy.Table(
    'insurance_person',
    ModelBase.metadata,
    sqlalchemy.Column('insurance_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('insurances.id')),
    sqlalchemy.Column('person_id', sqlalchemy.String, sqlalchemy.ForeignKey('people.iin'))
)

insurance_vehicle_table = sqlalchemy.Table(
    'insurance_vehicle',
    ModelBase.metadata,
    sqlalchemy.Column('insurance_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('insurances.id')),
    sqlalchemy.Column('vehicle_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('vehicles.id'))
)


class IdBase:
    id: Mapped[int] = mapped_column(sqlalchemy.Integer, primary_key=True)


class Mark(IdBase, ModelBase):
    __tablename__ = "marks"

    name: Mapped[str]
    vehicles: Mapped[list["Vehicle"]] = relationship(back_populates="mark")


class Vehicle(ModelBase, IdBase):
    __tablename__ = "vehicles"

    mark_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("marks.id"))
    mark: Mapped[Mark] = relationship(back_populates="vehicles")
    name: Mapped[str]
    owner_id: Mapped[str] = mapped_column(sqlalchemy.ForeignKey("people.iin"))
    owner: Mapped["Person"] = relationship(back_populates="vehicles")
    fines: Mapped[list["Fine"]] = relationship(back_populates="fined_vehicle")
    insurances: Mapped[list["Insurance"]] = relationship(secondary=insurance_vehicle_table, back_populates="vehicles")


class Location(ModelBase, IdBase):
    __tablename__ = "locations"

    latitude: Mapped[float]
    longitude: Mapped[float]
    fines: Mapped[list["Fine"]] = relationship(back_populates="location")


class Fine(ModelBase, IdBase):
    __tablename__ = "fines"

    fined_person_id: Mapped[str] = mapped_column(sqlalchemy.ForeignKey("people.iin"))
    fined_person: Mapped["Person"] = relationship(back_populates="fines")
    fined_vehicle_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("vehicles.id"))
    fined_vehicle: Mapped["Vehicle"] = relationship(back_populates="fines")
    fine_amount: Mapped[int]
    location_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("locations.id"))
    location: Mapped[Location] = relationship(back_populates="fines")


class Insurance(ModelBase, IdBase):
    __tablename__ = "insurances"

    people: Mapped[list["Person"]] = relationship(secondary=insurance_person_table, back_populates="insurances")
    vehicles: Mapped[list["Vehicle"]] = relationship(secondary=insurance_vehicle_table, back_populates="insurances")
    insurance_amount: Mapped[int]


class Person(ModelBase):
    __tablename__ = "people"

    iin: Mapped[str] = mapped_column(sqlalchemy.String, primary_key=True)
    name: Mapped[str]
    surname: Mapped[str]
    fines: Mapped[list["Fine"]] = relationship(back_populates="fined_person")
    vehicles: Mapped[list[Vehicle]] = relationship(back_populates="owner")
    insurances: Mapped[list[Insurance]] = relationship(secondary=insurance_person_table, back_populates="people")
