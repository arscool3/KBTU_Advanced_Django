from fastapi import FastAPI, Depends
from pydantic import BaseModel

app = FastAPI()

songs = {}
paintings = {}

class Art(BaseModel):
    name: str
    author: str

class Song(Art):
    pass

class Painting(Art):
    pass

class ArtDependency:
    def __init__(self, art_type: type[Art]):
        self.art_type = art_type

    def __call__(self, art: Art) -> str:
        if self.art_type == Song:
            songs[art.name] = art.author
            return "new album dropped"
        elif self.art_type == Painting:
            paintings[art.name] = art.author
            return "someone painted smth!"

s_dep = ArtDependency(Song)
p_dep = ArtDependency(Painting)

@app.get('/songs')
def get_all_songs() -> dict:
    return songs

@app.post('/song')
def add_song(song: Song, response: dict = Depends(s_dep)) -> dict:
    return {"message": response}

@app.get('/paintings')
def get_all_paintings() -> dict:
    return paintings

@app.post('/painting')
def add_painting(painting: Painting, response: dict = Depends(p_dep)) -> dict:
    return {"message": response}
