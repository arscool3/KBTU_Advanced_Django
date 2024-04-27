from fastapi import FastAPI, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

import models as db
import schemas as sc
import repository as rp
from database import engine

app = FastAPI()

app.include_router()


def get_db():
    try:
        session = Session(engine)
        yield session
        session.commit()
    except:
        raise
    finally:
        session.close()


@app.post("/clan", tags=['clan'])
def add_clan(clan: sc.ClanSchema, session: Session = Depends(get_db)) -> str:
    session.add(db.Clan(**clan.model_dump()))
    return clan.name


@app.get("/clan", tags=['clan'])
def get_clans(session: Session = Depends(get_db)) -> list[sc.ClanSchema]:
    db_clans = session.execute(select(db.Clan)).scalars().all()
    clans = [sc.ClanSchema.model_validate(db_clan) for db_clan in db_clans]
    return clans


@app.get("/clan/id/", tags=['clan'])
def get_clan_by_id(id: int, db: Session = Depends(get_db)) -> sc.ClanSchema:
    db_clan = db.get(db.Clan, id)
    clan = sc.ClanSchema.model_validate(db_clan)
    return clan


# @app.post("/human")
# def add_human(human: sc.HumanSchema, db: Session = Depends(get_db)) -> str:
#     db.add(db.Human(**human.model_dump()))
#     return human.name
#
#
# @app.get("/human")
# def get_humans(db: Session = Depends(get_db)) -> list[sc.HumanSchema]:
#     db_humans = db.execute(select(db.Human)).scalars()
#     humans = []
#     for db_human in db_humans:
#         human = sc.HumanSchema.model_validate(db_human)
#         humans.append(human)
#     return humans

def get_human_repository(db: Session = Depends(get_db)):
    return rp.HumanRepository(db)

@app.post("/human/", response_model=sc.HumanSchema, tags=['human'])
def create_human(human: sc.HumanSchema, human_repository: rp.HumanRepository = Depends(get_human_repository)):
    return human_repository.create_human(human)

@app.get("/human/", response_model=list[sc.HumanSchema], tags=['human'])
def read_humans(skip: int = 0, limit: int = 100, human_repository: rp.HumanRepository = Depends(get_human_repository)):
    humans = human_repository.get_humans(skip=skip, limit=limit)
    return humans

@app.get("/human/{human_id}", response_model=sc.HumanSchema, tags=['human'])
def read_human(human_id: int, human_repository: rp.HumanRepository = Depends(get_human_repository)):
    return human_repository.get_human(human_id)


@app.post("/territory", tags=['territory'])
def add_territory(territory: sc.TerritorySchema, db: Session = Depends(get_db)) -> str:
    db.add(db.Territory(**territory.model_dump()))
    return territory.name


@app.get("/territory", tags=['territory'])
def get_territories(db: Session = Depends(get_db)) -> list[sc.TerritorySchema]:
    db_territories = db.execute(select(db.Territory)).scalars()
    territories = []
    for db_territory in db_territories:
        territory = sc.TerritorySchema.model_validate(db_territory)
        territories.append(territory)
    return territories


@app.post("/business", tags=['business'])
def add_business(business: sc.BusinessSchema, db: Session = Depends(get_db)) -> str:
    db.add(db.Business(**business.model_dump()))
    return business.name


@app.get("/business", tags=['business'])
def get_business(db: Session = Depends(get_db)) -> list[sc.BusinessSchema]:
    db_businesses = db.execute(select(db.Business)).scalars()
    businesses = []
    for db_business in db_businesses:
        business = sc.TerritorySchema.model_validate(db_business)
        businesses.append(business)
    return businesses


@app.get("/clan_leaders/", response_model=list[sc.ClanLeaderSchema], tags=['clan leaders'])
def read_clan_leaders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    clan_leaders = db.query(db.Clan_leader).offset(skip).limit(limit).all()
    return clan_leaders

@app.post("/clan_leaders/", response_model=sc.ClanLeaderSchema, tags=['clan leaders'])
def create_clan_leader(clan_leader: sc.ClanLeaderSchema, db: Session = Depends(get_db)):
    # Assuming the Human part (e.g., name, id) is correctly handled in HumanSchema
    # and ClanLeaderSchema correctly inherits and extends it with specific fields like abilities
    db_clan_leader = db.Clan_leader(**clan_leader.dict())
    db.add(db_clan_leader)
    db.commit()
    db.refresh(db_clan_leader)
    return db_clan_leader


@app.get("/relations/", response_model=list[sc.RelationsSchema], tags=['relations'])
def read_relations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    relations = db.query(db.Relations).offset(skip).limit(limit).all()
    return relations


@app.post("/relations/", response_model=sc.RelationsSchema, tags=['relations'])
def create_relation(relation: sc.RelationsSchema, db: Session = Depends(get_db)):
    db_relation = db.Relations(name=relation.name, clan_1_id=relation.clan_1_id, clan_2_id=relation.clan_2_id,
                            relation_status=relation.relation_status)
    db.add(db_relation)
    db.commit()
    db.refresh(db_relation)
    return db_relation
