from fastapi import FastAPI
from typing import List
from pydantic import BaseModel,Field

app = FastAPI()

Films = [
    
]

class Film (BaseModel):
    name: str
    description:str
    rating: int = Field(ge=0, lt=10)
    director: str


@app.get("/films")
def get_films() -> list[Film]:
    return Films

@app.post("/film")
def create_film(film:Film)-> str:
    Films.append(film)

    return "Film succesfully added"

@app.get("/film/{id}")
def get_film_by_id(id:int) -> Film:
    return Films[id]

@app.get("/film/rating")
def get_film_by_rating(rating:int)-> list[Film]:
    return  [film for film in Films if film.rating == rating]






# @app.get("/students/{id}")
# def test(id: int) -> Student:
#     return students[id]


# @app.post("/students")
# def add_student(student: Student) -> str:
#     students.append(student)
#     return "succes"



# [
#   {
#     "name": "Barbie",
#     "description": "Общество, в котором всех девушек зовут Барби, а всех парней – Кеном в мире является бесконфликтным, идеально-утопическим, где у всех равные прав",
#     "rating": 6.6,
#     "director": "Грета Гервиг"
#   },
#   {
#     "name": "Оппенгеймер",
#     "description": "История жизни американского физика-теоретика Роберта Оппенгеймера, который во времена Второй мировой войны руководил Манхэттенским проектом",
#     "rating": 8.2,
#     "director": "Кристофер Нолан"
#   }
# ]