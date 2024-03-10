from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = (f'postgresql://postgres:123@localhost:5432/movie_db')



engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='123',
#                                 cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database conn successfull")
#         break
#     except Exception as error:
#         print("Connection failed")
#         print(error)
#         time.sleep(2)
