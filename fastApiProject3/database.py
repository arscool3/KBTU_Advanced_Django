from sqlalchemy import create_engine
from sqlalchemy.orm import Session

url = "postgresql://postgres:postgres@localhost/django_adv_3_lesson"
engine = create_engine(url)
