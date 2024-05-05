from typing import List, Optional
from pydantic import BaseModel


class NetflixBase(BaseModel):
    name: str


class NetflixCreate(NetflixBase):
    pass


class Netflix(NetflixBase):
    id: int

    class Config:
        from_attributes = True


class GenreBase(NetflixBase):
    pass


class GenreCreate(NetflixCreate):
    pass


class Genre(GenreBase):
    id: int

    class Config:
        from_attributes = True


class DirectorBase(NetflixBase):
    pass


class DirectorCreate(NetflixCreate):
    pass


class Director(DirectorBase):
    id: int

    class Config:
        from_attributes = True


class ActorBase(NetflixBase):
    pass


class ActorCreate(NetflixCreate):
    pass


class Actor(ActorBase):
    id: int

    class Config:
        from_attributes = True


class UserBase(NetflixBase):
    username: str
    email: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    watchlist: List['Film'] = []

    class Config:
        from_attributes = True


class FilmBase(NetflixBase):
    title: str
    release_year: int


class FilmCreate(FilmBase):
    director_id: int
    genre_id: int
    actor_id: int


class Film(FilmBase):
    id: int
    director: Director
    genre: Genre
    actor: Actor
    users: List[User] = []

    class Config:
        from_attributes = True


class UserWatchlistBase(BaseModel):
    user_id: int
    film_id: int


class UserWatchlistCreate(UserWatchlistBase):
    pass


class UserWatchlist(UserWatchlistBase):
    added_at: str

    class Config:
        from_attributes = True
