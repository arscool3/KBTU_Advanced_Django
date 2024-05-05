from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

# have to be stored in .env
POSTGRES_URL="postgresql://postgres:JASIK_2004@localhost:5432/micro_service_fastapi"


url = POSTGRES_URL
engine = create_engine(url)
session = Session(engine)

Base = declarative_base()