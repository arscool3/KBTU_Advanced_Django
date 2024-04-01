from fastapi import FastAPI

from core.models import Film
from core.database import session, Film as DbFilm
from sqlalchemy import select

from confluent_kafka import Producer

producer = Producer(
    {"bootstrap.servers": "localhost: 9092"}
)

topic = "main_topic"

app = FastAPI()


@app.post("/films/")
def create_film_kafka(film: Film):
    producer.produce(topic=topic, value=film.model_dump_json())
    producer.flush()
    return f"Produced {film}"


@app.get("/films/")
def get_films():
    db_films = session.execute(select(DbFilm)).scalars().all()
    return [Film.model_validate(film) for film in db_films]