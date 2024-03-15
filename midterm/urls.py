import models
from fastapi import APIRouter, Depends, HTTPException
from dependencies import *
from sqlalchemy import select
from schemas import *


router = APIRouter(prefix="")


@router.post("/artist/", tags=['artists'])
def create_artist(artist: CreateArtist, db: Database) -> str:
    db.add(models.Artist(artist.model_dump()))
    return artist.name


@router.get("/artists/", tags=["artists"])
def get_artists(db: Database) -> list[Artist]:
    db_artists = db.query(models.Artist).scalars()
    return list(map(Artist.model_validate, db_artists))


@router.delete("/artists/", tags=["artists"])
def delete_artist(db: Database, artist_id: int) -> bool:
    try:
        artist = db.get(models.Artist, id=artist_id)
        db.delete(artist)
        return True
    except:
        return False


@router.get("/artists/", tags=["artists"])
def get_artist_by_id(artist: ArtistDependency) -> Artist | None:
    return artist


@router.post('/songs/', tags=["songs"])
def create_song(song: CreateSong, db: Database) -> bool:
    song_data = song.model_dump()
    db.add_song(song_data)
    return True


@router.get('/songs/', tags=["songs"])
def get_songs(db: Database) -> list[Song]:
    db_songs = db.query(models.Song).scalars()
    return list(map(Song.model_validate, db_songs))


@router.delete("/songs/", tags=["songs"])
def delete_song(song: SongDependency) -> bool:
    song.delete()
    return True


@router.get("/songs/", tags=["songs"])
def get_song_by_id(song: SongDependency) -> Song | None:
    return song


@router.post("/albums/", tags=["albums"])
def create_album(album: CreateAlbum, db: Database) -> bool:
    db.add(models.Album, album.model_dump())
    return True


@router.delete("/albums/", tags=["albums"])
def delete_album(album: AlbumDependency) -> bool:
    album.delete()
    return True


@router.get("/albums/", tags=["albums"])
def get_albums(db: Database) -> list[Album]:
    db_albums = db.query(models.Album).scalars()
    return list(map(Album.model_validate, db_albums))


@router.get("/albums/", tags=["albums"])
def get_album_by_id(album: AlbumDependency) -> Album | None:
    return album


@router.put("/concerts/", tags=["concerts"])
def create_concert(concert: CreateConcert, db: Database) -> bool:
    db.add(models.Concert, concert.model_dump())
    return True


@router.get("/concerts/", tags=["concerts"])
def get_concerts(db: Database) -> list[Concert]:
    db_concerts = db.query(models.Concert).scalars()
    return list(map(Concert.model_validate, db_concerts))


@router.get("/concerts/", tags=["concerts"])
def get_concert_by_id(concert: ConcertDependency) -> Concert | None:
    return concert

@router.delete("/concerts/", tags=["concerts"])
def delete_concert(concert: ConcertDependency) -> bool:
    concert.delete()
    return True