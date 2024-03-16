from sqlalchemy import create_engine


DATABASE_URL = f"postgresql://postgres:postgres@localhost/lesson_6"

engine = create_engine(DATABASE_URL)
