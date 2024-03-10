from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from config import settings

SQLALCHEMY_DATABASE_URL = (f'postgresql://{settings.database_username}:{settings.database_password}@'
                           f'{settings.database_hostname}:{settings.database_port}/{settings.database_name}')



engine = create_engine(SQLALCHEMY_DATABASE_URL)

session = Session(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():

    try:
        yield session
        session.commit()
    except:
        raise
    finally:
        session.close()

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
