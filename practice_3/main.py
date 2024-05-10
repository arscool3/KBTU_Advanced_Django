from fastapi import FastAPI, Depends
from pydantic import BaseModel   
from typing import Annotated
import punq

app = FastAPI()

teams = []

class Team(BaseModel):
    title: str
    country: str

class TeamSubLayer:
    def __init__(self, log_message: str):
        self.log_message = log_message

    def add_team(self, team: Team):
        print(self.log_message)
        teams.append(team)
        return f"{team.title} was added "

    def delete_team(self, del_team: Team):
        for team in teams:
            if team.title == del_team.title:
                teams.remove(team)
                return f'{team.title} was deleted'


class TeamMainLayer:
    def __init__(self, repo: TeamSubLayer):
        self.repo = repo

    def add_team(self, team: Team):
        print('Some Logging')
        self.repo.add_team(team)
        print('End logging')

        return 'Team was added'
    
    def delete_team(self, del_team: Team):
        return self.repo.delete_team(del_team)
        

def get_container() -> punq.Container:
    container = punq.Container()
    container.register(TeamSubLayer, instance=TeamSubLayer(log_message='I am inside sub layer'))
    container.register(TeamMainLayer)
    return container


@app.get('/teams')
def get_teams() -> list[Team]:
    return teams


@app.post("/add_team")
def add_team(team: Annotated[str, Depends(get_container().resolve(TeamMainLayer).add_team)]) -> str:
    return team

@app.delete('/remove_team')
def del_team(team: Annotated[str, Depends(get_container().resolve(TeamMainLayer).delete_team)]) -> str:
    return team
