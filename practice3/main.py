from fastapi import FastAPI, Depends
from pydantic import BaseModel   
from typing import Annotated
import punq

app = FastAPI()

football = []

class FootballTeam(BaseModel):
    title: str
    country: str

# def add_football_team(football_team: FootballTeam):
#     football.append(football_team)
#     return f"{football_team.title} was added "


# def delete_football_team(del_team: FootballTeam):
#     for team in football:
#         if team.title == del_team.title:
#             football.remove(team)
#             return f'{team.title} was deleted'


class FootballSubLayer:
    def __init__(self, log_message: str):
        self.log_message = log_message

    def add_team(self, football_team: FootballTeam):
        print(self.log_message)
        football.append(football_team)
        return f"{football_team.title} was added "

    def delete_football_team(self, del_team: FootballTeam):
        for team in football:
            if team.title == del_team.title:
                football.remove(team)
                return f'{team.title} was deleted'


class FootballMainLayer:
    def __init__(self, repo: FootballSubLayer):
        self.repo = repo

    def add_team(self, football_team: FootballTeam):
        print('Some Logging')
        self.repo.add_team(football_team)
        print('End logging')

        return 'team was added'
    
    def delete_football_team(self, del_team: FootballTeam):
        return self.repo.delete_football_team(del_team)
        

def get_container() -> punq.Container:
    container = punq.Container()
    container.register(FootballSubLayer, instance=FootballSubLayer(log_message='I am inside sub layer'))
    container.register(FootballMainLayer)
    return container


@app.get('/teams')
def get_teams() -> list[FootballTeam]:
    return football


@app.post("/add_team")
def add_team(football_team: Annotated[str, Depends(get_container().resolve(FootballMainLayer).add_team)]) -> str:
    return football_team

@app.delete('/remove_team')
def del_team(football_team: Annotated[str, Depends(get_container().resolve(FootballMainLayer).delete_football_team)]) -> str:
    return football_team