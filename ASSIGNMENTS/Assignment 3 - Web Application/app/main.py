from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Mapped, mapped_column, relationship


from . import models
from .database import engine

from .routers import post, users


app = FastAPI()

origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(users.router)



@app.get("/")
async def root():
    return {"message": "Hello World"}
