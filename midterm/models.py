import sqlalchemy
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship


__all__ = ("ModelBase", "Artist", "Song", "Album")

from midterm.schemas.model_schemas import Song, Album

ModelBase = declarative_base()


song_artist_table = sqlalchemy.table(
    'song_artist',
    ModelBase.metadata,
    sqlalchemy.Column("song_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("songs.id")),
    sqlalchemy.Column("artist_id", sqlalchemy.Integer,  sqlalchemy.ForeignKey('artist.id'))
)

song_album_table = sqlalchemy.table(
    'song_album',
    ModelBase.metadata,
    sqlalchemy.Column("song_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("songs.id")),
    sqlalchemy.Column("album_id", sqlalchemy.Integer, sqlalchemy.ForeignKey('albums.id'))
)


class IdBase:
    id: Mapped[int] = mapped_column(sqlalchemy.Integer, primary_key=True)


class Artist(IdBase, ModelBase):
    __table_name = "artists"


    name: Mapped[str]
    songs: Mapped[list[Song]] = relationship(secondary=song_artist_table, back_populates="artists")
    albums: Mapped[list[Album]] = relationship(back_populates="artist")


class Album(IdBase, ModelBase):
    __table_name = "albums"


    name: Mapped[str]
    songs: Mapped[list[Song]] = relationship(secondary=song_album_table, back_populates="albums")
    artist: Mapped[Artist] = mapped_column(sqlalchemy.ForeignKey("artists.id"))


class Song(IdBase, ModelBase):
    __table_name = "songs"

    name: Mapped[str]
    artists: Mapped[list[Artist]] = relationship(secondary=song_artist_table, back_populates="songs")
    albums: Mapped[list[Album]] = relationship(secondary=song_album_table, back_populates="songs")


class Product(IdBase, ModelBase):
    __table_name = "products"

    name: Mapped[str]
    price: Mapped[float]
    artist: Mapped[Artist] = mapped_column(sqlalchemy.ForeignKey("artists.id"))


class Location(IdBase, ModelBase):
    __table_name = "locations"

    latitude: Mapped[float]
    longitude: Mapped[float]


class Concert(IdBase, ModelBase):
    __table_name = "concerts"

    name: Mapped[str]
    artist: Mapped[Artist] = mapped_column(sqlalchemy.ForeignKey("artists.id"))
    location: Mapped[Location] = mapped_column(sqlalchemy.ForeignKey("locations.id"))