from fastapi import FastAPI
import routers

from routers import auth, profile

app = FastAPI()


app.include_router(auth.router)
app.include_router(profile.router)
