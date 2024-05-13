from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import Annotated
from models import Team, Player, League

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


@app.post('/teams')
def add_team(team: Team) -> str:
    pass


@app.post('/player')
def add_player(player: Player) -> str:
    pass


@app.post('/league')
def add_league(league: League) -> str:
    pass