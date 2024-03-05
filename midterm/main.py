from fastapi import FastAPI
from pydantic import BaseModel
from typing import Annotated
from models import Team, Player
app = FastAPI()

@app.get('/teams')
def get_teams() -> list[Team]:
    pass

@app.get('/teams/{id}')
def get_team_by_id() -> Team:
    pass

@app.get('/teams/{id}/players')
def get_players_of_team() -> list[Player]:
    pass
