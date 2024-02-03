from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Optional

app = FastAPI()


class Film(BaseModel):
    id: Optional[int] = Field(default=None, example=1)
    name: str = Field(..., example="Горбатая гора")
    description: str = Field(...,
                             example="На фоне живописных просторов штата Вайоминг разворачивается изящная "
                                     "романтическая история сложных взаимоотношений двух молодых людей — помощника "
                                     "владельца ранчо и ковбоя родео"
                             )
    rating: float = Field(..., gt=0, lt=10, example=8.8)
    director: str = Field(..., example="Энг Ли")


films_db: Dict[int, Film] = {
    1: Film(id=1, name="Горбатая гора",
            description="На фоне живописных просторов штата Вайоминг разворачивается изящная романтическая история "
                        "сложных взаимоотношений двух молодых людей — помощника владельца ранчо и ковбоя родео",
            rating=8.8, director="Энг Ли"),
    2: Film(id=2, name="Джентельмены",
            description="Талантливый выпускник Оксфорда, применив свой уникальный ум и невиданную дерзость, придумал "
                        "нелегальную схему обогащения",
            rating=7.8, director="Гай Ричи"),
    3: Film(id=3, name="1917", description="Перед вами история о двух молодых британских солдатах во время Первой "
                                           "мировой войны, которым поручено пересечь вражескую территорию и "
                                           "доставить важное сообщение",
            rating=8.3, director="Сэм Мендес"),
}


@app.get("/films")
async def list_films():
    return list(films_db.values())


@app.get("/films/{film_id}")
async def get_film(film_id: int):
    if film_id not in films_db:
        raise HTTPException(status_code=404, detail="Film not found")
    return films_db[film_id]


@app.post("/films", status_code=201)
async def add_film(film: Film):
    if film.id in films_db:
        raise HTTPException(status_code=400, detail="Film already exists")
    films_db[film.id] = film
    return film


@app.get("/films/rating/{rating}")
async def get_film_by_rating(rating: float):
    filtered_films = {film_id: film for film_id, film in films_db.items() if film.rating == rating}
    if not filtered_films:
        raise HTTPException(status_code=404, detail="No films found with the given rating")
    return filtered_films
