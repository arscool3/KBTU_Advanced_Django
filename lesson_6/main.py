import punq
from fastapi.params import Depends
from fastapi import FastAPI
from sqlalchemy import select

import models as db
from database import session
from schemas import Movie, CreateMovie, Director, CreateDirector, Genre, CreateGenre, Studio, CreateStudio, ReturnType
from repository import MovieRepository, DirectorRepository, GenreRepository, StudioRepository, BaseRepository

app = FastAPI()


def dependency(arg: int) -> dict:
    return {'ok': arg}


@app.get("/")
def lol(dep_func: dict = Depends(dependency)):
    return dep_func


class Dependency:
    def __init__(self, repo: BaseRepository):
        self.repo = repo

    def __call__(self, id: int) -> ReturnType:
        return self.repo.get_by_id(id)


def get_container(repository: type[BaseRepository]) -> punq.Container:
    container = punq.Container()
    container.register(BaseRepository, repository, instance=repository(session=session))
    container.register(Dependency)
    return container


# app.add_api_route("/movies", get_container(MovieRepository).resolve(Dependency), methods=["GET"])
# app.add_api_route("/movies", get_container(MovieRepository).resolve(Dependency), methods=["POST"])
# app.add_api_route("/directors", get_container(DirectorRepository).resolve(Dependency), methods=["GET"])
# app.add_api_route("/directors", get_container(DirectorRepository).resolve(Dependency), methods=["POST"])
# app.add_api_route("/genres", get_container(GenreRepository).resolve(Dependency), methods=["GET"])
# app.add_api_route("/genres", get_container(GenreRepository).resolve(Dependency), methods=["POST"])
# app.add_api_route("/ratings", get_container(RatingRepository).resolve(Dependency), methods=["GET"])
# app.add_api_route("/ratings", get_container(RatingRepository).resolve(Dependency), methods=["POST"])


@app.get("/movie")
def get_movie():
    db_movies = session.execute(select(db.Movie)).scalars().all()
    movies = []
    for db_movie in db_movies:
        movies.append(Movie.model_validate(db_movie))
    return movies


@app.post("/movie")
def add_movie(movie: CreateMovie):
    session.add(db.Movie(**movie.model_dump()))
    session.commit()
    session.close()
    return "Movie was added"


@app.get("/director")
def get_director():
    db_directors = session.execute(select(db.Director)).scalars().all()
    directors = []
    for db_director in db_directors:
        directors.append(Director.model_validate(db_director))
    return directors


@app.post("/director")
def add_director(director: CreateDirector):
    session.add(db.Director(**director.model_dump()))
    session.commit()
    session.close()
    return "Director was added"


@app.get("/genre")
def get_genre():
    db_genres = session.execute(select(db.Genre)).scalars().all()
    genres = []
    for db_genre in db_genres:
        genres.append(Genre.model_validate(db_genre))
    return genres


@app.post("/genre")
def add_genre(genre: CreateGenre):
    session.add(db.Genre(**genre.model_dump()))
    session.commit()
    session.close()
    return "Genre was added"


@app.get("/studio")
def get_studio():
    db_studios = session.execute(select(db.Studio)).scalars().all()
    studios = []
    for db_studio in db_studios:
        studios.append(Studio.model_validate(db_studio))
    return studios


@app.post("/studio")
def add_studio(rating: CreateStudio):
    session.add(db.Studio(**rating.model_dump()))
    session.commit()
    session.close()
    return "Studio was added"
