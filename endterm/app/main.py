from contextlib import contextmanager

import punq
from fastapi import FastAPI, Depends, HTTPException

from fastapi.middleware.cors import CORSMiddleware

from .database import session as db, session
from .routers.genre import router as genre_router
from .routers.movie import router as movie_router
from .routers.director import router as director_router
from .routers.studio import router as studio_router

from .schemas import Movie, Genre, CreateGenre

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(genre_router)
app.include_router(movie_router)
app.include_router(director_router)
app.include_router(studio_router)
