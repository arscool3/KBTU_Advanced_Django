import confluent_kafka
from schemas import Film
from typing import NewType



Message = NewType('Message', str)

producer = confluent_kafka.Producer(
    {"bootstrap.servers": "localhost:9092"}
)

topic = 'main_topic'


def produce(film: Film):
    producer.produce(topic=topic, value=film.model_dump_json())
    producer.flush()
    
def generate_recommendations(films):
    genre_map = {}
    for film in films:
        if film.genre not in genre_map:
            genre_map[film.genre] = []
        genre_map[film.genre].append(film.name)

    for film in films:
        recommendations = genre_map.get(film.genre, [])
        film.recommendations = [rec for rec in recommendations if rec != film.name]



if __name__ == '__main__':
    films = [
        Film(name='emma', director='idk', genre='romance'),
        Film(name='little women', director='greta gerwig', genre='romance'),
        Film(name='spiderman no way home', director='idk', genre='Action'),
        Film(name='the amazing spiderman', director='idk', genre='action'),
        Film(name='spiderman with miles morales in it idk', director='idk', genre='Action'),
    ]
    
    generate_recommendations(films)

    for film in films:
        produce(film)
