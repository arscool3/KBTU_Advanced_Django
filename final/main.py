from fastapi import FastAPI
import routers

from routers import auth, profile, project, post, contribution

app = FastAPI()


app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(project.router)
app.include_router(post.router)
app.include_router(contribution.router)
