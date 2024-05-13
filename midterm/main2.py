from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import Annotated
import punq
app = FastAPI()

teams = []
leagues = []
players = []
managers = []
positions = (
    'LW', 'ST', 'RW', 'LM', 'CAM', 'RM', 'CM', 'CDM', 'LB', 'CB', 'RB', 'GK'
)

class League(BaseModel):
    id: int
    name: str
    region: str

class Team(BaseModel):
    id: int
    name: str
    country: str
    league_id: int

class FootballPerson(BaseModel):
    id: int
    fullname: str
    nationality: str
    team_id: int

class Player(FootballPerson):
    position: str
    transfer_value: int

class Manager(FootballPerson):
    yoe: int


class TeamSubLayer:
    def __init__(self, log_message: str):
        self.log_message = log_message

    def add_team(self, team: Team):
        print(self.log_message)
        teams.append(team)
        return f"{team.name} was added"


class TeamMainLayer:
    def __init__(self, repo: TeamSubLayer):
        self.repo = repo

    def add_team(self, team: Team):
        print('Start Logging')
        self.repo.add_team(team)
        print('End logging')
        return "Team was added"
        

def get_container() -> punq.Container:
    container = punq.Container()
    container.register(TeamSubLayer, instance=TeamSubLayer(log_message='I am inside sub layer'))
    container.register(TeamMainLayer)
    return container

def get_team_by_id(id: int) -> Team | None:
    for team in teams:
        if id == team.id:
            return team
    return None



def add_league_dep(league: League) -> str:
    leagues.append(league)
    name = league.name
    region = league.region
    return f'you have succesfully added {name} league in the {region} region' 

def add_player_dep(pl: Player) -> str:
    players.append(pl)
    name = pl.fullname
    team = get_team_by_id(pl.team_id)
    if team != None:
        return f'you have succesfully added player: {name} to the {team.name}' 
    return 'sorry there is no such team'


@app.post('/leagues')
def add_league(league_dep: str = Depends(add_league_dep)) -> str:
    return league_dep

@app.post('/teams')
def add_team(team: Annotated[str, Depends(get_container().resolve(TeamMainLayer).add_team)]) -> str:
    return team

@app.post('/players')
def add_player(player_dep: str = Depends(add_player_dep)) -> str:
    return player_dep


@app.get('/teams')
def get_teams() -> list[Team]:
    return teams

@app.get('/leagues')
def get_leagues() -> list[League]:
    return leagues

@app.get('/players')
def get_players() -> list[Player]:
    return players

@app.get('/managers')
def get_managers() -> list[Manager]:
    return managers
