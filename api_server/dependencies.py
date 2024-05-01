from typing import Annotated
import confluent_kafka
impor dramatiq
from fastapi import Depends
from sqlalchemy.orm import Session
import models
from api_server.schemas import SpotifyWrappedTask
from database import get_db, get_kafka_producer
from schemas import Artist, Song, Album, Concert

__all__ = (
    "Database",
    "Producer"
    "ArtistDependency",
    "SongDependency",
    "ModelArtistDependency",
    "ModelSongDependency",
    "AlbumDependency",
    "AlbumDependencyClass",
    "ModelAlbumDependency",
    "ModelConcertDependency",
    "ConcertDependency",
    "BackgroundTaskStatusDependency"
)

Database = Annotated[Session, Depends(get_db)]
Producer = Annotated[confluent_kafka.Producer, Depends(get_kafka_producer)]


def get_artist_model(artist_id: int, db: Database) -> models.Artist | None:
    db_artist = db.get(models.Artist, artist_id)
    return db_artist


def get_song_model(song_id: int, db: Database) -> models.Song | None:
    db_song = db.get(models.Song, song_id)
    return db_song


def get_album_model(album_id: int, db: Database) -> models.Album | None:
    db_album = db.get(models.Album, album_id)
    return db_album


def get_concert_by_id(concert_id: int, db: Database) -> models.Concert | None:
    return db.get(models.Concert, concert_id)

def get_background_task_by_id(task_id: int) -> SpotifyWrappedTask | None:
    task = dramatiq.Message.fetch(task_id)
    if task is None:
        return None
    return SpotifyWrappedTask(task_id, task.get_status())


class ArtistDependencyClass:
    def __call__(self, db_artist: models.Artist = Depends(get_artist_model)) -> Artist | None:
        return Artist.model_validate(db_artist)


class SongDependencyClass:
    def __call__(self, db_song: models.Song = Depends(get_song_model)) -> Song | None:
        return Song.model_validate(db_song)


class AlbumDependencyClass:
    def __call__(self, db_album: models.Album = Depends(get_album_model)) -> Album | None:
        return Album.model_validate(db_album)


class ConcertDependencyClass:
    def __call__(self, db_concert: models.Concert = Depends(get_concert_by_id)) -> Concert | None:
        return Concert.model_validate(db_concert)


ArtistDependency = Annotated[Artist, Depends(ArtistDependencyClass())]
SongDependency = Annotated[Song, Depends(SongDependencyClass())]
AlbumDependency = Annotated[Album, Depends(AlbumDependencyClass())]
ConcertDependency = Annotated[Concert, Depends(ConcertDependencyClass())]


ModelArtistDependency = Annotated[models.Artist, Depends(get_artist_model)]
ModelSongDependency = Annotated[models.Song, Depends(get_song_model)]
ModelAlbumDependency = Annotated[models.Album, Depends(get_album_model)]
ModelConcertDependency = Annotated[models.Concert, Depends(get_concert_by_id)]


BackgroundTaskStatusDependency = Annotated[SpotifyWrappedTask, Depends(get_background_task_by_id)]

